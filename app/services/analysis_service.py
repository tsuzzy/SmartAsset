"""
AI-powered financial analysis service
"""
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisResult, Recommendation
from app.core.exceptions import AIAnalysisException
from app.services.portfolio_service import PortfolioService
from app.services.asset_service import AssetService


class AnalysisService:
    """Service for AI-powered financial analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.portfolio_service = PortfolioService(db)
        self.asset_service = AssetService(db)
    
    def analyze_portfolio(self, request: AnalysisRequest) -> AnalysisResponse:
        """Analyze a portfolio using AI"""
        if not request.portfolio_id:
            raise AIAnalysisException("Portfolio ID is required for portfolio analysis")
        
        portfolio = self.portfolio_service.get_portfolio(request.portfolio_id)
        if not portfolio:
            raise AIAnalysisException("Portfolio not found")
        
        # Get portfolio performance
        performance = self.portfolio_service.get_portfolio_performance(request.portfolio_id)
        
        # Generate analysis results
        results = self._generate_portfolio_analysis(portfolio, performance)
        
        # Generate recommendations
        recommendations = self._generate_portfolio_recommendations(portfolio, performance)
        
        return AnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            analysis_type="portfolio_analysis",
            target_id=request.portfolio_id,
            results=results,
            recommendations=recommendations,
            summary=self._generate_portfolio_summary(performance),
            risk_level=self._assess_portfolio_risk(portfolio, performance),
            confidence_score=0.85  # Placeholder confidence score
        )
    
    def analyze_asset(self, request: AnalysisRequest) -> AnalysisResponse:
        """Analyze a specific asset using AI"""
        if not request.asset_id:
            raise AIAnalysisException("Asset ID is required for asset analysis")
        
        asset = self.asset_service.get_asset(request.asset_id)
        if not asset:
            raise AIAnalysisException("Asset not found")
        
        # Generate asset analysis results
        results = self._generate_asset_analysis(asset)
        
        # Generate asset recommendations
        recommendations = self._generate_asset_recommendations(asset)
        
        return AnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            analysis_type="asset_analysis",
            target_id=request.asset_id,
            results=results,
            recommendations=recommendations,
            summary=self._generate_asset_summary(asset),
            risk_level=self._assess_asset_risk(asset),
            confidence_score=0.80  # Placeholder confidence score
        )
    
    def get_recommendations(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Get AI-powered investment recommendations"""
        # This would integrate with LangChain and OpenAI
        # For now, return placeholder recommendations
        return {
            "recommendations": [
                {
                    "action": "buy",
                    "asset_symbol": "AAPL",
                    "confidence": 0.75,
                    "reasoning": "Strong fundamentals and positive market sentiment"
                },
                {
                    "action": "hold",
                    "asset_symbol": "MSFT",
                    "confidence": 0.85,
                    "reasoning": "Stable performance, good for long-term holding"
                }
            ],
            "market_sentiment": "bullish",
            "risk_level": "moderate"
        }
    
    def get_market_sentiment(self) -> Dict[str, Any]:
        """Get current market sentiment analysis"""
        # This would integrate with external APIs and AI analysis
        return {
            "overall_sentiment": "neutral",
            "confidence": 0.70,
            "factors": [
                "Federal Reserve policy",
                "Earnings season performance",
                "Geopolitical events"
            ],
            "sector_sentiment": {
                "technology": "bullish",
                "healthcare": "neutral",
                "finance": "bearish"
            }
        }
    
    def _generate_portfolio_analysis(self, portfolio, performance) -> List[AnalysisResult]:
        """Generate portfolio analysis results"""
        results = []
        
        if performance:
            results.extend([
                AnalysisResult(
                    metric="Total Return",
                    value=performance["total_return"],
                    unit="USD",
                    description="Total return from investments"
                ),
                AnalysisResult(
                    metric="Return Percentage",
                    value=performance["return_percentage"],
                    unit="%",
                    description="Percentage return on investment"
                ),
                AnalysisResult(
                    metric="Portfolio Value",
                    value=performance["total_portfolio_value"],
                    unit="USD",
                    description="Total portfolio value including cash"
                )
            ])
        
        return results
    
    def _generate_portfolio_recommendations(self, portfolio, performance) -> List[Recommendation]:
        """Generate portfolio recommendations"""
        recommendations = []
        
        # Placeholder recommendations based on portfolio characteristics
        if performance and performance["return_percentage"] < 0:
            recommendations.append(
                Recommendation(
                    action="rebalance",
                    asset_id=None,
                    quantity=None,
                    confidence=0.75,
                    reasoning="Portfolio showing negative returns, consider rebalancing"
                )
            )
        
        return recommendations
    
    def _generate_asset_analysis(self, asset) -> List[AnalysisResult]:
        """Generate asset analysis results"""
        return [
            AnalysisResult(
                metric="Current Price",
                value=asset.current_price,
                unit="USD",
                description="Current market price"
            ),
            AnalysisResult(
                metric="P/E Ratio",
                value=asset.pe_ratio or 0,
                unit="",
                description="Price-to-earnings ratio"
            ),
            AnalysisResult(
                metric="Beta",
                value=asset.beta or 1.0,
                unit="",
                description="Beta coefficient (volatility vs market)"
            )
        ]
    
    def _generate_asset_recommendations(self, asset) -> List[Recommendation]:
        """Generate asset-specific recommendations"""
        recommendations = []
        
        # Simple recommendation logic based on P/E ratio
        if asset.pe_ratio and asset.pe_ratio < 15:
            recommendations.append(
                Recommendation(
                    action="buy",
                    asset_id=asset.id,
                    quantity=None,
                    confidence=0.70,
                    reasoning=f"Low P/E ratio of {asset.pe_ratio} suggests undervaluation"
                )
            )
        
        return recommendations
    
    def _generate_portfolio_summary(self, performance) -> str:
        """Generate portfolio analysis summary"""
        if not performance:
            return "Unable to generate portfolio summary"
        
        return f"Portfolio shows a {performance['return_percentage']:.2f}% return with total value of ${performance['total_portfolio_value']:,.2f}"
    
    def _generate_asset_summary(self, asset) -> str:
        """Generate asset analysis summary"""
        return f"{asset.name} ({asset.symbol}) is currently trading at ${asset.current_price:.2f} with a P/E ratio of {asset.pe_ratio or 'N/A'}"
    
    def _assess_portfolio_risk(self, portfolio, performance) -> str:
        """Assess portfolio risk level"""
        if not performance:
            return "unknown"
        
        return_percentage = performance["return_percentage"]
        if return_percentage < -10:
            return "high"
        elif return_percentage < 5:
            return "moderate"
        else:
            return "low"
    
    def _assess_asset_risk(self, asset) -> str:
        """Assess asset risk level"""
        if asset.beta:
            if asset.beta > 1.5:
                return "high"
            elif asset.beta > 0.8:
                return "moderate"
            else:
                return "low"
        return "unknown" 