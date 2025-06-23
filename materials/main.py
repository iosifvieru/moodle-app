# Iosif Vieru
# 1409A

from mongodb.database import db
from fastapi import FastAPI
from controllers import document_controller
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mongodb.database import collection
import os

app = FastAPI()

app.include_router(document_controller.router)

UPLOAD_FOLDER = "./uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

exemplu_document_db = {
    "cod": 1,
    "probe_ponderi": [
        {
            "nume_proba": "Laborator",
            "pondere": 30
        }
        # ...
    ],
    "materiale_curs": [
        {
            "nume_fisier": "curs 1",
            "link": "/path/catre/fisier"
        }
        # ...
    ],
    "materiale_laborator": [
        {
            "nume_fisier": "laborator 1",
            "link": "/path/catre/fisier"
        }
        # ...
    ]
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"message": "Hello world!"}