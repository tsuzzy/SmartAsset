"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings


# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine for testing"""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Create database session for testing"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with overridden database"""
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_asset_data():
    """Sample asset data for testing"""
    return {
        "name": "Apple Inc.",
        "symbol": "AAPL",
        "asset_type": "stock",
        "current_price": 150.0,
        "currency": "USD",
        "description": "Technology company",
        "sector": "Technology",
        "market_cap": 2500000000000.0,
        "volume": 50000000.0,
        "pe_ratio": 25.0,
        "dividend_yield": 0.5,
        "beta": 1.2,
        "volatility": 0.25
    }


@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing"""
    return {
        "name": "My Portfolio",
        "description": "A test portfolio",
        "total_value": 10000.0,
        "cash_balance": 1000.0,
        "risk_tolerance": "moderate",
        "investment_goal": "Growth",
        "target_return": 8.0,
        "max_drawdown": 15.0
    } 