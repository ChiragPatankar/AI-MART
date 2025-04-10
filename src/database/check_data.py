from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Product
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Check if database tables exist and contain data"""
    # Get absolute path for SQLite database
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'ai_mart.db')
    DATABASE_URL = f"sqlite:///{db_path}"
    
    # Create engine and session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # Check products table
        count = session.query(Product).count()
        logger.info(f"Found {count} products in database")

        if count > 0:
            # Get sample product
            product = session.query(Product).first()
            if product:
                logger.info(f"Sample product: {product.name}, Category: {product.category}, Price: ${product.price}")
        
        return count

    except Exception as e:
        logger.error(f"Error checking database: {str(e)}")
        return 0
    finally:
        session.close()

if __name__ == "__main__":
    count = check_database()
    if count == 0:
        logger.warning("No products found in database. Please run init_db.py to populate the database.") 