import logging
from fastapi import APIRouter, HTTPException, status
from config.db import conn
from models.bank import banks
from schemas.bank import Bank
from typing import List

bank = APIRouter()

@bank.get("/banks", response_model=List[Bank], tags=["Banks"])
def get_all_banks():
    try:
        with conn.begin() as transaction:
            result = conn.execute(banks.select()).fetchall()
        return result or []  # Devuelve una lista vacía si result es None
    except Exception as e:
        # Log the error
        logging.error(f"An unhandled error occurred: {e}")
        conn.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@bank.post("/banks", response_model=Bank, tags=["Banks"])
def create_bank(bank: Bank):
    try:
        with conn.begin() as transaction:
            new_bank = {
                "name": bank.name,
                "image_url": bank.image_url,
                "TEA": bank.TEA,
                "portes": bank.portes,
                "anual_desgravamen_insurance_percent": bank.anual_desgravamen_insurance_percent,
                "anual_vehicle_insurance_percent": bank.anual_vehicle_insurance_percent,
                "oficial_page": bank.oficial_page,
                "TEA_USD": bank.TEA_USD,
            }
            result = conn.execute(banks.insert().values(new_bank))
            created_bank = conn.execute(banks.select().where(banks.c.id == result.lastrowid)).first()
        return created_bank
    except Exception as e:
        # Log the error
        logging.error(f"An unhandled error occurred: {e}")
        conn.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@bank.get("/banks/{id}", response_model=Bank, tags=["Banks"])
def get_bank(id: int):
    try:
        bank = conn.execute(banks.select().where(banks.c.id == id)).first()
        if bank is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found"
            )
        return bank
    except Exception as e:
        # Log the error
        logging.error(f"An unhandled error occurred: {e}")
        conn.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@bank.put("/banks/{id}", response_model=Bank, tags=["Banks"])
def update_bank(id: int, bank: Bank):
    try:
        with conn.begin() as transaction:
            conn.execute(
                banks.update()
                .where(banks.c.id == id)
                .values(
                    name=bank.name,
                    image_url=bank.image_url,
                    TEA=bank.TEA,
                    portes=bank.portes,
                    anual_desgravamen_insurance_percent=bank.anual_desgravamen_insurance_percent,
                    anual_vehicle_insurance_percent=bank.anual_vehicle_insurance_percent,
                    oficial_page=bank.oficial_page,
                    TEA_USD=bank.TEA_USD,
                )
            )
            updated_bank = conn.execute(banks.select().where(banks.c.id == id)).first()
        return updated_bank
    except Exception as e:
        # Log the error
        logging.error(f"An unhandled error occurred: {e}")
        conn.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail="Internal Server Error")

@bank.delete("/banks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Banks"])
def delete_bank(id: int):
    try:
        with conn.begin() as transaction:
            deleted = conn.execute(banks.delete().where(banks.c.id == id))
            if deleted.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found"
                )
    except Exception as e:
        # Log the error
        logging.error(f"An unhandled error occurred: {e}")
        conn.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"message": "Bank with id {} deleted successfully!".format(id)}
