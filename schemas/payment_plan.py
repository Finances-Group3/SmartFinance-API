from pydantic import BaseModel
from typing import Optional
from enums.curency_enum import CurrencyEnum
from sqlalchemy.orm import relationship

class PaymentPlan(BaseModel):
    id: int
    name: str
    vehicle_price: float
    initial_fee: float
    currency: CurrencyEnum = CurrencyEnum.PEN
    payment_periods: int
    parcial_grace_periods: int
    total_grace_periods:int
    TEA: float = 0.0
    TNA: float = 0.0
    bank_id: int
    user_id: int
