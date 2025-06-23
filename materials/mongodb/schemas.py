
from pydantic import BaseModel
from typing import Optional

class Material(BaseModel):
    cod: int
    probe_ponderi:  Optional[list] = None
    materiale_curs: Optional[list] = None
    materiale_laborator: Optional[list] = None