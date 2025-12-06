"""
Test script to run demo SQL queries
Demonstrates INSERT, UPDATE, DELETE, SELECT operations
"""
from sqlmodel import Session, select, text
from app.database import engine
from app.models import Sneaker, Brand

def test_demo_queries():
    """Run all demo SQL queries"""

    with Session(engine) as session:
        print("=" * 60)
        print("STRIDE DATABASE - DEMO SQL QUERIES")
        print("=" * 60)

        # 1. SELECT ALL
        print("\n1. SELECT * FROM sneaker (first 5):")
        print("-" * 60)
        sneakers = session.exec(select(Sneaker).limit(5)).all()
        for s in sneakers:
            print(f"  ID: {s.sneaker_id}, Name: {s.name}, Colorway: {s.colorway}, Price: ${s.price}")

        # 2. SELECT with WHERE (price > 130)
        print("\n2. SELECT name, price FROM sneaker WHERE price > 130:")
        print("-" * 60)
        sneakers = session.exec(
            select(Sneaker.name, Sneaker.price)
            .where(Sneaker.price > 130)
        ).all()
        for name, price in sneakers:
            print(f"  {name}: ${price}")

        # 3. SELECT specific sneaker
        print("\n3. SELECT name, colorway FROM sneaker WHERE name = 'Air Jordan 1':")
        print("-" * 60)
        sneakers = session.exec(
            select(Sneaker.name, Sneaker.colorway)
            .where(Sneaker.name == "Air Jordan 1")
        ).all()
        for name, colorway in sneakers:
            print(f"  {name} - {colorway}")

        # 4. INSERT new sneaker (check if it already exists)
        print("\n4. INSERT new sneaker:")
        print("-" * 60)
        existing = session.exec(
            select(Sneaker).where(Sneaker.sku == "TEST-001")
        ).first()

        if not existing:
            new_sneaker = Sneaker(
                name="Air Force 1",
                sku="TEST-001",
                release_date="2022",
                colorway="Triple White",
                available_sizes="8,9,10",
                price=120.00,
                ratings=5,
                brand_id=1,
                retailer_id=1
            )
            session.add(new_sneaker)
            session.commit()
            print(f"  Inserted: {new_sneaker.name} - {new_sneaker.colorway}")
        else:
            print(f"  Already exists: {existing.name} - {existing.colorway}")

        # 5. UPDATE price
        print("\n5. UPDATE sneaker SET price = 170.50 WHERE name = 'Air Jordan 1':")
        print("-" * 60)
        sneakers = session.exec(
            select(Sneaker).where(Sneaker.name == "Air Jordan 1")
        ).all()
        for sneaker in sneakers:
            old_price = sneaker.price
            sneaker.price = 170.50
            print(f"  Updated {sneaker.name} - {sneaker.colorway}: ${old_price} -> ${sneaker.price}")
        session.commit()

        # 6. DELETE (we'll delete our test sneaker)
        print("\n6. DELETE sneaker WHERE sku = 'TEST-001':")
        print("-" * 60)
        test_sneaker = session.exec(
            select(Sneaker).where(Sneaker.sku == "TEST-001")
        ).first()
        if test_sneaker:
            session.delete(test_sneaker)
            session.commit()
            print(f"  Deleted: {test_sneaker.name} - {test_sneaker.colorway}")
        else:
            print("  Test sneaker not found")

        # 7. JOIN query
        print("\n7. JOIN sneaker and brand tables:")
        print("-" * 60)
        query = text("""
            SELECT s.name, s.colorway, s.price, b.name as brand_name
            FROM sneaker s
            JOIN brand b ON s.brand_id = b.brand_id
            ORDER BY b.name, s.name
            LIMIT 10
        """)
        results = session.exec(query).all()
        for row in results:
            print(f"  {row.brand_name}: {row.name} - {row.colorway} (${row.price})")

        # 8. AGGREGATE query
        print("\n8. AGGREGATE: Average price by brand:")
        print("-" * 60)
        query = text("""
            SELECT b.name as brand_name, AVG(s.price) as avg_price
            FROM sneaker s
            JOIN brand b ON s.brand_id = b.brand_id
            GROUP BY b.name
            ORDER BY avg_price DESC
        """)
        results = session.exec(query).all()
        for row in results:
            print(f"  {row.brand_name}: ${row.avg_price:.2f}")

        print("\n" + "=" * 60)
        print("All demo queries completed successfully!")
        print("=" * 60)


if __name__ == "__main__":
    test_demo_queries()
