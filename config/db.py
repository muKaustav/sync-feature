from decouple import config
from sqlalchemy import create_engine, MetaData

user = config("PSQL_USER")
password = config("PSQL_PASSWORD")
host = config("PSQL_HOST")
port = config("PSQL_PORT")
database = config("PSQL_DB")

POSTGRES_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(POSTGRES_URL)

meta = MetaData()

conn = engine.connect()
