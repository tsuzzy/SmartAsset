"""
Analysis Pydantic schemas
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime


class AnalysisRequest(BaseModel):
    """Schema for analysis request"""
    portfolio_id: Optional[int] = Field(None, description="Portfolio ID to analyze")
    asset_id: Optional[int] = Field(None, description="Asset ID to analyze")
    analysis_type: str = Field(..., description="Type of analysis to perform")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Analysis parameters")


class AnalysisResult(BaseModel):
    """Schema for analysis result"""
    metric: str = Field(..., description="Analysis metric name")
    value: float = Field(..., description="Metric value")
    unit: Optional[str] = Field(None, description="Value unit")
    description: Optional[str] = Field(None, description="Metric description")


class Recommendation(BaseModel):
    """Schema for investment recommendation"""
    action: str = Field(..., description="Recommended action")
    asset_id: Optional[int] = Field(None, description="Target asset ID")
    quantity: Optional[float] = Field(None, description="Recommended quantity")
    confidence: float = Field(..., description="Confidence level (0-1)")
    reasoning: str = Field(..., description="Reasoning for recommendation")


class AnalysisResponse(BaseModel):
    """Schema for analysis response"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    analysis_type: str = Field(..., description="Type of analysis performed")
    target_id: Optional[int] = Field(None, description="Target portfolio or asset ID")
    results: List[AnalysisResult] = Field(..., description="Analysis results")
    recommendations: Optional[List[Recommendation]] = Field(None, description="AI recommendations")
    summary: str = Field(..., description="Analysis summary")
    risk_level: Optional[str] = Field(None, description="Risk assessment")
    confidence_score: float = Field(..., description="Overall confidence score") 