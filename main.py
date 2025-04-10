from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.main import router as api_router
from src.database.database import init_db
from src.database.import_data import import_customer_data, import_product_data
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multi-Agent E-Commerce Recommendation System",
    description="A sophisticated recommendation system using multiple AI agents",
    version="1.0.0"
)

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting application initialization...")
    
    # Initialize database
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully!")
    
    # Import dataset
    try:
        logger.info("Starting dataset import...")
        logger.info("Importing customer data...")
        await import_customer_data()
        logger.info("Importing product data...")
        await import_product_data()
        logger.info("Dataset imported successfully!")
    except Exception as e:
        logger.error(f"Error importing dataset: {str(e)}", exc_info=True)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Multi-Agent E-Commerce Recommendation System",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 