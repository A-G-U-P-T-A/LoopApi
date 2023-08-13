from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from sqlalchemy import text

from models.models import Base, StoreStatus, BusinessHours, StoreTimezone

DATABASE_URL = "mysql://test:test@localhost/loop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clear_tables():
    with SessionLocal() as db:
        if db.execute(text("SHOW TABLES LIKE 'store_status'")).fetchone():
            db.query(StoreStatus).delete()
        if db.execute(text("SHOW TABLES LIKE 'business_hours'")).fetchone():
            db.query(BusinessHours).delete()
        if db.execute(text("SHOW TABLES LIKE 'store_timezone'")).fetchone():
            db.query(StoreTimezone).delete()
        db.commit()
