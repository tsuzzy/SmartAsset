#!/usr/bin/env python3
"""
Database setup script for SmartAsset
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.core.config import settings


def setup_database():
    """Set up the database tables"""
    print("Setting up database...")
    
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("Database tables created successfully!")
    
    # Test connection
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("Database connection test successful!")
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
    
    return True


def main():
    """Main setup function"""
    print("SmartAsset Database Setup")
    print("=" * 30)
    
    # Check if DATABASE_URL is set
    if not settings.DATABASE_URL:
        print("Error: DATABASE_URL not configured")
        print("Please set up your environment variables")
        return False
    
    print(f"Database URL: {settings.DATABASE_URL}")
    
    # Set up database
    success = setup_database()
    
    if success:
        print("\nDatabase setup completed successfully!")
        print("\nNext steps:")
        print("1. Run migrations: alembic upgrade head")
        print("2. Start the application: uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("\nDatabase setup failed!")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 