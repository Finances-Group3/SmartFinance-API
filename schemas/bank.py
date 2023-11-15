from pydantic import BaseModel
from typing import Optional

class Bank(BaseModel):
    id: int
    name: str
    image_url: str
    TEA: float
    anual_desgravamen_insurance_percent: float
    anual_vehicle_insurance_percent: float
    oficial_page : str