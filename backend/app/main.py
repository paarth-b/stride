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


@app.get("/api/sneakers/{sneaker_id}/complete")
def get_complete_sneaker_data(sneaker_id: int, session: Session = Depends(get_session)):
    """
    Get COMPLETE sneaker data showing ALL ER Diagram entities and relationships

    Returns:
    - Full Sneaker entity (all attributes)
    - Related Brand entity (Made By relationship, N:1)
    - Related Retailer entity (Sold By relationship via Brand, N:1, Total Participation)
    - Price History records (Was Historically Priced relationship, 1:N)
    - Favorited by users count (Favorites relationship, M:N)

    This endpoint demonstrates the COMPLETE ER Diagram implementation
    """
    # Get sneaker with brand and retailer (3 entities, 2 relationships)
    sneaker_query = (
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
            Brand.website.label("brand_website"),
            Brand.retailer_id,
            Retailer.name.label("retailer_name"),
            Retailer.location.label("retailer_location"),
            Retailer.website.label("retailer_website")
        )
        .join(Brand, Sneaker.brand_id == Brand.brand_id)
        .join(Retailer, Brand.retailer_id == Retailer.retailer_id)
        .where(Sneaker.sneaker_id == sneaker_id)
    )

    sneaker_data = session.exec(sneaker_query).first()

    if not sneaker_data:
        raise HTTPException(status_code=404, detail="Sneaker not found")

    # Get price history (Was Historically Priced relationship, 1:N)
    price_history = session.exec(
        select(PriceHistory)
        .where(PriceHistory.sneaker_id == sneaker_id)
        .order_by(PriceHistory.timestamp.desc())
    ).all()

    # Get favorites count (Favorites relationship, M:N)
    favorites_count = session.exec(
        select(Favorites)
        .where(Favorites.sneaker_id == sneaker_id)
    ).all()

    # Build comprehensive response
    return {
        "er_diagram_implementation": "COMPLETE - All 5 Entities, All 4 Relationships",
        "entity_sneaker": {
            "sneaker_id": sneaker_data.sneaker_id,
            "name": sneaker_data.name,
            "sku": sneaker_data.sku,
            "release_date": sneaker_data.release_date,
            "colorway": sneaker_data.colorway,
            "available_sizes": sneaker_data.available_sizes,
            "price": sneaker_data.price,
            "ratings": sneaker_data.ratings,
            "brand_id": sneaker_data.brand_id
        },
        "relationship_made_by": {
            "type": "Many-to-One (N:1)",
            "description": "Sneaker → Brand",
            "constraint": "NOT NULL on brand_id",
            "entity_brand": {
                "brand_id": sneaker_data.brand_id,
                "name": sneaker_data.brand_name,
                "website": sneaker_data.brand_website,
                "retailer_id": sneaker_data.retailer_id
            }
        },
        "relationship_sold_by": {
            "type": "Many-to-One (N:1)",
            "description": "Brand → Retailer",
            "constraint": "TOTAL PARTICIPATION - NOT NULL on brand.retailer_id",
            "note": "Sneaker inherits retailer through brand (no direct retailer_id on sneaker)",
            "entity_retailer": {
                "retailer_id": sneaker_data.retailer_id,
                "name": sneaker_data.retailer_name,
                "location": sneaker_data.retailer_location,
                "website": sneaker_data.retailer_website
            }
        },
        "relationship_was_historically_priced": {
            "type": "One-to-Many (1:N)",
            "description": "Sneaker → Price History",
            "constraint": "Price History is weak/dependent entity",
            "note": "CASCADE on DELETE - price history deleted when sneaker is deleted",
            "entity_price_history": {
                "total_records": len(price_history),
                "latest_5_prices": [
                    {
                        "price_id": ph.price_id,
                        "price": ph.price,
                        "timestamp": ph.timestamp,
                        "sneaker_id": ph.sneaker_id
                    }
                    for ph in price_history[:5]
                ]
            }
        },
        "relationship_favorites": {
            "type": "Many-to-Many (M:N)",
            "description": "User ↔ Sneaker",
            "implementation": "Junction table: favorites(user_id, sneaker_id)",
            "constraint": "Composite Primary Key: (user_id, sneaker_id)",
            "total_users_favorited": len(favorites_count),
            "favorited_by_users": [
                {
                    "user_id": fav.user_id,
                    "sneaker_id": fav.sneaker_id,
                    "created_at": fav.created_at
                }
                for fav in favorites_count[:5]
            ]
        },
        "constraints_enforced": {
            "primary_keys": "All 5 entities have PKs",
            "foreign_keys": "brand_id, retailer_id, sneaker_id, user_id",
            "unique_constraints": "sneaker.sku, user.email",
            "check_constraints": "sneaker.ratings (1-5)",
            "total_participation": "brand.retailer_id NOT NULL",
            "cascade_delete": "price_history and favorites CASCADE on sneaker delete"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", os.getenv("BACKEND_PORT", 8000))),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
