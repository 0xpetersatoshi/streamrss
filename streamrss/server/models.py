
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base  = declarative_base()

class Rules(Base):
    __tablename__ = 'rules'
    id  = Column(Integer, primary_key=True, index=True)
    pattern = Column(String)
    tag = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
