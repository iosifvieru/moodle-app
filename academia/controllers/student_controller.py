# Iosif Vieru 1409A
# 25.10.2024

from fastapi import APIRouter, HTTPException, Request
from services.student_service import *
from data.schemas import StudentSchema
from utils import generate_hateoas_links, MAX_SIZE, validate_token
import jwt

router = APIRouter()

"""
GET /api/academia/students

accepts page, items_per_page, year, type, name as query parameters.
returns a JSON of students.
"""
@router.get("/api/academia/students")
async def get_students(
        request: Request,
        page: int = 1, 
        items_per_page: int = 10,
        year: int | None = None, 
        type: str | None = None,
        name: str | None = None,
        surname: str | None = None
    ):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    checking every query, if data is invalid -> 422 unprocessable entity
    """
    if page is not None and page < 0:
        raise HTTPException(status_code=422, detail="Page must be greater than 0.")
    
    if items_per_page is not None and items_per_page < 0:
        raise HTTPException(status_code=422, detail="Items_per_page must be greater than 0.")

    if year is not None and year < 0:
        raise HTTPException(status_code=422, detail="Year must be greater than 0.")

    if type is not None and len(type) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Type length must not be greater than {MAX_SIZE}.")

    if name is not None and len(name) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Name length must not be greater than {MAX_SIZE}.")
    
    if surname is not None and len(name) > MAX_SIZE:
        raise HTTPException(status_code=422, detail=f"Surname length must not be greater than {MAX_SIZE}.")

    students, total_items = get_all_students_as_dict(page=page, items_per_page=items_per_page,
                                        year=year, type=type, name=name, surname=surname)

    if students is None:
        raise HTTPException(status_code=404, detail="Students not found.")
    
    links = {
        "self": generate_hateoas_links(router, "get_students", 
                                       page=page,
                                       items_per_page=items_per_page,
                                       year=year,
                                       type=type,
                                       name=name),
        "parent": generate_hateoas_links(router, "get_students"),
    }

    for student in students.values():
        student["_links"] = {
            "self": generate_hateoas_links(router, "get_student", id=student["id"]),
            "parent": generate_hateoas_links(router, "get_students"),
            "lectures": {"href": f"/api/academia/students/{student['id']}/lectures"}
        }


    """ adding next and prev page """
    total_pages = (total_items + items_per_page - 1) // items_per_page
    if page < total_pages:
        links["next"] = generate_hateoas_links(router, "get_students", page=page + 1, items_per_page=items_per_page)

    if page > 1:
        links["prev"] = generate_hateoas_links(router, "get_students", page=page - 1, items_per_page=items_per_page)
    
    return {
        "students": students,
        "_links": links
    }

"""
GET /api/academia/students/{id}

returns a student as JSON based on the id parameter.
"""
@router.get("/api/academia/students/{id}", name="get_student")
async def get_student(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    if id < 0 -> 422 unprocessable entity.
    """
    if id is not None and id < 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")
    
    student = get_student_as_dict(id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    
    links = {
        "self": generate_hateoas_links(router, "get_student", id=id),
        "parent": generate_hateoas_links(router, "get_students"),
        "lectures": generate_hateoas_links(router, "get_student_lectures", id=id)
    }

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    if(decoded_data['role'] == "admin"):
        links["delete"] = {"href": f"/api/academia/student/{id} DELETE"}
        links["post"] = {"href": f"/api/academia/student/{id} POST"}

    return {
        "student": student,
        "_links": links
    }

"""
GET /api/academia/students/{id}/lectures

returns the lectures of a student based on id as JSON
"""
@router.get("/api/academia/students/{id}/lectures", name="get_student_lectures")
async def get_student_lectures(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    """
    if id < 0 -> 422 unprocessable entity.
    """
    if id is not None and id < 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")

    lectures = get_student_lectures_as_dict(id)

    if lectures is None:
        raise HTTPException(status_code=404, detail="Lectures not found.")

    links = {
        "self": generate_hateoas_links(router, "get_student_lectures", id=id),
        "parent": generate_hateoas_links(router, "get_student", id=id)
    }

    return {
        "lectures": lectures,
        "_links": links
    }

"""
POST /api/academia/students

INSERT a new student in the database.
"""
@router.post("/api/academia/students")
async def insert_student(request: Request, student: StudentSchema):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)

    try:
        insert_student = insert_student_to_db(student)
        return insert_student
    except HTTPException as exception:
        raise exception

"""
DELETE /api/academia/students/{id}

DELETES a student from the database.
"""
@router.delete("/api/academia/students/{id}")
async def delete_student(request: Request, id: int):
    """ validating the token """
    authorization: str = request.headers.get("Authorization")
    validate_token(authorization)

    decoded_data = jwt.decode(authorization.split(" ")[1], options={"verify_signature": False})
    print(decoded_data['role'])

    if(decoded_data['role'] != 'admin'):
        raise HTTPException(status_code=403)
    
    if id is not None and id <= 0:
        raise HTTPException(status_code=422, detail="ID must be greater than 0.")
    
    try:
        deleted_student = delete_student_from_db(id)

        links = {
            "parent": generate_hateoas_links(router, "get_students")
        }

        return {
            "message": "Student deleted succesfully.",
            "student": deleted_student,
            "_links": links
        }

    except HTTPException as exception:
        raise exception
