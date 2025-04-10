from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Product, Customer
import json
import os

def init_db():
    # Get absolute path for SQLite database
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'ai_mart.db')
    DATABASE_URL = f"sqlite:///{db_path}"
    
    # Create database engine
    engine = create_engine(DATABASE_URL)
    
    # Drop all existing tables
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create default customer
        default_customer = Customer(
            id=1,
            name="Default Customer",
            email="customer@example.com",
            preferences=json.dumps({
                "favorite_categories": ["Electronics", "Fashion", "Home"],
                "price_range": {"min": 0, "max": 5000},
                "brands": ["Apple", "Samsung", "Nike"]
            })
        )
        db.add(default_customer)
        
        # Create sample products
        sample_products = [
            {
                "name": "Laptop Pro X",
                "description": "High-performance laptop with 16GB RAM and 512GB SSD",
                "price": 1299.99,
                "category": "Electronics",
                "subcategory": "Laptops",
                "brand": "TechPro",
                "average_rating": 4.5,
                "review_sentiment": 0.8,
                "seasonal_availability": "all_year",
                "geographical_availability": "worldwide",
                "similar_products": json.dumps([2, 3]),
                "recommendation_frequency": 0.9,
                "image_url": "https://via.placeholder.com/300"
            },
            {
                "name": "Smart Watch Elite",
                "description": "Advanced smartwatch with health monitoring features",
                "price": 299.99,
                "category": "Electronics",
                "subcategory": "Wearables",
                "brand": "TechPro",
                "average_rating": 4.3,
                "review_sentiment": 0.7,
                "seasonal_availability": "all_year",
                "geographical_availability": "worldwide",
                "similar_products": json.dumps([1, 3]),
                "recommendation_frequency": 0.8,
                "image_url": "https://via.placeholder.com/300"
            },
            {
                "name": "Premium Headphones",
                "description": "Noise-cancelling wireless headphones",
                "price": 199.99,
                "category": "Electronics",
                "subcategory": "Audio",
                "brand": "SoundMax",
                "average_rating": 4.7,
                "review_sentiment": 0.9,
                "seasonal_availability": "all_year",
                "geographical_availability": "worldwide",
                "similar_products": json.dumps([1, 2]),
                "recommendation_frequency": 0.85,
                "image_url": "https://via.placeholder.com/300"
            },
            {
                "name": "Designer Handbag",
                "description": "Luxury leather handbag with gold accents",
                "price": 599.99,
                "category": "Fashion",
                "subcategory": "Bags",
                "brand": "LuxStyle",
                "average_rating": 4.8,
                "review_sentiment": 0.9,
                "seasonal_availability": "all_year",
                "geographical_availability": "worldwide",
                "similar_products": json.dumps([5, 6]),
                "recommendation_frequency": 0.7,
                "image_url": "https://example.com/handbag.jpg"
            },
            {
                "name": "Smart Home Hub",
                "description": "Central control for all your smart home devices",
                "price": 149.99,
                "category": "Home",
                "subcategory": "Smart Home",
                "brand": "HomeTech",
                "average_rating": 4.4,
                "review_sentiment": 0.75,
                "seasonal_availability": "all_year",
                "geographical_availability": "worldwide",
                "similar_products": json.dumps([6]),
                "recommendation_frequency": 0.8,
                "image_url": "https://example.com/smarthub.jpg"
            },
            {
                "name": "4K Smart TV",
                "description": "65-inch 4K Smart TV with HDR",
                "price": 899.99,
                "category": "Electronics",
                "subcategory": "TVs",
                "brand": "VisionTech",
                "average_rating": 4.6,
                "review_sentiment": 0.85,
                "seasonal_availability": "all_year",
                "geographical_availability": "worldwide",
                "similar_products": json.dumps([1, 3]),
                "recommendation_frequency": 0.75,
                "image_url": "https://example.com/tv.jpg"
            }
        ]
        
        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
        
        # Commit all changes
        db.commit()
        print("Database initialized successfully with sample data!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 