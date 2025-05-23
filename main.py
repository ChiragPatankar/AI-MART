from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.main import router as api_router
from src.database.database import init_db
from src.database.import_data import import_customer_data, import_product_data
import asyncio
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multi-Agent E-Commerce Recommendation System",
    description="A sophisticated recommendation system using multiple AI agents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Serve static React frontend
app.mount("/static", StaticFiles(directory="frontend_build/static"), name="static")

@app.get("/")
def serve_react_app():
    return FileResponse("frontend_build/index.html")

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

@app.get("/status")
async def root_status():
    return {
        "message": "Welcome to the Multi-Agent E-Commerce Recommendation System",
        "status": "operational"
    }

# Uvicorn entry point for local dev (not used in Hugging Face Docker Spaces)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
