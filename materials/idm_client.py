import grpc
import auth_pb2
import auth_pb2_grpc

HOST="10.5.0.3"
PORT=50051

"""
THIS RETURNS A TOKEN.

    username -> str
    password -> str
"""
def login(username: str, password: str):
    address = f"{HOST}:{PORT}"
    with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
        stub = auth_pb2_grpc.AuthenticateStub(channel)
        response = stub.authenticate(auth_pb2.AuthRequest(username=username, password=password))
    
    print(f"status: {response.status}, message: {response.message}")

    return response.message

"""
returns true or false
"""
def validate(jwt: str):
    address = f"{HOST}:{PORT}"
    with grpc.insecure_channel(address) as channel:
        stub = auth_pb2_grpc.AuthenticateStub(channel)
        response = stub.validate(auth_pb2.JWTValidateRequest(jwt=jwt))

    print(f"{response.valid}")

    return response.valid

if __name__ == "__main__":
    jwt = login("test", "test")
    validate(jwt)