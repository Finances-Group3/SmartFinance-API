from enum import Enum
from pydantic import BaseModel

class CurrencyEnum(str, Enum):
    USD = "USD"
    PEN = "PEN"