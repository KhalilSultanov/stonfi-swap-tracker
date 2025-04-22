from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SwapTransactionBase(BaseModel):
    wallet_address: str
    tx_hash: str
    token_in: str
    token_out: str
    amount_in: float
    amount_out: float
    timestamp: Optional[datetime] = None
    status: str


class SwapTransactionCreate(SwapTransactionBase):
    pass


class SwapTransactionOut(SwapTransactionBase):
    id: int

    class Config:
        from_attributes = True


class WalletAddressSchema(BaseModel):
    wallet_address: str = Field(..., min_length=48, max_length=48)
