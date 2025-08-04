"""
Custom exception classes
"""
from fastapi import HTTPException, status


class SmartAssetException(Exception):
    """Base exception for SmartAsset application"""
    pass


class AssetNotFoundException(SmartAssetException):
    """Raised when an asset is not found"""
    pass


class PortfolioNotFoundException(SmartAssetException):
    """Raised when a portfolio is not found"""
    pass


class InsufficientFundsException(SmartAssetException):
    """Raised when there are insufficient funds for a transaction"""
    pass


class InvalidTransactionException(SmartAssetException):
    """Raised when a transaction is invalid"""
    pass


class AIAnalysisException(SmartAssetException):
    """Raised when AI analysis fails"""
    pass


def handle_smart_asset_exception(exc: SmartAssetException):
    """Convert SmartAsset exceptions to HTTP exceptions"""
    if isinstance(exc, AssetNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    elif isinstance(exc, PortfolioNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    elif isinstance(exc, InsufficientFundsException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds for transaction"
        )
    elif isinstance(exc, InvalidTransactionException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction"
        )
    elif isinstance(exc, AIAnalysisException):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI analysis failed"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 