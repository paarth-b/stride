"""
Data loading script for ER Diagram Compliant Schema
Loads data from expanded CSV files
Handles brand-retailer relationship mapping
"""
import random
import csv
import os
from datetime import datetime, timedelta
from sqlmodel import Session
from collections import defaultdict

# Import models
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import Brand, Retailer, Sneaker, User, PriceHistory, Favorites
from app.database import engine


def seed_from_csv():
    """
    Seed database from expanded CSV files according to ER diagram

    Key changes from original:
    1. Brand now has retailer_id (total participation)
    2. Sneaker no longer has retailer_id
    3. Favorites junction table created
    """
    # Get the path to the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, 'data')

    # CSV file paths - EXPANDED versions
    csv_files = {
        'brand': os.path.join(data_dir, 'brand.csv'),
        'retailer': os.path.join(data_dir, 'retailer.csv'),
        'user': os.path.join(data_dir, 'user.csv'),
        'sneaker': os.path.join(data_dir, 'sneaker.csv'),
        'price_history': os.path.join(data_dir, 'price_history.csv')
    }

    # Verify all CSV files exist
    print("🔍 Verifying expanded CSV files...")
    for name, path in csv_files.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Expanded CSV file not found: {path}")
        print(f"   ✓ Found {name}.csv")

    with Session(engine) as session:
        print("\n🚀 Starting database seeding from expanded CSV files...")
        print("   ⚠️  Using ER Diagram Compliant Schema\n")

        # Clear existing data in correct order (respecting foreign keys)
        print("🧹 Clearing existing data...")
        session.query(Favorites).delete()
        session.query(PriceHistory).delete()
        session.query(Sneaker).delete()
        session.query(Brand).delete()
        session.query(Retailer).delete()
        session.query(User).delete()
        session.commit()
        print("   ✓ Existing data cleared")

        # ID mappings (CSV ID → Database ID)
        brand_id_map = {}
        retailer_id_map = {}
        sneaker_id_map = {}
        user_id_map = {}

        # Track brand→retailer mapping from sneaker data
        # We'll use the first retailer we see for each brand
        brand_to_retailer = {}

        # =================================================================
        # STEP 1: Load Retailers FIRST (no dependencies)
        # =================================================================
        print("\n🏪 Loading retailers...")
        with open(csv_files['retailer'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=['retailer_id', 'name', 'location', 'website'])
            retailers_loaded = 0
            for row in reader:
                csv_id = int(row['retailer_id'])
                retailer = Retailer(
                    name=row['name'].strip(),
                    location=row['location'].strip() if row['location'] else None,
                    website=row['website'].strip() if row['website'] else None
                )
                session.add(retailer)
                session.flush()
                retailer_id_map[csv_id] = retailer.retailer_id
                retailers_loaded += 1
            session.commit()
            print(f"   ✓ Loaded {retailers_loaded} retailers")

        # =================================================================
        # STEP 2: Read Brand→Retailer mapping from brand CSV
        # =================================================================
        print("\n🔍 Reading brand-retailer relationships from brand CSV...")
        with open(csv_files['brand'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=['brand_id', 'name', 'website', 'retailer_id'])
            for row in reader:
                try:
                    csv_brand_id = int(row['brand_id'])
                    csv_retailer_id = int(row['retailer_id'])
                    brand_to_retailer[csv_brand_id] = csv_retailer_id
                except (ValueError, KeyError):
                    continue

        print(f"   ✓ Mapped {len(brand_to_retailer)} brands to retailers")

        # =================================================================
        # STEP 3: Load Brands WITH retailer_id (ER diagram requirement)
        # =================================================================
        print("\n👟 Loading brands with retailer assignments...")
        with open(csv_files['brand'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=['brand_id', 'name', 'website', 'retailer_id'])
            brands_loaded = 0
            for row in reader:
                csv_id = int(row['brand_id'])
                csv_retailer_id = int(row['retailer_id'])

                if csv_retailer_id not in retailer_id_map:
                    print(f"   ⚠ Warning: Retailer ID {csv_retailer_id} not found for brand {row['name']}")
                    continue

                brand = Brand(
                    name=row['name'].strip(),
                    website=row['website'].strip() if row['website'] else None,
                    retailer_id=retailer_id_map[csv_retailer_id]  # ER DIAGRAM REQUIREMENT
                )
                session.add(brand)
                session.flush()
                brand_id_map[csv_id] = brand.brand_id
                brands_loaded += 1

            session.commit()
            print(f"   ✓ Loaded {brands_loaded} brands with retailer associations")

        # =================================================================
        # STEP 4: Load Users
        # =================================================================
        print("\n👤 Loading users...")
        with open(csv_files['user'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=['user_id', 'name', 'email', 'password'])
            users_loaded = 0
            for row in reader:
                csv_id = int(row['user_id'])
                user = User(
                    name=row['name'].strip(),
                    email=row['email'].strip(),
                    password=row['password'].strip()
                )
                session.add(user)
                session.flush()
                user_id_map[csv_id] = user.user_id
                users_loaded += 1
            session.commit()
            print(f"   ✓ Loaded {users_loaded} users")

        # =================================================================
        # STEP 5: Load Sneakers (WITHOUT retailer_id per ER diagram)
        # =================================================================
        print("\n👟 Loading sneakers (without retailer_id)...")
        with open(csv_files['sneaker'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=[
                'sneaker_id', 'name', 'sku', 'release_year', 'colorway',
                'available_sizes', 'price', 'ratings', 'brand_id'
            ])
            sneakers_loaded = 0
            for row in reader:
                try:
                    csv_sneaker_id = int(row['sneaker_id'])
                    csv_brand_id = int(row['brand_id'])

                    # Map CSV IDs to database IDs
                    if csv_brand_id not in brand_id_map:
                        print(f"   ⚠ Warning: Brand ID {csv_brand_id} not found, skipping sneaker {row['name']}")
                        continue

                    sneaker = Sneaker(
                        name=row['name'].strip(),
                        sku=row['sku'].strip(),
                        release_date=row['release_year'].strip() if row['release_year'] else None,
                        colorway=row['colorway'].strip() if row['colorway'] else None,
                        available_sizes=row['available_sizes'].strip() if row['available_sizes'] else None,
                        price=float(row['price']),
                        ratings=int(row['ratings']) if row['ratings'] else None,
                        brand_id=brand_id_map[csv_brand_id]
                        # NO retailer_id - this is the key change per ER diagram!
                    )
                    session.add(sneaker)
                    session.flush()
                    sneaker_id_map[csv_sneaker_id] = sneaker.sneaker_id
                    sneakers_loaded += 1

                except (ValueError, KeyError) as e:
                    print(f"   ⚠ Warning: Error loading sneaker {row.get('name', 'unknown')}: {e}")
                    continue

            session.commit()
            print(f"   ✓ Loaded {sneakers_loaded} sneakers")

        # =================================================================
        # STEP 6: Load Price History
        # =================================================================
        print("\n📊 Loading price history...")
        with open(csv_files['price_history'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=['price_id', 'sneaker_id', 'price', 'timestamp'])
            prices_loaded = 0
            for row in reader:
                try:
                    csv_sneaker_id = int(row['sneaker_id'])

                    # Map CSV sneaker ID to database ID
                    if csv_sneaker_id not in sneaker_id_map:
                        continue  # Skip if sneaker wasn't loaded

                    # Parse timestamp (format: "2025-10-06 00:00:00")
                    timestamp_str = row['timestamp'].strip()
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                    price_history = PriceHistory(
                        sneaker_id=sneaker_id_map[csv_sneaker_id],
                        price=float(row['price']),
                        timestamp=timestamp
                    )
                    session.add(price_history)
                    prices_loaded += 1

                    # Commit in batches for better performance
                    if prices_loaded % 100 == 0:
                        session.commit()

                except (ValueError, KeyError) as e:
                    print(f"   ⚠ Warning: Error loading price history: {e}")
                    continue

            session.commit()
            print(f"   ✓ Loaded {prices_loaded} price history records")

        # =================================================================
        # STEP 7: Generate Favorites (M:N relationship)
        # =================================================================
        print("\n❤️  Generating sample favorites...")
        favorites_created = 0

        # Create some random favorites for each user
        if user_id_map and sneaker_id_map:
            for csv_user_id, db_user_id in user_id_map.items():
                # Each user favorites 3-8 random sneakers
                num_favorites = random.randint(3, min(8, len(sneaker_id_map)))
                random_sneakers = random.sample(list(sneaker_id_map.values()), num_favorites)

                for db_sneaker_id in random_sneakers:
                    try:
                        favorite = Favorites(
                            user_id=db_user_id,
                            sneaker_id=db_sneaker_id
                        )
                        session.add(favorite)
                        favorites_created += 1
                    except Exception:
                        # Skip if duplicate (unlikely but possible)
                        continue

            session.commit()
            print(f"   ✓ Created {favorites_created} favorite relationships")

        # =================================================================
        # COMPLETION SUMMARY
        # =================================================================
        print("\n" + "="*60)
        print("✅ Database seeding completed successfully!")
        print("="*60)
        print(f"   • {len(retailer_id_map)} retailers")
        print(f"   • {len(brand_id_map)} brands (each with retailer)")
        print(f"   • {len(user_id_map)} users")
        print(f"   • {len(sneaker_id_map)} sneakers (retailer via brand)")
        print(f"   • {prices_loaded} price history points")
        print(f"   • {favorites_created} user favorites")
        print("="*60)
        print("\n🎯 Schema now matches ER diagram EXACTLY:")
        print("   ✓ Brand → Retailer (with total participation)")
        print("   ✓ Sneaker → Brand (retailer inherited)")
        print("   ✓ User ↔ Sneaker (M:N via favorites)")
        print("   ✓ Sneaker → Price History (1:N)")
        print("="*60)


if __name__ == "__main__":
    seed_from_csv()
