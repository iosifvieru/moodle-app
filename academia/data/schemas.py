# Iosif Vieru
# 1.11.2024

from pydantic import BaseModel
from typing import Optional

# pydantic models -> ensures that the incoming data conforms to the expected schema

# student
class StudentSchema(BaseModel):
    id: Optional[int] = None
    nume: str
    prenume: str
    email: str
    ciclu_studii: str
    an_studiu: int
    grupa: int

# lecture
class DisciplinaSchema(BaseModel):
    cod: int
    id_titular: int
    nume_disciplina: str
    an_studiu: int
    tip_disciplina: str
    categorie_disciplina: str
    tip_examinare: str

# professor
class ProfesorSchema(BaseModel):
    id: Optional[int] = None
    nume: str
    prenume: str
    email: str
    grad_didactic: str
    tip_asociere: str
    afiliere: str

# join_ds schema
class Join_DSSchema(BaseModel):
    disciplinaID: int
    studentID: int