
from fastapi import APIRouter, HTTPException
from idm_client import validate


def validate_token(jwt: str):
    if jwt is None:
        raise HTTPException(status_code=401, detail="Invalid authorization.")

    if jwt:
        parts = jwt.split(" ")
        bearer = parts[0]
        token = parts[1]

        if validate(token) == False:
            raise HTTPException(status_code=401, detail="Invalid authorization.")
