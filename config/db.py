from sqlalchemy import create_engine, MetaData

URL_DATABASE = "mysql+pymysql://root:password@localhost:3306/smartfinance_db"

engine = create_engine(URL_DATABASE).execution_options(isolation_level="AUTOCOMMIT")

meta = MetaData()
 
meta.create_all(engine)

conn = engine.connect()