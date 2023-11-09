from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table("users", 
    meta, 
    Column("id", Integer, primary_key=True),
    Column("first_name", String(30)),
    Column("last_name", String(30)),
    Column("email", String(50)),
    Column("password", String(255))
)

meta.create_all(engine)