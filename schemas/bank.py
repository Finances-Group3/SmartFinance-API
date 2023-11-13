from pydantic import BaseModel
from typing import Optional

class Bank(BaseModel):
    id: int
    name: str
    image_url: str
    porcentaje_seguro_desgravamen: float
    porcentaje_seguro_vehicular: float