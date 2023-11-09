from pydantic import BaseModel
from typing import Optional
from enum import Enum
from sqlalchemy.orm import relationship

class PaymentPlan(BaseModel):
    id: int
    name: str
    vehicle_price: float
    initial_fee: float

    # no se si agregar su propio modelo aa currency
    currency: str 
    payment_periods: int
    parcial_grace_periods: int
    total_grace_periods:int
    TEA: float = 0.0
    TNA: float = 0.0
    bank_id: int
    user_id: int
