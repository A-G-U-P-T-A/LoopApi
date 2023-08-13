from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StoreStatus(Base):
    __tablename__ = 'store_status'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timestamp_utc = Column(DateTime)
    status = Column(String(15))


class BusinessHours(Base):
    __tablename__ = 'business_hours'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    day = Column(Integer)
    start_time_local = Column(Time)
    end_time_local = Column(Time)


class StoreTimezone(Base):
    __tablename__ = 'store_timezone'
    id = Column(Integer, primary_key=True)
    store_id = Column(Integer)
    timezone_str = Column(String(50))
