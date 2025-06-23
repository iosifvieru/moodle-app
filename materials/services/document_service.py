# Iosif Vieru 1409A
# 14.11.2024

from mongodb.database import collection
from fastapi import HTTPException
from mongodb.schemas import Material

def get_material_by_code(cod: int) -> dict | None:
    material = collection.find_one({'cod': cod})

    if material:
        material.pop("_id", None)
        return material
      
    else:
        return None

"""
Valideaza campul "probe_ponderi".

Suma ponderilor probelor trebuie sa fie 100%.
"""
def validare_probe_ponderi(lista: list[dict]):
    suma_ponderi: int = 0
    for proba in lista:
        for element in proba:
            if element == "pondere":
                try:
                    pondere: int = abs(int(proba[element]))
                    suma_ponderi = suma_ponderi + pondere
                except:
                    raise HTTPException(status_code=422, detail="Pondere must be an integer.")
    
    if suma_ponderi != 100:
        raise HTTPException(status_code=422, detail="Suma ponderi must equal 100.")

"""
Introduce / modifica un document in mongodb.
"""
def insert_material(material: Material):
    if material.cod <= 0:
        raise HTTPException(status_code=422, detail="Cod must be greater than 0.")
    
    if material.probe_ponderi is not None:
        validare_probe_ponderi(material.probe_ponderi)

    """
    Daca documentul nu exista in baza de date il creaza.
    """
    if collection.find_one({"cod": material.cod}):
        #raise HTTPException(status_code=409, detail="This document already exists in the database.")
        collection.replace_one({"cod": material.cod}, dict(material))

    # inserare in mongo db
    collection.insert_one(dict(material))

    return material

def delete_material(cod: int):
    if cod <= 0:
        raise HTTPException(status_code=422, detail="Cod must be greater than 0.")
    
    material = collection.find_one({"cod": cod})
    if not material:
        raise HTTPException(status_code=404, detail="No material found.")
    
    material.pop("_id", None)
    collection.delete_one({"cod": cod})
    return dict(material)