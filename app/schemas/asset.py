"""
Asset Pydantic schemas
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.asset import AssetType


class AssetBase(BaseModel):
    """Base asset schema"""
    name: str = Field(..., description="Asset name")
    symbol: str = Field(..., description="Asset symbol/ticker")
    asset_type: AssetType = Field(..., description="Type of asset")
    current_price: float = Field(..., description="Current price")
    currency: str = Field(default="USD", description="Currency")
    description: Optional[str] = Field(None, description="Asset description")
    sector: Optional[str] = Field(None, description="Sector/industry")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    volume: Optional[float] = Field(None, description="Trading volume")
    pe_ratio: Optional[float] = Field(None, description="Price-to-earnings ratio")
    dividend_yield: Optional[float] = Field(None, description="Dividend yield")
    beta: Optional[float] = Field(None, description="Beta coefficient")
    volatility: Optional[float] = Field(None, description="Volatility measure")


class AssetCreate(AssetBase):
    """Schema for creating an asset"""
    pass


class AssetUpdate(BaseModel):
    """Schema for updating an asset"""
    name: Optional[str] = None
    symbol: Optional[str] = None
    asset_type: Optional[AssetType] = None
    current_price: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    sector: Optional[str] = None
    market_cap: Optional[float] = None
    volume: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    volatility: Optional[float] = None


class AssetResponse(AssetBase):
    """Schema for asset response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 