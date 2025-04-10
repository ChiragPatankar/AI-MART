import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_csv_files():
    """Check CSV file contents"""
    try:
        # Get the absolute path to the CSV files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        product_csv = os.path.join(current_dir, 'product_recommendation_data.csv')
        customer_csv = os.path.join(current_dir, 'customer_data_collection.csv')
        
        # Check product data
        if os.path.exists(product_csv):
            df = pd.read_csv(product_csv)
            logger.info(f"Product CSV found with {len(df)} rows")
            logger.info("First row of product data:")
            logger.info(df.iloc[0].to_dict())
            logger.info(f"Columns: {df.columns.tolist()}")
        else:
            logger.error(f"Product CSV not found at: {product_csv}")
        
        # Check customer data
        if os.path.exists(customer_csv):
            df = pd.read_csv(customer_csv)
            logger.info(f"Customer CSV found with {len(df)} rows")
            logger.info("First row of customer data:")
            logger.info(df.iloc[0].to_dict())
            logger.info(f"Columns: {df.columns.tolist()}")
        else:
            logger.error(f"Customer CSV not found at: {customer_csv}")
            
    except Exception as e:
        logger.error(f"Error checking CSV files: {str(e)}", exc_info=True)

if __name__ == "__main__":
    check_csv_files() 