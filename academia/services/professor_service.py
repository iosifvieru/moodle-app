# Iosif Vieru 1409A
# 25.10.2024

from data.model import Profesor, Disciplina
from playhouse.shortcuts import model_to_dict
from data.schemas import ProfesorSchema
from fastapi import HTTPException

def get_all_professors_as_dict(page: int = 1, items_per_page: int = 10, 
                    acad_rank: str | None = None, name: str | None = None,
                    surname: str | None = None, affiliation: str | None = None) -> dict:
    
    professors = Profesor.select()
    total_items = professors.count()
    professors = professors.paginate(page, items_per_page)

    if acad_rank:
        professors = professors.where(Profesor.grad_didactic == acad_rank)

    if name:
        professors = professors.where(Profesor.nume.contains(name) | Profesor.prenume.contains(name))
    
    if surname:
        professors = professors.where(Profesor.nume.contains(surname) | Profesor.prenume.contains(surname))  

    if name and surname:
        professors = professors.where(Profesor.nume.contains(name) & Profesor.prenume.contains(surname))  

    if affiliation:
        professors = professors.where(Profesor.afiliere.contains(affiliation))

    if not professors.exists():
        return None
    
    message = dict()
    for index, professor in enumerate(professors):
        message[str(index)] = model_to_dict(professor)

    return message, total_items

# returns None if professor is not found, otherwise returns the value as a dict.
def get_professor_as_dict(id: int) -> dict:
    # select * from profesori where id=id;
    profesor = Profesor.get_or_none(id)

    if profesor is None:
        return None
    
    return model_to_dict(profesor)


def get_professor_lectures_as_dict(id: int) -> dict:
    # select * from disciplina.d where d.id_titular = id;
    query = (
        Disciplina.select().where(Disciplina.id_titular == id)
    )
    
    # returns none if query doesn t exists
    if not query.exists():
        return None

    # model to dict
    message = dict()
    for index, lecture in enumerate(query):
        message[str(index)] = model_to_dict(lecture, recurse=False)

    return message

def insert_professor_to_db(professor: ProfesorSchema):
    if Profesor.select().where(Profesor.email == professor.email).exists():
        raise HTTPException(status_code=409, detail="There is already a professor with this email.")

    prof = Profesor.create(
        nume = professor.nume,
        prenume = professor.prenume,
        email = professor.email,
        grad_didactic = professor.grad_didactic,
        tip_asociere = professor.tip_asociere,
        afiliere = professor.afiliere
    )
    return model_to_dict(prof, recurse=False)

def delete_professor_from_db(id: int):
    if not Profesor.select().where(Profesor.id == id).exists():
        raise HTTPException(status_code=404, detail="Professor not found.")
    
    profesor = Profesor.get_by_id(id)
    profesor.delete_instance()

    return model_to_dict(profesor)