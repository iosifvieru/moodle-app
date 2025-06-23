# Iosif Vieru
# 14.11.2024

from fastapi import APIRouter, HTTPException, Request, File, UploadFile, Form
from services.document_service import *
from mongodb.schemas import Material
from utils import validate_token
import jwt
import os
from uuid import uuid4

router = APIRouter()

UPLOAD_FOLDER = "./uploads"

@router.get("/api/materials/{cod}")
async def get_lecture_materials(request: Request, cod: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    if cod is None or cod <= 0:
        raise HTTPException(status_code=422, detail="Cod must be greater than 0.")
    
    material = get_material_by_code(cod)

    if material is None:
        raise HTTPException(status_code=404, detail=f"Nu am gasit materiale pentru disciplina cu codul {cod}!")
    return material

@router.put("/api/materials")
async def insert_lecture_material(request: Request, material: Material):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'profesor'):
        raise HTTPException(status_code=403)

    try:
        return insert_material(material)
    except HTTPException as e:
        raise e
    
@router.delete("/api/materials/{cod}")
async def delete_lecture_material(request: Request, cod: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)
    
    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'profesor'):
        raise HTTPException(status_code=403)

    try:
        return {
            "message": "Stergere cu succes.",
            "material": delete_material(cod)
        }
    except HTTPException as e:
        raise e


@router.post("/api/materials/upload")
async def upload_material_files(
    request: Request,
    cod: int = Form(...),
    materiale_curs: list[UploadFile] = File(default=[]),
    materiale_laborator: list[UploadFile] = File(default=[])
):
    """Handle file uploads for lecture materials."""
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    if decoded_data['role'] != 'profesor':
        raise HTTPException(status_code=403)

    material = get_material_by_code(cod)
    if not material:
        #raise HTTPException(status_code=404, detail=f"No material found for cod {cod}.")
        insert_material(Material(cod=cod))

    uploaded_files = {
        "materiale_curs": [],
        "materiale_laborator": []
    }

    try:
        for file in materiale_curs:
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            uploaded_files["materiale_curs"].append(file_path)

        for file in materiale_laborator:
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)

            uploaded_files["materiale_laborator"].append(file_path)

        updated_material = {
            "materiale_curs": uploaded_files["materiale_curs"],
            "materiale_laborator": uploaded_files["materiale_laborator"]
        }
        collection.update_one({"cod": cod}, {"$set": updated_material})

        return {
            "message": "Files uploaded successfully.",
            "uploaded_files": uploaded_files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

