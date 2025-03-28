from sqlalchemy import create_engine, MetaData
from databases import Database

# SQLite URL for the default database
DATABASE_URL = "sqlite:///./pymediamanagement.db"

# Create the SQLAlchemy engine and metadata
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

# Create the async database connection
database = Database(DATABASE_URL)