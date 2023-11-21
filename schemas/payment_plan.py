from pydantic import BaseModel, validator
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
    funding_amount: float  = 0.0
    total_periods: int   = 0.0
    changed_TE: float   = 0.0
    fixed_fee: float = 0.0
    desgravamen_percent_by_freq: float = 0.0
    vehicle_insurance_amount: float = 0.0
    physical_account_statement: bool = False
    VNA: float = 0.0
    TIR: float = 0.0
    TCEA: float = 0.0

    @validator('TEA', 'TNA', 'initial_fee_percent', 'changed_TE', 'desgravamen_percent_by_freq', pre=True)
    def validate_float_precision(cls, value):
        return round(value, 12)
        

