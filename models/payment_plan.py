from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine


payment_plans = Table(
    "payment_plans",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("vehicle_price", Float),
    Column("initial_fee", Float),
    Column("currency", String(10)),
    Column("payment_periods", Integer),
    Column("parcial_grace_periods", Integer),
    Column("total_grace_periods", Integer),
    Column("TEA", Float, default=0.0),
    Column("TNA", Float, default=0.0),
    Column("bank_id", Integer, ForeignKey("banks.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

meta.create_all(engine)