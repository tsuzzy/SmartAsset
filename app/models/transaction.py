"""
Transaction model
"""
from sqlalchemy import Column, String, Float, ForeignKey, Integer, Enum, Text
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class TransactionType(str, enum.Enum):
    """Transaction types"""
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class Transaction(BaseModel):
    """Transaction database model"""
    __tablename__ = "transactions"

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)  # Null for cash transactions
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    price_per_unit = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False)
    fees = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    transaction_date = Column(String(10), nullable=False)  # YYYY-MM-DD format

    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions") 