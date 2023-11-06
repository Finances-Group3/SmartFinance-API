from pydantic import BaseModel
from typing import Optional

class Bank(BaseModel):
    id: int
    name: str