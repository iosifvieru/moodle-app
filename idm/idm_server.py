import grpc
from concurrent import futures
import auth_pb2
import auth_pb2_grpc

import hashlib, datetime, jwt, uuid, os, dotenv
from data.model import User

import redis
from redis.exceptions import ConnectionError

dotenv.load_dotenv()

secret = os.getenv('JWT_SECRET')
alg = os.getenv('JWT_ALGORITHM')
expiration = int(os.getenv('JWT_EXPIRATION'))
password_secret = os.getenv('PASS_SECRET')

print(secret)
print(password_secret)

redis_client = redis.StrictRedis(host='10.5.0.5', port=6379, decode_responses=True)

class AuthenticateServicer(auth_pb2_grpc.AuthenticateServicer):
    def authenticate(self, request, context):
        """ 
        checks if the user is in the database.
        """
        user = User.get_or_none(email=request.username)

        """
        returns an error code if the user is not found.
        """
        if user is None:
            print("No user found.")
            return auth_pb2.AuthResponse(status="ERROR", message="No user found.")

        pass_to_be_encoded = request.password
        pass_to_be_encoded += password_secret
        encoded_password = hashlib.md5(pass_to_be_encoded.encode()).hexdigest()

        """
        checks whether the password is the same as the one from database.
        """
        if(encoded_password != user.parola):
            return auth_pb2.AuthResponse(status="ERROR", message="Username or password is incorrect.")

        """
        everything seems ok so i m generating the jwt.

        !!!! "sub" MUST be a string.
        """
        jwt_payload = {
            "iss": "http",
            "sub": str(user.id),
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=expiration),
            "jti": uuid.uuid4().hex,
            "role": user.rol,
            "email": user.email
        }
        """
        enconding the token.
        """
        token = jwt.encode(jwt_payload, secret, alg);

        """
        returning the jwt and an OK status.
        """

        print(f"[LOGIN] {token} la data de {datetime.datetime.now()}")
        return auth_pb2.AuthResponse(status="OK", message=token)

    def validate(self, request, context):
        token = str(request.jwt)
        """
        checks if the token is in the blacklist.
        """

        try:
            if not redis_client.ping():
                raise ConnectionError("Redis is not connected")
            
            if redis_client.exists(token) == 1:
                return auth_pb2.JWTValidateResponse(valid=False)
        
            """
            decoding the token.
            """
            decoded_token = jwt.decode(token, secret, algorithms=alg)

            """
            checks if the token is expired.
            """
            if not "exp" in decoded_token:
                return auth_pb2.JWTValidateResponse(valid=False)
            
            token_expire_date = datetime.datetime.fromtimestamp(decoded_token["exp"])
            current_time = datetime.datetime.now()

            if((token_expire_date < current_time)):
                return auth_pb2.JWTValidateResponse(valid=False)

            """
            maybe further checks...
            """

        except jwt.ExpiredSignatureError as e:
            print("[IDM] Error:", e)
            return auth_pb2.JWTValidateResponse(valid=False)
        except jwt.InvalidTokenError as e:
            print("[IDM] Error:", e) 
            return auth_pb2.JWTValidateResponse(valid=False)
        except ConnectionError as e:
            print("[IDM] Error:", e)
            return auth_pb2.JWTValidateResponse(valid=False)
        except Exception as e:
            print("[IDM] Error:", e)
            raise e

        """
        i guess the token is valid...
        """
        return auth_pb2.JWTValidateResponse(valid=True)

    def invalidate(self, request, context):
        token = request.jwt
        try:
            if not redis_client.ping():
                return auth_pb2.JWTInvalidateResponse(deleted=False)

            #if token in jwt_blacklist:
            if redis_client.exists(token) == 1:
                return auth_pb2.JWTInvalidateResponse(deleted=False)

            #jwt_blacklist.append(token)
            redis_client.setex(token, expiration * 60, "blacklisted")
            return auth_pb2.JWTInvalidateResponse(deleted=True)

        except Exception:
            return auth_pb2.JWTInvalidateResponse(deleted=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthenticateServicer_to_server(AuthenticateServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    print("[IDM] starting idm..")
    serve()