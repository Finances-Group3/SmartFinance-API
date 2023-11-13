from pydantic import BaseModel, validator
from typing import Optional
from enums.curency_enum import CurrencyEnum
from enums.payment_frequency import PaymentFrequencyEnum 

class PaymentPlan(BaseModel):
    id: int
    name: str
    vehicle_price: float
    initial_fee_percent: float
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
    total_periods: int # total_periods = anual_payment_periods * 12/payment_frequency
    changed_TE: float 
    fixed_fee: float
    desgravamen_percent_by_freq: float = 0.0
    desgravamen_insurance_amount: float
    vehicle_insurance_amount: float

    @validator('TEA', 'TNA', 'initial_fee_percent', 'changed_TE', 'desgravamen_percent_by_freq', pre=True)
    def validate_float_precision(cls, value):
        return round(value, 12)
      
            


class payment_detail:
    cuota_fija: float
    interes: float
    pago_seguro_desgravamen: float
    pago_seguro_vehicular: float
    amortizacion: float
    saldo: float