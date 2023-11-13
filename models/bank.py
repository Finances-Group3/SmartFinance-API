from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Float
from config.db import meta, engine

banks = Table(
    "banks",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("image_url", String(255)),
    Column("porcentaje_seguro_desgravamen", Float),
    Column("porcentaje_seguro_vehicular", Float),
)

meta.create_all(engine)