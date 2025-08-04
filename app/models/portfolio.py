"""
Portfolio model
"""
from sqlalchemy import Column, String, Float, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Portfolio(BaseModel):
    """Portfolio database model"""
    __tablename__ = "portfolios"

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For future user system
    total_value = Column(Float, default=0.0)
    cash_balance = Column(Float, default=0.0)
    risk_tolerance = Column(String(20), default="moderate")  # low, moderate, high
    investment_goal = Column(String(100), nullable=True)
    target_return = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)

    # Relationships
    portfolio_assets = relationship("PortfolioAsset", back_populates="portfolio")
    transactions = relationship("Transaction", back_populates="portfolio")


class PortfolioAsset(BaseModel):
    """Portfolio-Asset relationship model"""
    __tablename__ = "portfolio_assets"

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    average_cost = Column(Float, nullable=False, default=0.0)
    current_value = Column(Float, nullable=False, default=0.0)
    allocation_percentage = Column(Float, nullable=True)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="portfolio_assets")
    asset = relationship("Asset", back_populates="portfolio_assets") 