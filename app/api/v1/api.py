"""
Main API router for v1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import assets, portfolios, analysis, auth

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"]) 