"""
Tests for asset API endpoints
"""
import pytest
from fastapi.testclient import TestClient

from app.models.asset import Asset, AssetType


class TestAssetsAPI:
    """Test asset API endpoints"""
    
    def test_get_assets_empty(self, client: TestClient):
        """Test getting assets when none exist"""
        response = client.get("/api/v1/assets/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_asset(self, client: TestClient, sample_asset_data: dict):
        """Test creating a new asset"""
        response = client.post("/api/v1/assets/", json=sample_asset_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_asset_data["name"]
        assert data["symbol"] == sample_asset_data["symbol"]
        assert data["asset_type"] == sample_asset_data["asset_type"]
        assert data["current_price"] == sample_asset_data["current_price"]
    
    def test_get_asset_by_id(self, client: TestClient, sample_asset_data: dict):
        """Test getting asset by ID"""
        # First create an asset
        create_response = client.post("/api/v1/assets/", json=sample_asset_data)
        assert create_response.status_code == 200
        asset_id = create_response.json()["id"]
        
        # Then get it by ID
        response = client.get(f"/api/v1/assets/{asset_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == asset_id
        assert data["name"] == sample_asset_data["name"]
    
    def test_get_asset_not_found(self, client: TestClient):
        """Test getting non-existent asset"""
        response = client.get("/api/v1/assets/999")
        assert response.status_code == 404
        assert "Asset not found" in response.json()["detail"]
    
    def test_update_asset(self, client: TestClient, sample_asset_data: dict):
        """Test updating an asset"""
        # First create an asset
        create_response = client.post("/api/v1/assets/", json=sample_asset_data)
        assert create_response.status_code == 200
        asset_id = create_response.json()["id"]
        
        # Then update it
        update_data = {"current_price": 160.0, "description": "Updated description"}
        response = client.put(f"/api/v1/assets/{asset_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["current_price"] == 160.0
        assert data["description"] == "Updated description"
    
    def test_delete_asset(self, client: TestClient, sample_asset_data: dict):
        """Test deleting an asset"""
        # First create an asset
        create_response = client.post("/api/v1/assets/", json=sample_asset_data)
        assert create_response.status_code == 200
        asset_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/assets/{asset_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Asset deleted successfully"
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/assets/{asset_id}")
        assert get_response.status_code == 404 