-- Stride Database Schema - ER Diagram Compliant Version
-- PostgreSQL Schema for Sneaker E-commerce/Tracking Platform
-- Matches ER Diagram EXACTLY with all constraints

-- Drop tables if they exist (for clean setup)
-- Must drop in correct order to respect foreign key dependencies
DROP TABLE IF EXISTS favorites CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;
DROP TABLE IF EXISTS sneaker CASCADE;
DROP TABLE IF EXISTS brand CASCADE;
DROP TABLE IF EXISTS retailer CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

-- =============================================================================
-- ENTITY: Retailer
-- Primary Key: retailer_id
-- Attributes: name, location, website
-- =============================================================================
CREATE TABLE retailer (
    retailer_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(50),
    website VARCHAR(100)
);

-- =============================================================================
-- ENTITY: Brand
-- Primary Key: brand_id
-- Attributes: name, website
-- Foreign Key: retailer_id (from "Sold By" relationship)
-- Constraint: Total Participation - Every brand MUST have a retailer (NOT NULL)
-- =============================================================================
CREATE TABLE brand (
    brand_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    website VARCHAR(100),
    retailer_id INT NOT NULL,  -- MOVED FROM SNEAKER - ER Diagram requirement
    FOREIGN KEY (retailer_id) REFERENCES retailer(retailer_id) ON DELETE RESTRICT
);

-- =============================================================================
-- ENTITY: User
-- Primary Key: user_id
-- Attributes: name, email, password
-- =============================================================================
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
);

-- =============================================================================
-- ENTITY: Sneaker
-- Primary Key: sneaker_id
-- Attributes: name, sku, release_date, colorway, available_sizes, price, ratings
-- Foreign Key: brand_id (from "Made By" relationship)
-- Constraint: A sneaker cannot exist without a brand (NOT NULL)
-- NOTE: retailer_id REMOVED - now inherited through brand
-- =============================================================================
CREATE TABLE sneaker (
    sneaker_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    sku VARCHAR(20) UNIQUE NOT NULL,
    release_date VARCHAR(20),
    colorway VARCHAR(50),
    available_sizes VARCHAR(50),
    price FLOAT NOT NULL,
    ratings INT CHECK (ratings >= 1 AND ratings <= 5),
    brand_id INT NOT NULL,  -- "Made By" relationship (N:1)
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id) ON DELETE CASCADE
);

-- =============================================================================
-- ENTITY: Price History (Weak Entity)
-- Primary Key: price_id
-- Foreign Key: sneaker_id (dependency on Sneaker)
-- Attributes: price, timestamp
-- Relationship: "Was Historically Priced" (1:N from Sneaker)
-- =============================================================================
CREATE TABLE price_history (
    price_id SERIAL PRIMARY KEY,
    sneaker_id INT NOT NULL,
    price FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sneaker_id) REFERENCES sneaker(sneaker_id) ON DELETE CASCADE
);

-- =============================================================================
-- JUNCTION TABLE: Favorites
-- Relationship: "Favorites" (M:N between User and Sneaker)
-- Primary Key: Composite (user_id, sneaker_id)
-- Foreign Keys: user_id, sneaker_id
-- Constraint: One user can favorite many sneakers, one sneaker can be favorited by many users
-- =============================================================================
CREATE TABLE favorites (
    user_id INT NOT NULL,
    sneaker_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, sneaker_id),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (sneaker_id) REFERENCES sneaker(sneaker_id) ON DELETE CASCADE
);

-- =============================================================================
-- INDEXES for Performance Optimization
-- =============================================================================
-- Sneaker indexes
CREATE INDEX idx_sneaker_brand ON sneaker(brand_id);
CREATE INDEX idx_sneaker_sku ON sneaker(sku);

-- Brand indexes
CREATE INDEX idx_brand_retailer ON brand(retailer_id);

-- Price history indexes
CREATE INDEX idx_price_history_sneaker ON price_history(sneaker_id);
CREATE INDEX idx_price_history_timestamp ON price_history(timestamp);
CREATE INDEX idx_price_history_sneaker_timestamp ON price_history(sneaker_id, timestamp);

-- Favorites indexes
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_favorites_sneaker ON favorites(sneaker_id);

-- User indexes
CREATE INDEX idx_user_email ON "user"(email);

-- =============================================================================
-- RELATIONSHIP SUMMARY (Per ER Diagram):
-- =============================================================================
-- 1. "Made By" (Sneaker → Brand): Many-to-One (N:1)
--    Implementation: brand_id FK in sneaker table
--
-- 2. "Sold By" (Brand → Retailer): Many-to-One (N:1) with Total Participation
--    Implementation: retailer_id FK in brand table (NOT NULL)
--    Constraint: Every brand MUST be associated with a retailer
--
-- 3. "Favorites" (User ↔ Sneaker): Many-to-Many (M:N)
--    Implementation: favorites junction table
--
-- 4. "Was Historically Priced" (Sneaker → Price History): One-to-Many (1:N)
--    Implementation: sneaker_id FK in price_history table
--    Note: Price History is a weak/dependent entity
-- =============================================================================
