-- Demo SQL Queries for Stride Application
-- These queries demonstrate all required functionality

-- 1. SELECT: Get all sneakers
SELECT * FROM sneaker;

-- 2. SELECT with WHERE: Get sneakers with price > 130
SELECT name, price FROM sneaker
WHERE price > 130;

-- 3. SELECT with specific condition: Get Air Jordan 1 sneakers
SELECT name, colorway FROM sneaker
WHERE name = 'Air Jordan 1';

-- 4. INSERT: Add a new sneaker
INSERT INTO sneaker (sneaker_id, name, sku, release_date, colorway, available_sizes, price, ratings, brand_id, retailer_id)
VALUES (51, 'Air Force 1', 'CW2288-111', '2022', 'Triple White', '8,9,10', 120.00, 5, 1, 1);

-- 5. UPDATE: Update price of Air Jordan 1
UPDATE sneaker
SET price = 170.50
WHERE name = 'Air Jordan 1';

-- 6. DELETE: Delete a sneaker by ID
DELETE FROM sneaker
WHERE sneaker_id = 5;

-- 7. JOIN: Get sneakers with brand information
SELECT s.name, s.colorway, s.price, b.name as brand_name
FROM sneaker s
JOIN brand b ON s.brand_id = b.brand_id
ORDER BY b.name, s.name;

-- 8. AGGREGATE: Get average price by brand
SELECT b.name as brand_name, AVG(s.price) as avg_price
FROM sneaker s
JOIN brand b ON s.brand_id = b.brand_id
GROUP BY b.name
ORDER BY avg_price DESC;

-- 9. Price History: Get latest prices for each sneaker
SELECT s.name, s.colorway, ph.price, ph.timestamp
FROM price_history ph
JOIN sneaker s ON ph.sneaker_id = s.sneaker_id
WHERE ph.timestamp >= NOW() - INTERVAL '7 days'
ORDER BY ph.timestamp DESC
LIMIT 20;

-- 10. Complex Query: Get price statistics for each sneaker
SELECT
    s.name,
    s.colorway,
    s.price as retail_price,
    MIN(ph.price) as min_price,
    MAX(ph.price) as max_price,
    AVG(ph.price) as avg_price,
    COUNT(ph.price_id) as data_points
FROM sneaker s
JOIN price_history ph ON s.sneaker_id = ph.sneaker_id
GROUP BY s.sneaker_id, s.name, s.colorway, s.price
ORDER BY avg_price DESC;
