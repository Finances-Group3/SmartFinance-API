from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine

from sqlalchemy import Enum

from enums.payment_frequency import PaymentFrequencyEnum

payment_plans = Table(
    "payment_plans",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("vehicle_price", Float),
    Column("initial_fee_percent", Float),
    Column("currency", String(5)),
    Column("anual_payment_periods", Integer),
    Column("payment_frequency", Enum(PaymentFrequencyEnum), nullable=False),
    Column("parcial_grace_periods", Integer),
    Column("total_grace_periods", Integer),
    Column("TEA", Float, default=0.0),
    Column("TNA", Float, default=0.0),
    Column("bank_id", Integer, ForeignKey("banks.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("funding_amount", Float),
    Column("total_periods", Integer),
    Column("changed_TE", Float),
    Column("fixed_fee", Float),
    Column("desgravamen_percent_by_freq", Float),
    Column("vehicle_insurance_amount", Float),
    Column("physical_account_statement", Integer, default=0),
)

meta.create_all(engine)