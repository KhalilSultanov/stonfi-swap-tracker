from sqlalchemy import Column, Integer, String, DateTime, Float
from .db import Base
from datetime import datetime


class SwapTransaction(Base):
    __tablename__ = "swap_transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    tx_hash = Column(String, unique=True, index=True)
    token_in = Column(String)
    token_out = Column(String)
    amount_in = Column(Float)
    amount_out = Column(Float)
    timestamp = Column(DateTime, default=datetime.now())
    status = Column(String)
