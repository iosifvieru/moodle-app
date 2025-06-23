"""
scuzati neprofesionalismul acestui api... :(
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from idm_client import login, invalidate
from fastapi.middleware.cors import CORSMiddleware

"""
schemas for api
"""
class LoginSchema(BaseModel):
    email: str
    password: str

class LogoutSchema(BaseModel):
    jwt: str

"""
api instance
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" routes """
@app.get("/")
async def index():
    return "da... functionez"

@app.post("/login")
async def login_api(login_data: LoginSchema):
    response = login(login_data.email, login_data.password)
    if(response["status"] == "OK"):
        return {
            "status": response["status"],
            "message": response["message"]
        }
    else:
        raise HTTPException(status_code=404, detail=response["message"])

@app.post("/logout")
async def logout_api(jwt: str):
    response = invalidate(jwt)
    return response.deleted