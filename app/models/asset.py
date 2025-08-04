"""
Asset model
"""
from sqlalchemy import Column, String, Float, Text, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class AssetType(str, enum.Enum):
    """Asset types"""
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    MUTUAL_FUND = "mutual_fund"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    REAL_ESTATE = "real_estate"
    OTHER = "other"


class Asset(BaseModel):
    """Asset database model"""
    __tablename__ = "assets"

    name = Column(String(255), nullable=False, index=True)
    symbol = Column(String(20), nullable=False, unique=True, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    current_price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    description = Column(Text, nullable=True)
    sector = Column(String(100), nullable=True)
    market_cap = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    dividend_yield = Column(Float, nullable=True)
    beta = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)

    # Relationships
    portfolio_assets = relationship("PortfolioAsset", back_populates="asset")
    transactions = relationship("Transaction", back_populates="asset") 