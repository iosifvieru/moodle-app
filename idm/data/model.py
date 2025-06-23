# Iosif Vieru
# 5.12.2024

from peewee import (
    Model, CharField, AutoField
)

from data.database import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField(primary_key=True)
    email = CharField(max_length=255, unique=True)
    parola = CharField(max_length=255, null=False)
    rol = CharField(
        choices=[(0, 'admin'), (1, 'profesor'), (2, 'student')],
        max_length=20,
        null=False
    )

    class Meta:
        db_table = "users"

def create_database():
    db.connect()
    db.create_tables([User], safe=True)

create_database()