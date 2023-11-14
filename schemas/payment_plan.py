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
    funding_amount: float
    total_periods: int # total_periods = anual_payment_periods * 12/payment_frequency
    changed_TE: float 
    fixed_fee: float
    desgravamen_percent_by_freq: float = 0.0
    vehicle_insurance_amount: float

    @validator('TEA', 'TNA', 'initial_fee_percent', 'changed_TE', 'desgravamen_percent_by_freq', pre=True)
    def validate_float_precision(cls, value):
        return round(value, 12)
        

class PaymentDetail:
    def __init__(
        self,
        nro_cuota,
        saldo_inicial,
        interes,
        cuota_fija,
        amortizacion,
        pago_seguro_desgravamen,
        pago_seguro_vehicular,
        portes,
        saldo_final,
        flujo,
    ):
        self.nro_cuota = nro_cuota
        self.saldo_inicial = saldo_inicial
        self.interes = interes
        self.cuota_fija = cuota_fija
        self.amortizacion = amortizacion
        self.pago_seguro_desgravamen = pago_seguro_desgravamen
        self.pago_seguro_vehicular = pago_seguro_vehicular
        self.portes = portes
        self.saldo_final = saldo_final
        self.flujo = flujo


