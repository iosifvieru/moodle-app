# study-database-service
# Iosif Vieru 1409A
# 20.10.2024

from fastapi import FastAPI
from controllers import (
    professor_controller, lecture_controller, student_controller
)
from fastapi.middleware.cors import CORSMiddleware

# fastapi instance
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(professor_controller.router)
app.include_router(lecture_controller.router)
app.include_router(student_controller.router)

# "/" route
@app.get("/")
async def home():
    return {"message: hello world!"}