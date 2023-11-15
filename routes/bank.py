from fastapi import APIRouter, HTTPException, status
from config.db import conn
from models.bank import banks
from schemas.bank import Bank
from typing import List

bank = APIRouter()


@bank.get("/banks", response_model=List[Bank], tags=["Banks"])
def get_all_banks():
    return conn.execute(banks.select()).fetchall()


@bank.post("/banks", response_model=Bank, tags=["Banks"])
def create_bank(bank: Bank):
    new_bank = {
        "name": bank.name,
        "image_url": bank.image_url,
        "TEA": bank.TEA,
        "portes": bank.portes,
        "anual_desgravamen_insurance_percent": bank.anual_desgravamen_insurance_percent,
        "anual_vehicle_insurance_percent": bank.anual_vehicle_insurance_percent,
        "oficial_page": bank.oficial_page,
    }
    result = conn.execute(banks.insert().values(new_bank))
    return conn.execute(banks.select().where(banks.c.id == result.lastrowid)).first()


@bank.get("/banks/{id}", response_model=Bank, tags=["Banks"])
def get_bank(id: int):
    bank = conn.execute(banks.select().where(banks.c.id == id)).first()
    if bank is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found"
        )
    return bank


@bank.put("/banks/{id}", response_model=Bank, tags=["Banks"])
def update_bank(id: int, bank: Bank):
    conn.execute(
        banks.update().where(banks.c.id == id).values(
            name=bank.name,
            image_url=bank.image_url,
            TEA=bank.TEA,
            portes=bank.portes,
            anual_desgravamen_insurance_percent=bank.anual_desgravamen_insurance_percent,
            anual_vehicle_insurance_percent=bank.anual_vehicle_insurance_percent,
            oficial_page=bank.oficial_page,
        )
    )
    return conn.execute(banks.select().where(banks.c.id == id)).first()


@bank.delete("/banks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Banks"])
def delete_bank(id: int):
    deleted = conn.execute(banks.delete().where(banks.c.id == id))
    if deleted.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found"
        )
    return {"message": "Bank with id {} deleted successfully!".format(id)}
