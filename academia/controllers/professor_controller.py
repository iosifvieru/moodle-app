# Iosif Vieru 1409A
# 25.10.2024

from fastapi import APIRouter, HTTPException, Request
from services.professor_service import *
from utils import MAX_SIZE, generate_hateoas_links, validate_token
from data.schemas import ProfesorSchema
import jwt

router = APIRouter()

"""
GET /api/academia/professors
returns a dict with all the professors from database based on query arguments
"""
@router.get("/api/academia/professors")
async def get_professors(
        request: Request,
        page: int = 1, 
        items_per_page: int = 10, 
        acad_rank: str | None = None, 
        name: str | None = None,
        surname: str | None = None,
        affiliation: str | None = None
    ):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    checks every query and makes sure everything is ok :)
    """
    if page is not None and page <= 0:
        raise HTTPException(status_code=422, detail="Page must be greater than 0.")
    
    if items_per_page is not None and items_per_page < 0:
        raise HTTPException(status_code=422, detail="Items per page must be greater than 0.")
    
    if acad_rank is not None and len(acad_rank) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Academy rank length must NOT be greater than {MAX_SIZE}")

    if name is not None and len(name) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Name length must NOT be greater than {MAX_SIZE}")

    if surname is not None and len(surname) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Surname length must NOT be greater than {MAX_SIZE}")

    if affiliation is not None and len(affiliation) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Affiliation must not be greater than {MAX_SIZE}")

    """
    calling service to get all the professors from db
    """
    professors, total_items = get_all_professors_as_dict(page=page, items_per_page=items_per_page, 
                                            acad_rank=acad_rank, name=name,
                                            affiliation=affiliation)
    """
    raising 404 if none is found
    """
    if not professors:
        raise HTTPException(status_code=404, detail="No professors.")

    """
    generates HATEOAS links
    """
    links = {
        "self": generate_hateoas_links(router, "get_professors")
    }

    """ adding next and prev page """
    total_pages = (total_items + items_per_page - 1) // items_per_page
    if page < total_pages:
        links["next"] = generate_hateoas_links(router, "get_professors", page=page + 1, items_per_page=items_per_page)

    if page > 1:
        links["prev"] = generate_hateoas_links(router, "get_professors", page=page - 1, items_per_page=items_per_page)


    for profesor in professors.values():
        profesor["_links"] = {
            "self": generate_hateoas_links(router, "get_professors", id=profesor["id"]),
            "parent": generate_hateoas_links(router, "get_professors"),
            "lectures": {"href": f"/api/academia/professors/{profesor['id']}/lectures"}
        }

    """
    200 OK
    """
    return {
        "professors": professors,
        "_links": links
    }

"""
GET /api/academia/professors/{id}

returns the professor with that id.
"""
@router.get("/api/academia/professors/{id}")
async def get_professor(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    422 Unprocessable entity if id <= 0
    """
    if id is not None and id <= 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")

    profesor = get_professor_as_dict(id)

    """ 
    404 Not found none in db
    """
    if not profesor:
        raise HTTPException(status_code=404, detail="Professor not found.")

    """
    generating HATEOAS links
    """
    links = {
        "self": generate_hateoas_links(router, "get_professor", id=id),
        "parent": generate_hateoas_links(router, "get_professors"),
        "lectures": generate_hateoas_links(router, "get_professor_lectures", id=id)
    }

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    if(decoded_data['role'] == "admin"):
        links["delete"] = {"href": f"/api/academia/professors/{id} DELETE"}
        links["post"] = {"href": f"/api/academia/professors/{id} POST"}

    """ 
    200 OK
    """
    return {
        "profesor": profesor,
        "_links": links
    }

"""
GET /api/academia/professors/{id}/lectures
"""
@router.get("/api/academia/professors/{id}/lectures")
async def get_professor_lectures(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    422 Unprocessable Entity if id <= 0
    """
    if id is not None and id <= 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")

    lectures = get_professor_lectures_as_dict(id)

    """
    404 not found if no professor is found
    """
    if lectures is None:
        raise HTTPException(status_code=404, detail="No lecture found.")

    """
    generating HATEOAS links
    """
    links = {
        "self": generate_hateoas_links(router, "get_professor_lectures", id=id),
        "parent": generate_hateoas_links(router, "get_professor", id=id)
    }

    """
    200 OK
    """
    return {
        "lectures": lectures,
        "_links": links
    }

"""
POST

INSERT a professor in DB.
"""
@router.post("/api/academia/professors")
async def insert_professor(request: Request, profesor: ProfesorSchema):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)

    try:
        inserted_professor = insert_professor_to_db(profesor)
        return inserted_professor
    except HTTPException as exception:
        raise exception

"""
DELETE

Deletes a professor db
"""
@router.delete("/api/academia/professors/{id}")
async def delete_professor(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)

    """
    422 Unprocessable entity if id <= 0.
    """
    if id is not None and id <= 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")
    
    try:
        deleted_professor = delete_professor_from_db(id)

        links = {
            "parent": generate_hateoas_links(router, "get_professors")
        }

        return {
            "message": "Professor deleted succesfully.",
            "student": deleted_professor,
            "_links": links
        }

    except HTTPException as exception:
        raise exception
