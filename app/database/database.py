
from sqlalchemy import Table, create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine



SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://sanjana:5454@localhost:5431/todolist"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,  class_=AsyncSession)
Base = declarative_base()
metadata = MetaData()

def create_table_dynamically(table_name, columns):

    try:
        if not engine.dialect.has_table(engine, table_name):
            table = Table(table_name, metadata, *columns)
            metadata.create_all(engine)
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Table '{table_name}' already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")


def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()

# def create_all_tables():
#     """
#     Creates all tables defined in the models.
#     """
#     Base.metadata.create_all(bind=engine)
