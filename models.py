from sqlalchemy import Column, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    amount_uah = Column(Float)
    amount_usd = Column(Float)
    is_paid = Column(Boolean, default=False)

