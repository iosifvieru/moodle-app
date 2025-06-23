# Iosif Vieru 1409A
# 24.10.2024

from peewee import (
    Model, IntegerField, CharField, ForeignKeyField, CompositeKey, AutoField
)

from data.database import db

class BaseModel(Model):
    class Meta:
        database = db

class Profesor(BaseModel):
    #id = IntegerField(primary_key=True)
    id = AutoField()
    nume = CharField(max_length=255, null=False)
    prenume = CharField(max_length=255, null=False)
    email = CharField(max_length=255, unique=True, null=False)
    grad_didactic = CharField(
        choices=[(0, 'asist'), (1, 'sef lucr'), (2, 'conf'), (3, 'prof')],
        max_length=20
    )
    tip_asociere = CharField(
        choices=[(0, "titular"), (1, "asociat"), (2, "extern")],
        unique=False
    )
    afiliere = CharField(max_length=255)

    class Meta:
        db_table = "profesori"

class Student(BaseModel):
    #id = IntegerField(primary_key=True)
    id = AutoField()
    nume = CharField(max_length=255, null=False)
    prenume = CharField(max_length=255, null=False)
    email = CharField(max_length=255, unique=True)
    ciclu_studii = CharField(
        choices=[(0, "licenta"), (1, "master")],
        null=False
    )
    an_studiu = IntegerField(null=False)
    grupa = IntegerField(null=False)
    
    class Meta:
        db_table = "studenti"

class Disciplina(BaseModel):
    cod = IntegerField(primary_key=True)
    id_titular = ForeignKeyField(
        Profesor, 
        backref='discipline', 
        on_delete='CASCADE',
        column_name='id_titular')
    nume_disciplina = CharField(max_length=255, null=False)
    an_studiu = IntegerField(null=False)
    tip_disciplina = CharField(
        choices=[(0, 'impusa'), (1, 'optionala'), (2, 'liber_aleasa')],
        null=False
    )
    categorie_disciplina = CharField(
        choices=[(0, 'domeniu'), (1, 'specialitate'), (2, 'adiacenta')],
        null=False
    )
    tip_examinare = CharField(
        choices=[(0, 'examen'), (1, 'colocviu')],
        null=False
    )
    
    class Meta:
        db_table = "discipline"

class Join_DS(BaseModel):
    disciplinaID = ForeignKeyField(
            Disciplina, 
            backref='studenti', 
            on_delete='CASCADE',
            column_name='disciplinaID'
        )
    studentID = ForeignKeyField(
            Student, 
            backref='discipline', 
            on_delete='CASCADE',
            column_name='studentID'
        )
    class Meta:
        primary_key = CompositeKey('disciplinaID', 'studentID')
        db_table = "join_ds"

def create_database():
    db.connect()
    db.create_tables([Student, Profesor, Disciplina, Join_DS], safe=True)

create_database()