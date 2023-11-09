from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

from routes.bank import bank
from routes.user import user
from routes.payment_plan import payment_plan

app = FastAPI(
    title="SmartFinance",
    description="A simple finance API using FastAPI and MySQL",
    version="0.1.0"
)

app.include_router(bank)
app.include_router(user)
app.include_router(payment_plan)


