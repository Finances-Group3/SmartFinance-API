from pydantic import BaseModel
from typing import Optional
from enums.curency_enum import CurrencyEnum
from sqlalchemy.orm import relationship
from enums.payment_frequency import PaymentFrequencyEnum 

class PaymentPlan(BaseModel):
    id: int
    name: str
    vehicle_price: float
    initial_fee: float
    currency: CurrencyEnum = CurrencyEnum.PEN
    anual_payment_periods: int
    payment_frequency: PaymentFrequencyEnum = PaymentFrequencyEnum.MENSUAL
    parcial_grace_periods: int
    total_grace_periods:int
    TEA: float = 0.0
    TNA: float = 0.0
    bank_id: int
    user_id: int
    funding_amount: float
    total_periods: int
    changed_TEA: float
    fixed_fee: float
    desgravamen_insurance: float
    vehicle_insurance: float


class payment_detail:
    cuota_fija: float
    interes: float
    pago_seguro_desgravamen: float
    pago_seguro_vehicular: float
    amortizacion: float
    saldo: float