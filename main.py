from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from sqlalchemy.orm import Session

from routes.bank import bank

app = FastAPI(
    title="SmartFinance",
    description="A simple finance API using FastAPI and MySQL",
    version="0.1.0"
)

app.include_router(bank)