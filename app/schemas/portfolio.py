"""
Portfolio Pydantic schemas
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class PortfolioBase(BaseModel):
    """Base portfolio schema"""
    name: str = Field(..., description="Portfolio name")
    description: Optional[str] = Field(None, description="Portfolio description")
    user_id: Optional[int] = Field(None, description="User ID (for future use)")
    total_value: float = Field(default=0.0, description="Total portfolio value")
    cash_balance: float = Field(default=0.0, description="Cash balance")
    risk_tolerance: str = Field(default="moderate", description="Risk tolerance level")
    investment_goal: Optional[str] = Field(None, description="Investment goal")
    target_return: Optional[float] = Field(None, description="Target return percentage")
    max_drawdown: Optional[float] = Field(None, description="Maximum drawdown tolerance")


class PortfolioCreate(PortfolioBase):
    """Schema for creating a portfolio"""
    pass


class PortfolioUpdate(BaseModel):
    """Schema for updating a portfolio"""
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
    total_value: Optional[float] = None
    cash_balance: Optional[float] = None
    risk_tolerance: Optional[str] = None
    investment_goal: Optional[str] = None
    target_return: Optional[float] = None
    max_drawdown: Optional[float] = None


class PortfolioAssetResponse(BaseModel):
    """Schema for portfolio asset response"""
    id: int
    asset_id: int
    quantity: float
    average_cost: float
    current_value: float
    allocation_percentage: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PortfolioResponse(PortfolioBase):
    """Schema for portfolio response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    portfolio_assets: Optional[List[PortfolioAssetResponse]] = []

    class Config:
        from_attributes = True 