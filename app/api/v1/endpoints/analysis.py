"""
AI-powered financial analysis endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService

router = APIRouter()


@router.post("/portfolio", response_model=AnalysisResponse)
async def analyze_portfolio(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze a portfolio using AI"""
    analysis_service = AnalysisService(db)
    try:
        analysis = analysis_service.analyze_portfolio(request)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/asset", response_model=AnalysisResponse)
async def analyze_asset(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze a specific asset using AI"""
    analysis_service = AnalysisService(db)
    try:
        analysis = analysis_service.analyze_asset(request)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/recommendations", response_model=Dict[str, Any])
async def get_recommendations(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered investment recommendations"""
    analysis_service = AnalysisService(db)
    try:
        recommendations = analysis_service.get_recommendations(request)
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/market-sentiment")
async def get_market_sentiment(
    db: Session = Depends(get_db)
):
    """Get current market sentiment analysis"""
    analysis_service = AnalysisService(db)
    try:
        sentiment = analysis_service.get_market_sentiment()
        return sentiment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get market sentiment: {str(e)}"
        ) 