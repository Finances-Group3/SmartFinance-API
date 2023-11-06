from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

banks = Table("banks", 
    meta, 
    Column("id", Integer, primary_key=True),
    Column("name", String(30))
)

meta.create_all(engine)