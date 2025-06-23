# Iosif Vieru 1409A
# 25.10.2024

from fastapi import APIRouter, HTTPException, Request
from services.lecture_service import *
from utils import generate_hateoas_links, MAX_SIZE, validate_token
from data.schemas import DisciplinaSchema
import jwt

router = APIRouter()

"""
GET /api/academia/lectures

takes page, items_per_page, type and category as query parameters
returns a JSON of lectures
"""
@router.get("/api/academia/lectures")
async def get_lectures(
        request: Request,
        page: int = 1, 
        items_per_page: int = 10,
        type: str | None = None, 
        category: str | None = None,
    ):
    
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    checking every query parameter and validating them.
    raise 422 unprocessable entity if data not valid.
    """
    if page is not None and page < 0:
        raise HTTPException(status_code=422, detail="Page must be greater than 0.")
    
    if items_per_page is not None and items_per_page < 0:
        raise HTTPException(status_code=422, detail="Items_per_page must be greater than 0.")

    if type is not None and len(type) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Type length must NOT be greater than {MAX_SIZE}")

    if category is not None and len(category) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Category length must NOT be greater than {MAX_SIZE}")

    """
    returns the lectures from db as a dictionary.
    """
    lectures, total_items = get_all_lectures_as_dict(page=page, items_per_page=items_per_page,
                                        type=type, category=category)

    """
    raising 404 not found if no lectures were returned from database.
    """
    if not lectures:
        raise HTTPException(status_code=404, detail="Lectures not found.")
    
    """
    generating HATEOAS links
    """
    links = {
        "self": generate_hateoas_links(router, "get_lectures")
    }

    """ adding next and prev page """
    total_pages = (total_items + items_per_page - 1) // items_per_page
    if page < total_pages:
        links["next"] = generate_hateoas_links(router, "get_lectures", page=page + 1, items_per_page=items_per_page)

    if page > 1:
        links["prev"] = generate_hateoas_links(router, "get_lectures", page=page - 1, items_per_page=items_per_page)

    """
    returning all data. 200 OK
    """
    return {
        "lectures": lectures,
        "_links": links
    }


"""
GET /api/academia/lectures/{id}

returns a lecture as JSON based on id.
"""
@router.get("/api/academia/lectures/{id}")
async def get_lecture(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)
    
    """
    validating id parameter.
    """
    if id is not None and id < 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")

    """
    getting the lecture data from database.
    """
    lecture = get_lecture_as_dict(id)

    """
    404 NOT FOUND if lecture is not present in the database.
    """
    if lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found.")
    
    """
    generating HATEOAS links
    """
    links = {
        "self": generate_hateoas_links(router, "get_lecture", id=id),
        "parent": generate_hateoas_links(router, "get_lectures"),
    }

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    if(decoded_data['role'] == "admin"):
        links["delete"] = {"href": f"/api/academia/lectures/{id} DELETE"}
        links["post"] = {"href": f"/api/academia/lectures/{id} POST"}

    """
    200 OK
    """
    return {
        "lecture": lecture,
        "_links": links
    }

""" 
POST /api/academia/lectures/

INSERTS a new lecture in the database.
"""
@router.post("/api/academia/lectures")
async def insert_new_lecture(request: Request, lecture: DisciplinaSchema):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)

    """
    calling insert_lecture_to_db -> this function is raising HTTPException if conflict.
    """
    try:
        inserted_lecture = insert_lecture_to_db(lecture)
        """
        maybe hateoas links? -> for future me
        """
        return {
            "message": "Lecture inserted sucessfully!",
            "lecture": inserted_lecture
        }
    
    except HTTPException as exception:
        raise exception

"""
DELETE /api/academia/lectures/{cod}

deletes an entry from database
"""
@router.delete("/api/academia/lectures/{cod}")
async def delete_lecture(request: Request, cod: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)

    """
    checking if cod is not none or less than 0.
    """
    if cod is not None and cod <= 0:
        raise HTTPException(status_code=422, detail="Cod must be greater than 0.")

    try:
        """
        deleting the lecture
        """
        deleted_lecture = delete_lecture_from_db(cod)

        """
        generating HATEOS links
        """
        links = {
            "parent": generate_hateoas_links(router, "get_lectures")
        }

        """
        200 OK
        """
        return {
            "message": "Lecture deleted succesfully.",
            "lecture": deleted_lecture,
            "_links": links
        }

    except HTTPException as exception:
        raise exception

"""
PUT /api/academia/lectures/{cod}

Updates an existing lecture in the database.
"""
@router.put("/api/academia/lectures/{cod}")
async def update_lecture(request: Request, cod: int, lecture: DisciplinaSchema):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)

    """
    validating the cod parameter.
    """
    if cod is not None and cod <= 0:
        raise HTTPException(status_code=422, detail="Cod must be greater than 0.")

    """
    checking if lecture exists
    """
    existing_lecture = Disciplina.get_or_none(Disciplina.cod == cod)
    if existing_lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found.")

    """
    updating the lecture
    """
    try:
        existing_lecture.cod = int(lecture.cod)
        existing_lecture.id_titular = int(lecture.id_titular)
        existing_lecture.nume_disciplina = str(lecture.nume_disciplina)
        existing_lecture.an_studiu = int(lecture.an_studiu)
        existing_lecture.tip_disciplina = str(lecture.tip_disciplina)
        existing_lecture.categorie_disciplina = str(lecture.categorie_disciplina)
        existing_lecture.tip_examinare = str(lecture.tip_examinare)

        """
        save the updated lecture
        """
        existing_lecture.save()

        """
        generate HATEOAS links
        """
        links = {
            "self": generate_hateoas_links(router, "update_lecture", cod=cod),
            "parent": generate_hateoas_links(router, "get_lectures"),
        }

        """
        return the updated lecture
        """
        return {
            "message": "Lecture updated successfully.",
            "lecture": model_to_dict(existing_lecture),
            "_links": links,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update lecture. Error: {e}")
