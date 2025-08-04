"""
Portfolio service with business logic
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.portfolio import Portfolio, PortfolioAsset
from app.models.asset import Asset
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate
from app.core.exceptions import PortfolioNotFoundException


class PortfolioService:
    """Service for portfolio management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_portfolios(self, skip: int = 0, limit: int = 100) -> List[Portfolio]:
        """Get all portfolios with pagination"""
        return self.db.query(Portfolio).offset(skip).limit(limit).all()
    
    def get_portfolio(self, portfolio_id: int) -> Optional[Portfolio]:
        """Get portfolio by ID"""
        return self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    
    def create_portfolio(self, portfolio_data: PortfolioCreate) -> Portfolio:
        """Create a new portfolio"""
        db_portfolio = Portfolio(**portfolio_data.dict())
        self.db.add(db_portfolio)
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def update_portfolio(self, portfolio_id: int, portfolio_data: PortfolioUpdate) -> Optional[Portfolio]:
        """Update an existing portfolio"""
        db_portfolio = self.get_portfolio(portfolio_id)
        if not db_portfolio:
            return None
        
        update_data = portfolio_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_portfolio, field, value)
        
        self.db.commit()
        self.db.refresh(db_portfolio)
        return db_portfolio
    
    def delete_portfolio(self, portfolio_id: int) -> bool:
        """Delete a portfolio"""
        db_portfolio = self.get_portfolio(portfolio_id)
        if not db_portfolio:
            return False
        
        self.db.delete(db_portfolio)
        self.db.commit()
        return True
    
    def add_asset_to_portfolio(self, portfolio_id: int, asset_id: int, quantity: float, price: float) -> bool:
        """Add asset to portfolio"""
        portfolio = self.get_portfolio(portfolio_id)
        if not portfolio:
            return False
        
        # Check if asset already exists in portfolio
        existing_asset = self.db.query(PortfolioAsset).filter(
            PortfolioAsset.portfolio_id == portfolio_id,
            PortfolioAsset.asset_id == asset_id
        ).first()
        
        if existing_asset:
            # Update existing position
            total_quantity = existing_asset.quantity + quantity
            total_cost = (existing_asset.average_cost * existing_asset.quantity) + (price * quantity)
            existing_asset.average_cost = total_cost / total_quantity
            existing_asset.quantity = total_quantity
        else:
            # Create new position
            portfolio_asset = PortfolioAsset(
                portfolio_id=portfolio_id,
                asset_id=asset_id,
                quantity=quantity,
                average_cost=price
            )
            self.db.add(portfolio_asset)
        
        self.db.commit()
        return True
    
    def remove_asset_from_portfolio(self, portfolio_id: int, asset_id: int, quantity: float) -> bool:
        """Remove asset from portfolio"""
        portfolio_asset = self.db.query(PortfolioAsset).filter(
            PortfolioAsset.portfolio_id == portfolio_id,
            PortfolioAsset.asset_id == asset_id
        ).first()
        
        if not portfolio_asset or portfolio_asset.quantity < quantity:
            return False
        
        portfolio_asset.quantity -= quantity
        if portfolio_asset.quantity == 0:
            self.db.delete(portfolio_asset)
        
        self.db.commit()
        return True
    
    def get_portfolio_performance(self, portfolio_id: int) -> Optional[Dict[str, Any]]:
        """Get portfolio performance metrics"""
        portfolio = self.get_portfolio(portfolio_id)
        if not portfolio:
            return None
        
        # Calculate basic metrics
        total_invested = sum(
            pa.quantity * pa.average_cost 
            for pa in portfolio.portfolio_assets
        )
        
        current_value = sum(
            pa.quantity * pa.asset.current_price 
            for pa in portfolio.portfolio_assets
        )
        
        total_return = current_value - total_invested
        return_percentage = (total_return / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "portfolio_id": portfolio_id,
            "total_invested": total_invested,
            "current_value": current_value,
            "total_return": total_return,
            "return_percentage": return_percentage,
            "cash_balance": portfolio.cash_balance,
            "total_portfolio_value": current_value + portfolio.cash_balance
        } 