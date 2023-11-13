from fastapi import APIRouter, HTTPException, status
from config.db import conn
from models.payment_plan import payment_plans
from models.bank import banks
import algorithms

from schemas.payment_plan import PaymentPlan
from typing import List


def check_bank_exists(bank_id: int):
    bank = conn.execute(banks.select().where(banks.c.id == bank_id)).first()
    if bank is None:
        return False
    return True

payment_plan = APIRouter()

@payment_plan.get(
    "/payment_plans", response_model=List[PaymentPlan], tags=["Payment Plans"]
)
def get_all_payment_plans():
    return conn.execute(payment_plans.select()).fetchall()


@payment_plan.post("/payment_plans", response_model=PaymentPlan, tags=["Payment Plans"])
def create_payment_plan(payment_plan: PaymentPlan):

    if payment_plan.vehicle_price <= 0.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle price cannot be zero or negative",
        )

    if not check_bank_exists(payment_plan.bank_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank ID does not exist in the database",
        )

    if payment_plan.TNA == 0.0 and payment_plan.TEA == 0.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TNA and TEA cannot be zero, fill one of them",
        )
    
    if payment_plan.TNA != 0.0 and payment_plan.TEA != 0.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TNA and TEA cannot be filled at the same time, fill only one of them",
        )
    
    if payment_plan.TNA != 0.0:
        TEA = algorithms.from_TNA_to_TEA(payment_plan.TNA)
        payment_plan.TEA = TEA

    new_payment_plan = {
        "name": payment_plan.name,
        "vehicle_price": payment_plan.vehicle_price,
        "initial_fee": payment_plan.initial_fee,
        "currency": payment_plan.currency,
        "anual_payment_periods": payment_plan.anual_payment_periods,
        "payment_frequency": payment_plan.payment_frequency,
        "parcial_grace_periods": payment_plan.parcial_grace_periods,
        "total_grace_periods": payment_plan.total_grace_periods,
        "TEA": payment_plan.TEA,
        "TNA": payment_plan.TNA,
        "bank_id": payment_plan.bank_id,
        "user_id": payment_plan.user_id,
    }
    result = conn.execute(payment_plans.insert().values(new_payment_plan))
    return conn.execute(
        payment_plans.select().where(payment_plans.c.id == result.lastrowid)
    ).first()


@payment_plan.get(
    "/payment_plans/{id}", response_model=PaymentPlan, tags=["Payment Plans"]
)
def get_payment_plan(id: int):
    payment_plan = conn.execute(
        payment_plans.select().where(payment_plans.c.id == id)
    ).first()
    if payment_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment Plan not found"
        )
    return payment_plan

@payment_plan.get("/payment_plans/user/{id}", response_model=List[PaymentPlan], tags=["Payment Plans"])
def get_payment_plan_by_user(id: int):
    payment_plan = conn.execute(
        payment_plans.select().where(payment_plans.c.user_id == id)
    ).fetchall()
    if payment_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment Plan not found"
        )
    return payment_plan

@payment_plan.get("/payment_plans/user/{user_id}/bank/{bank_id}", response_model=List[PaymentPlan], tags=["Payment Plans"])
def get_payment_plan_by_user_and_bank(user_id: int, bank_id: int):
    payment_plan = conn.execute(
        payment_plans.select().where(payment_plans.c.user_id == user_id).where(payment_plans.c.bank_id == bank_id)
    ).fetchall()
    if payment_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment Plan not found"
        )
    return payment_plan

@payment_plan.put(
    "/payment_plans/{id}", response_model=PaymentPlan, tags=["Payment Plans"]
)
def update_payment_plan(id: int, payment_plan: PaymentPlan):
    conn.execute(
        payment_plans.update()
        .where(payment_plans.c.id == id)
        .values(
            name=payment_plan.name,
            vehicle_price=payment_plan.vehicle_price,
            initial_fee=payment_plan.initial_fee,
            currency=payment_plan.currency,
            anual_payment_periods=payment_plan.anual_payment_periods,
            payment_frequency=payment_plan.payment_frequency,
            parcial_grace_periods=payment_plan.parcial_grace_periods,
            total_grace_periods=payment_plan.total_grace_periods,
            TEA=payment_plan.TEA,
            TNA=payment_plan.TNA,
            bank_id=payment_plan.bank_id,
            user_id=payment_plan.user_id,
        )
    )
    return conn.execute(payment_plans.select().where(payment_plans.c.id == id)).first()


@payment_plan.delete(
    "/payment_plans/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Payment Plans"],
)
def delete_payment_plan(id: int):
    deleted = conn.execute(payment_plans.delete().where(payment_plans.c.id == id))
    if deleted.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment Plan not found"
        )
    return {"message": "Payment Plan with id {} deleted successfully!".format(id)}

