from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://bcraft:password@localhost:5432/bcraft"

def get_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = None
    try:
        db = session()
        yield db
    finally:
        db.close()


