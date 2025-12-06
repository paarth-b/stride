"""
FastAPI main application for Stride backend
Provides REST API for sneaker price visualization
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import os
from dotenv import load_dotenv

from app.models import (
    Brand,
    Retailer,
    Sneaker,
    PriceHistory,
    Favorites,
    SneakerWithBrand,
    PricePoint,
    PriceHistoryRequest,
    FavoriteRequest
)
from app.database import get_session, create_db_and_tables
from app.data_generator import seed_from_csv

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Stride API",
    description="Sneaker Price Visualization Platform API",
    version="1.0.0"
)

# Configure CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
cors_origins = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:3001",
]
# Add any additional origins from environment (comma-separated)
extra_origins = os.getenv("CORS_ORIGINS", "")
if extra_origins:
    cors_origins.extend([origin.strip() for origin in extra_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create tables on startup"""
    create_db_and_tables()


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "name": "Stride API",
        "version": "1.0.0",
        "description": "Sneaker Price Visualization Platform",
        "endpoints": {
            "GET /api/sneakers": "Get all sneakers with brand information",
            "POST /api/sneakers/prices": "Get price history for selected sneakers",
            "POST /api/init-data": "Initialize database with sample data",
            "GET /docs": "Interactive API documentation"
        }
    }


@app.get("/api/sneakers", response_model=List[SneakerWithBrand])
def get_all_sneakers(session: Session = Depends(get_session)):
    """
    Get all sneakers with brand and retailer information
    Returns denormalized data for easy frontend consumption

    ER Diagram Compliance:
    - Sneaker has brand_id (Made By relationship)
    - Brand has retailer_id (Sold By relationship)
    - Retailer info is inherited through brand
    """
    # Join sneakers with brands AND retailers (retailer via brand per ER diagram)
    statement = (
        select(
            Sneaker.sneaker_id,
            Sneaker.name,
            Sneaker.sku,
            Sneaker.release_date,
            Sneaker.colorway,
            Sneaker.available_sizes,
            Sneaker.price,
            Sneaker.ratings,
            Sneaker.brand_id,
            Brand.name.label("brand_name"),
            Brand.retailer_id  # Now from Brand, not Sneaker!
        )
        .join(Brand, Sneaker.brand_id == Brand.brand_id)
        .order_by(Brand.name, Sneaker.name)
    )

    results = session.exec(statement).all()

    # Convert to response model
    sneakers = []
    for row in results:
        sneaker = SneakerWithBrand(
            sneaker_id=row.sneaker_id,
            name=row.name,
            sku=row.sku,
            release_date=row.release_date,
            colorway=row.colorway,
            available_sizes=row.available_sizes,
            price=row.price,
            ratings=row.ratings,
            brand_id=row.brand_id,
            brand_name=row.brand_name,
            retailer_id=row.retailer_id  # Inherited from brand
        )
        sneakers.append(sneaker)

    return sneakers


@app.post("/api/sneakers/prices", response_model=List[PricePoint])
def get_price_history(
    request: PriceHistoryRequest,
    session: Session = Depends(get_session)
):
    """
    Get price history for selected sneakers
    Supports filtering by date range
    """
    if not request.sneaker_ids:
        raise HTTPException(status_code=400, detail="No sneaker IDs provided")

    # Build query
    statement = select(PriceHistory).where(
        PriceHistory.sneaker_id.in_(request.sneaker_ids)
    )

    # Apply date filters if provided
    if request.start_date:
        statement = statement.where(PriceHistory.timestamp >= request.start_date)
    if request.end_date:
        statement = statement.where(PriceHistory.timestamp <= request.end_date)

    # Order by timestamp
    statement = statement.order_by(PriceHistory.timestamp)

    # Execute query
    price_history = session.exec(statement).all()

    # Convert to response model
    price_points = [
        PricePoint(
            timestamp=ph.timestamp,
            price=ph.price,
            sneaker_id=ph.sneaker_id
        )
        for ph in price_history
    ]

    return price_points


@app.post("/api/init-data")
def initialize_data(session: Session = Depends(get_session)):
    """
    Initialize database with data from expanded CSV files
    Loads data according to ER diagram requirements
    """
    try:
        seed_from_csv()
        return {
            "status": "success",
            "message": "Database initialized successfully from expanded CSV files (ER Diagram Compliant)"
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"CSV file not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize data: {str(e)}")


@app.get("/api/brands", response_model=List[Brand])
def get_all_brands(session: Session = Depends(get_session)):
    """Get all brands"""
    brands = session.exec(select(Brand)).all()
    return brands


@app.get("/api/retailers", response_model=List[Retailer])
def get_all_retailers(session: Session = Depends(get_session)):
    """Get all retailers"""
    retailers = session.exec(select(Retailer)).all()
    return retailers


@app.post("/api/favorites")
def add_favorite(request: FavoriteRequest, session: Session = Depends(get_session)):
    """
    Add a sneaker to user's favorites
    Implements the M:N "Favorites" relationship from ER diagram
    """
    # Check if already favorited
    existing = session.exec(
        select(Favorites).where(
            Favorites.user_id == request.user_id,
            Favorites.sneaker_id == request.sneaker_id
        )
    ).first()

    if existing:
        return {"status": "already_exists", "message": "Already in favorites"}

    favorite = Favorites(
        user_id=request.user_id,
        sneaker_id=request.sneaker_id
    )
    session.add(favorite)
    session.commit()

    return {"status": "success", "message": "Added to favorites"}


@app.delete("/api/favorites/{user_id}/{sneaker_id}")
def remove_favorite(user_id: int, sneaker_id: int, session: Session = Depends(get_session)):
    """Remove a sneaker from user's favorites"""
    favorite = session.exec(
        select(Favorites).where(
            Favorites.user_id == user_id,
            Favorites.sneaker_id == sneaker_id
        )
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    session.delete(favorite)
    session.commit()

    return {"status": "success", "message": "Removed from favorites"}


@app.get("/api/favorites/{user_id}")
def get_user_favorites(user_id: int, session: Session = Depends(get_session)):
    """Get all favorites for a user"""
    favorites = session.exec(
        select(Favorites.sneaker_id).where(Favorites.user_id == user_id)
    ).all()

    return {"user_id": user_id, "favorited_sneaker_ids": favorites}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", os.getenv("BACKEND_PORT", 8000))),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
