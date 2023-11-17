from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from routes.bank import bank
from routes.user import user
from routes.payment_plan import payment_plan

app = FastAPI(
    title="SmartFinance",
    description="A simple finance API using FastAPI and MySQL",
    version="0.1.0"
)

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bank)
app.include_router(user)
app.include_router(payment_plan)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

