# Iosif Vieru 1409A
# 25.10.2024

from data.model import Disciplina
from playhouse.shortcuts import model_to_dict
from data.schemas import DisciplinaSchema
from fastapi import HTTPException

"""
makes a call to db to get lectures based on the arguments.
"""
def get_all_lectures_as_dict(
        page: int = 1, 
        items_per_page: int = 10,
        type: str | None = None, 
        category: str | None = None) -> dict:
    
    """ 
    select * from db.
    """
    lectures = Disciplina.select()
    total_items = lectures.count()
    lectures = lectures.paginate(page, items_per_page)

    """
    filters the results on type if present
    """
    if type:
        lectures = lectures.where(Disciplina.tip_disciplina == type)
    
    """
    filters the results on category if present
    """
    if category:
        lectures = lectures.where(Disciplina.tip_examinare == category)
    
    """
    returns none if there is no lecture
    """
    if not lectures.exists():
        return None
    
    """
    makes a dict out of all results and returns
    """
    message = dict()
    for index, lecture in enumerate(lectures):
        message[str(index)] = model_to_dict(lecture, recurse=False)

    return message, total_items

# returns None if lecture is not found, otherwise returns the value as a dict.
def get_lecture_as_dict(id: int) -> dict:
    lecture = Disciplina.get_or_none(id)

    if lecture is None:
        return None
    
    return model_to_dict(lecture, recurse=False)

"""
inserts a lecture in database
"""
def insert_lecture_to_db(lecture: DisciplinaSchema):
    if Disciplina.select().where(Disciplina.cod == lecture.cod).exists():
        raise HTTPException(status_code=409, detail="There is already a lecture with this code.")
    
    new_lecture = Disciplina.create(
        cod = int(lecture.cod),
        id_titular = int(lecture.id_titular),
        nume_disciplina = str(lecture.nume_disciplina),
        an_studiu = int(lecture.an_studiu),
        tip_disciplina = str(lecture.tip_disciplina),
        categorie_disciplina = str(lecture.categorie_disciplina),
        tip_examinare = str(lecture.tip_examinare)
    )
        
    return model_to_dict(new_lecture)

"""
deletes a lecture from database
"""
def delete_lecture_from_db(cod: int):
    """
    raising 404 if no lecture is found.
    """
    if not Disciplina.select().where(Disciplina.cod == cod).exists():
        raise HTTPException(status_code=404, detail="No lecture found.")
    
    """
    deletes the actual stuff
    """
    lecture = Disciplina.get_by_id(cod)
    lecture.delete_instance()

    """
    returns the deleted instance
    """
    return model_to_dict(lecture, recurse=False)