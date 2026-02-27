from sqlalchemy import Column, Integer, Text, Numeric, TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    shop = Column(Text, index=True)
    amount = Column(Numeric)
    created_at = Column(TIMESTAMP, server_default=func.now())