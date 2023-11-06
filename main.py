from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from sqlalchemy.orm import Session

from routes.bank import bank

app = FastAPI()

app.include_router(bank)