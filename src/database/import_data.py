import pandas as pd
import json
from sqlalchemy import select
from src.database.models import Base, Customer, Product, BrowsingHistory, Purchase
import os
from dotenv import load_dotenv
from src.database.database import AsyncSessionLocal, init_db
import asyncio
import logging
import ast

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def clean_list_string(s):
    """Convert string representation of list to actual list"""
    try:
        # Remove quotes and brackets, then split
        s = s.strip('[]').replace("'", "")
        return [item.strip() for item in s.split(',')]
    except Exception as e:
        logger.warning(f"Error cleaning list string: {str(e)}")
        return []

async def ensure_tables_exist():
    """Ensure database tables are created"""
    logger.info("Creating database tables...")
    try:
        await init_db()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}", exc_info=True)
        raise

async def clear_existing_data():
    """Clear all existing data from the database"""
    logger.info("Clearing existing data...")
    try:
        async with AsyncSessionLocal() as session:
            # Delete all records from each table
            tables = [
                "feedback",
                "product_embeddings",
                "customer_embeddings",
                "customer_segment_memberships",
                "customer_segments",
                "recommendations",
                "cart",
                "purchases",
                "browsing_history",
                "products",
                "customers"
            ]
            
            for table in tables:
                try:
                    await session.execute(f"DELETE FROM {table}")
                    logger.info(f"Cleared table: {table}")
                except Exception as e:
                    logger.warning(f"Error clearing table {table}: {str(e)}")
            
            await session.commit()
            logger.info("All existing data cleared successfully")
    except Exception as e:
        logger.error(f"Error clearing existing data: {str(e)}", exc_info=True)
        raise

async def import_customer_data():
    """Import customer data from CSV"""
    logger.info("Starting customer data import...")
    try:
        # Get the absolute path to the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'customer_data_collection.csv')
        
        if not os.path.exists(csv_path):
            logger.error(f"Customer data file not found at: {csv_path}")
            return
            
        df = pd.read_csv(csv_path)
        logger.info(f"Found {len(df)} customer records to import")
        
        async with AsyncSessionLocal() as session:
            try:
                # Process each row
                for index, row in df.iterrows():
                    if index % 100 == 0:
                        logger.info(f"Processing customer record {index + 1}/{len(df)}")
                    
                    # Use the original customer ID format
                    customer_id = row['Customer_ID']
                    
                    # Check if customer already exists
                    stmt = select(Customer).where(Customer.id == customer_id)
                    result = await session.execute(stmt)
                    existing_customer = result.scalar_one_or_none()
                    
                    if existing_customer:
                        logger.debug(f"Customer {customer_id} already exists, skipping...")
                        continue
                    
                    # Parse browsing and purchase history
                    browsing_history = ast.literal_eval(row['Browsing_History']) if pd.notna(row['Browsing_History']) else []
                    purchase_history = ast.literal_eval(row['Purchase_History']) if pd.notna(row['Purchase_History']) else []
                    
                    # Create customer with full profile data
                    customer = Customer(
                        id=customer_id,
                        name=f"Customer {customer_id}",
                        email=f"customer{customer_id}@example.com",
                        preferences=json.dumps({
                            'age': int(row['Age']),
                            'gender': row['Gender'],
                            'location': row['Location'],
                            'segment': row['Customer_Segment'],
                            'avg_order_value': float(row['Avg_Order_Value']),
                            'browsing_history': browsing_history,
                            'purchase_history': purchase_history,
                            'holiday': row['Holiday'],
                            'season': row['Season']
                        })
                    )
                    session.add(customer)
                    
                    # Add browsing history
                    for category in browsing_history:
                        browsing = BrowsingHistory(
                            customer_id=customer_id,
                            category=category,
                            view_time=None,  # We don't have this data
                            duration_seconds=0,  # We don't have this data
                            page_actions=json.dumps({})  # We don't have this data
                        )
                        session.add(browsing)
                    
                    # Add purchase history
                    for item in purchase_history:
                        purchase = Purchase(
                            customer_id=customer_id,
                            items=json.dumps([item]),
                            total_amount=float(row['Avg_Order_Value']),  # Using average order value as placeholder
                            timestamp=None  # We don't have this data
                        )
                        session.add(purchase)
                    
                    # Commit every 100 records to avoid memory issues
                    if index > 0 and index % 100 == 0:
                        await session.commit()
                        logger.info(f"Committed {index} customer records")
                
                # Final commit for remaining records
                await session.commit()
                logger.info("Customer data imported successfully!")
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Error importing customer data: {str(e)}", exc_info=True)
                raise
                
    except Exception as e:
        logger.error(f"Error reading customer data CSV: {str(e)}", exc_info=True)
        raise

async def import_product_data():
    """Import product data from CSV"""
    logger.info("Starting product data import...")
    try:
        # Get the absolute path to the CSV file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'product_recommendation_data.csv')
        
        if not os.path.exists(csv_path):
            logger.error(f"Product data file not found at: {csv_path}")
            return
            
        df = pd.read_csv(csv_path)
        logger.info(f"Found {len(df)} product records to import")
        
        async with AsyncSessionLocal() as session:
            try:
                # Process each row
                for index, row in df.iterrows():
                    if index % 100 == 0:
                        logger.info(f"Processing product record {index + 1}/{len(df)}")
                    
                    # Use the original product ID format
                    product_id = row['Product_ID']
                    
                    # Check if product already exists
                    stmt = select(Product).where(Product.id == product_id)
                    result = await session.execute(stmt)
                    existing_product = result.scalar_one_or_none()
                    
                    if existing_product:
                        logger.debug(f"Product {product_id} already exists, skipping...")
                        continue
                    
                    # Create product with features as JSON string
                    features = {
                        'subcategory': row['Subcategory'],
                        'brand': row['Brand'],
                        'average_rating': float(row['Average_Rating_of_Similar_Products']),
                        'product_rating': float(row['Product_Rating']),
                        'sentiment_score': float(row['Customer_Review_Sentiment_Score']),
                        'holiday': row['Holiday'],
                        'season': row['Season'],
                        'location': row['Geographical_Location'],
                        'similar_products': clean_list_string(row['Similar_Product_List']),
                        'recommendation_probability': float(row['Probability_of_Recommendation'])
                    }
                    
                    product = Product(
                        id=product_id,
                        name=f"Product {product_id}",
                        description=f"{row['Category']} - {row['Subcategory']}",
                        price=float(row['Price']),
                        category=row['Category'],
                        features=json.dumps(features),
                        image_url='https://via.placeholder.com/300'  # Default placeholder image
                    )
                    session.add(product)
                    
                    # Commit every 1000 records to avoid memory issues
                    if index > 0 and index % 1000 == 0:
                        await session.commit()
                        logger.info(f"Committed {index} product records")
                
                # Final commit for remaining records
                await session.commit()
                logger.info("Product data imported successfully!")
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Error importing product data: {str(e)}", exc_info=True)
                raise
                
    except Exception as e:
        logger.error(f"Error reading product data CSV: {str(e)}", exc_info=True)
        raise

async def main():
    """Main function to run the import process"""
    try:
        # Ensure tables exist
        await ensure_tables_exist()
        
        # Clear existing data
        await clear_existing_data()
        
        # Import data
        await import_customer_data()
        await import_product_data()
        
        logger.info("Data import completed successfully!")
        
    except Exception as e:
        logger.error(f"Error importing data: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main()) 