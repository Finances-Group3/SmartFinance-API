from enum import Enum

class PaymentFrequencyEnum(int, Enum):
    MENSUAL = 1
    BIMESTRAL = 2
    TRIMESTRAL = 3
    CUATRIMESTRAL = 4
    SEMESTRAL = 6
    ANUAL = 12