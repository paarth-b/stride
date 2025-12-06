"""
SQLModel ORM models for Stride database
ER DIAGRAM COMPLIANT VERSION
Matches the ER diagram exactly with all relationships and constraints
"""
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Retailer(SQLModel, table=True):
    """
    ENTITY: Retailer
    Represents stores or vendors selling brands
    Primary Key: retailer_id
    Attributes: name, location, website
    """
    retailer_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    location: Optional[str] = Field(default=None, max_length=50)
    website: Optional[str] = Field(default=None, max_length=100)

    # Relationship: One retailer can sell many brands
    # brands: List["Brand"] = Relationship(back_populates="retailer")


class Brand(SQLModel, table=True):
    """
    ENTITY: Brand
    Represents sneaker manufacturers
    Primary Key: brand_id
    Attributes: name, website
    Foreign Key: retailer_id (from "Sold By" relationship)
    CONSTRAINT: Total Participation - must have a retailer (NOT NULL)
    """
    brand_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    website: Optional[str] = Field(default=None, max_length=100)

    # RELATIONSHIP: "Sold By" (Brand → Retailer) Many-to-One
    # Total participation: NOT NULL enforced
    retailer_id: int = Field(foreign_key="retailer.retailer_id")

    # Relationship: One brand can have many sneakers
    # retailer: Optional[Retailer] = Relationship(back_populates="brands")
    # sneakers: List["Sneaker"] = Relationship(back_populates="brand")


class User(SQLModel, table=True):
    """
    ENTITY: User
    Represents customers/accounts using the platform
    Primary Key: user_id
    Attributes: name, email, password
    """
    __tablename__ = "user"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=50, unique=True)
    password: str = Field(max_length=50)

    # Relationship: M:N with Sneaker through favorites table
    # favorited_sneakers: List["Sneaker"] = Relationship(
    #     back_populates="favorited_by_users",
    #     link_model=Favorites
    # )


class Sneaker(SQLModel, table=True):
    """
    ENTITY: Sneaker (Central entity)
    Primary Key: sneaker_id
    Attributes: name, sku, release_date, colorway, available_sizes, price, ratings
    Foreign Key: brand_id (from "Made By" relationship)
    NOTE: retailer_id REMOVED per ER diagram - inherited through brand
    """
    sneaker_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    sku: str = Field(max_length=20, unique=True)
    release_date: Optional[str] = Field(default=None, max_length=20)
    colorway: Optional[str] = Field(default=None, max_length=50)
    available_sizes: Optional[str] = Field(default=None, max_length=50)
    price: float
    ratings: Optional[int] = Field(default=None, ge=1, le=5)

    # RELATIONSHIP: "Made By" (Sneaker → Brand) Many-to-One
    brand_id: int = Field(foreign_key="brand.brand_id")

    # Relationships
    # brand: Optional[Brand] = Relationship(back_populates="sneakers")
    # price_history: List["PriceHistory"] = Relationship(back_populates="sneaker")
    # favorited_by_users: List["User"] = Relationship(
    #     back_populates="favorited_sneakers",
    #     link_model=Favorites
    # )


class PriceHistory(SQLModel, table=True):
    """
    ENTITY: Price History (Weak/Dependent Entity)
    Tracks sneaker price fluctuations over time
    Primary Key: price_id
    Foreign Key: sneaker_id (dependency on Sneaker)
    Attributes: price, timestamp
    RELATIONSHIP: "Was Historically Priced" (1:N from Sneaker)
    """
    __tablename__ = "price_history"

    price_id: Optional[int] = Field(default=None, primary_key=True)
    sneaker_id: int = Field(foreign_key="sneaker.sneaker_id")
    price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: Each price history belongs to one sneaker
    # sneaker: Optional[Sneaker] = Relationship(back_populates="price_history")


class Favorites(SQLModel, table=True):
    """
    JUNCTION TABLE: Favorites
    Implements Many-to-Many relationship between User and Sneaker
    RELATIONSHIP: "Favorites" (User ↔ Sneaker) M:N
    Primary Key: Composite (user_id, sneaker_id)
    """
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    sneaker_id: int = Field(foreign_key="sneaker.sneaker_id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# =============================================================================
# Response/DTO Models for API (not database tables)
# =============================================================================

class SneakerWithBrand(SQLModel):
    """
    Response model: Sneaker with brand and retailer information
    Denormalized for easy frontend consumption
    """
    sneaker_id: int
    name: str
    sku: str
    release_date: Optional[str]
    colorway: Optional[str]
    available_sizes: Optional[str]
    price: float
    ratings: Optional[int]
    brand_id: int
    brand_name: str
    retailer_id: int  # Inherited from brand
    retailer_name: Optional[str] = None  # Can include retailer name too


class PricePoint(SQLModel):
    """Response model: Price point for time-series visualization"""
    timestamp: datetime
    price: float
    sneaker_id: int


class PriceHistoryRequest(SQLModel):
    """Request model: Get price history for selected sneakers"""
    sneaker_ids: list[int]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class FavoriteRequest(SQLModel):
    """Request model: Add/remove favorite"""
    user_id: int
    sneaker_id: int


class FavoriteResponse(SQLModel):
    """Response model: User's favorited sneakers"""
    user_id: int
    sneaker_id: int
    sneaker_name: str
    brand_name: str
    created_at: datetime
