from sqlalchemy import create_engine, MetaData
from starlette.config import Config

config = Config(".env")

_user = config("DB_USER", cast=str)
_password = config("DB_PASSWORD", cast=str)
_host = config("DB_HOST", cast=str)
_database = config("DB_NAME", cast=str)
_port = config("DB_PORT", cast=int, default=3306)

URL_DATABASE = f"mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_database}"

engine = create_engine(URL_DATABASE).execution_options(isolation_level="AUTOCOMMIT")

meta = MetaData()
 
meta.create_all(engine)

conn = engine.connect()