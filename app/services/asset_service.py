"""
Asset service with business logic
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate
from app.core.exceptions import AssetNotFoundException


class AssetService:
    """Service for asset management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_assets(self, skip: int = 0, limit: int = 100) -> List[Asset]:
        """Get all assets with pagination"""
        return self.db.query(Asset).offset(skip).limit(limit).all()
    
    def get_asset(self, asset_id: int) -> Optional[Asset]:
        """Get asset by ID"""
        return self.db.query(Asset).filter(Asset.id == asset_id).first()
    
    def get_asset_by_symbol(self, symbol: str) -> Optional[Asset]:
        """Get asset by symbol"""
        return self.db.query(Asset).filter(Asset.symbol == symbol).first()
    
    def create_asset(self, asset_data: AssetCreate) -> Asset:
        """Create a new asset"""
        db_asset = Asset(**asset_data.dict())
        self.db.add(db_asset)
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
    
    def update_asset(self, asset_id: int, asset_data: AssetUpdate) -> Optional[Asset]:
        """Update an existing asset"""
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return None
        
        update_data = asset_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asset, field, value)
        
        self.db.commit()
        self.db.refresh(db_asset)
        return db_asset
    
    def delete_asset(self, asset_id: int) -> bool:
        """Delete an asset"""
        db_asset = self.get_asset(asset_id)
        if not db_asset:
            return False
        
        self.db.delete(db_asset)
        self.db.commit()
        return True
    
    def search_assets(self, query: str) -> List[Asset]:
        """Search assets by name or symbol"""
        return self.db.query(Asset).filter(
            (Asset.name.ilike(f"%{query}%")) | 
            (Asset.symbol.ilike(f"%{query}%"))
        ).all()
    
    def get_assets_by_type(self, asset_type: str) -> List[Asset]:
        """Get assets by type"""
        return self.db.query(Asset).filter(Asset.asset_type == asset_type).all() 