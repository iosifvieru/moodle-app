# Iosif Vieru 1409A
# 25.10.2024

from data.model import Student, Join_DS
from playhouse.shortcuts import model_to_dict
from data.schemas import StudentSchema
from fastapi import HTTPException

def get_all_students_as_dict(
        page: int = 1, 
        items_per_page: int = 10,
        year: int | None = None, 
        type: str | None = None,
        name: str | None = None,
        surname: str | None = None
    ) -> dict:

    students = Student.select()
    total_items = students.count()
    students = students.paginate(page, items_per_page)

    if year:
        students = students.where(Student.an_studiu == year)

    if type:
        students = students.where(Student.ciclu_studii == type)

    if name:
        students = students.where(Student.nume.contains(name) | Student.prenume.contains(name))

    if surname:
        students = students.where(Student.nume.contains(surname) | Student.prenume.contains(surname));

    if name and surname:
        students = students.where(Student.nume.contains(name) & Student.prenume.contains(surname))
    
    if not students.exists():
        return None
    
    message = dict()
    for index, lecture in enumerate(students):
        message[str(index)] = model_to_dict(lecture)

    return message, total_items

def get_student_as_dict(id: int) -> dict:
    student = Student.get_or_none(id)

    if student is None:
        return None
    
    return model_to_dict(student, recurse=False)

def get_student_by_email(email: str) -> dict:
    student = Student.get_or_none(email)
    if student is None:
        return None
    
    return model_to_dict(student, recurse=False)

def get_student_lectures_as_dict(id: int) -> dict:
    lectures = Join_DS.select().where(Join_DS.studentID == id)

    if not lectures.exists():
        return None
    
    message = dict()
    for index, lecture in enumerate(lectures):
        message[str(index)] = model_to_dict(lecture, recurse=True)

    return message

def insert_student_to_db(student: StudentSchema):
    if Student.select().where(Student.email == student.email).exists():
        raise HTTPException(status_code=409, detail="There is already a student with this email.")

    user = Student.create(
        nume = student.nume,
        prenume = student.prenume,
        email = student.email,
        ciclu_studii = student.ciclu_studii,
        an_studiu = student.an_studiu,
        grupa = student.grupa
    )

    return model_to_dict(user)

def delete_student_from_db(id: int):
    if not Student.select().where(Student.id == id).exists():
        raise HTTPException(status_code=404, detail="Student not found.")
    
    student = Student.get_by_id(id)
    student.delete_instance()

    return model_to_dict(student)