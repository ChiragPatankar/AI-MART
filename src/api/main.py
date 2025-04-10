from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_db
from src.agents import (
    CustomerAgent,
    ProductAgent,
    RecommendationAgent,
    FeedbackAgent,
    CartAgent
)
from src.database.database_manager import DatabaseManager
from typing import Optional, Dict, Any
import time
import logging
import uvicorn
from sqlalchemy import select, func
from src.database.models import Customer, Product, Recommendation, Feedback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="AI-Mart API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create router
router = APIRouter()

# Initialize database manager
db_manager = DatabaseManager()

# Initialize agents
customer_agent = CustomerAgent("customer_agent_1", db_manager)
product_agent = ProductAgent("product_agent_1", db_manager)
recommendation_agent = RecommendationAgent("recommendation_agent_1", db_manager)
feedback_agent = FeedbackAgent("feedback_agent_1", db_manager)
cart_agent = CartAgent("cart_agent_1", db_manager)

@router.get("/")
async def root():
    return {"message": "Welcome to AI-Mart API"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

# Cart endpoints
@router.get("/cart/")
async def get_cart(db: AsyncSession = Depends(get_db)):
    start_time = time.time()
    try:
        data = {"action_type": "get_cart"}
        result = await cart_agent.process(data, db)
        end_time = time.time()
        logger.info(f"Cart GET API response time: {(end_time - start_time) * 1000:.2f}ms")
        return result
    except Exception as e:
        end_time = time.time()
        logger.error(f"Cart GET API error after {(end_time - start_time) * 1000:.2f}ms: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cart/")
async def add_to_cart(data: dict, db: AsyncSession = Depends(get_db)):
    try:
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)
        
        if not product_id:
            raise HTTPException(status_code=400, detail="Product ID is required")
            
        cart_data = {
            "action_type": "add_to_cart",
            "product_id": product_id,
            "quantity": quantity
        }
        result = await cart_agent.process(cart_data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/cart/{product_id}")
async def update_cart_item(product_id: int, quantity: int, db: AsyncSession = Depends(get_db)):
    try:
        data = {
            "action_type": "update_quantity",
            "product_id": product_id,
            "quantity": quantity
        }
        result = await cart_agent.process(data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/cart/{product_id}")
async def remove_from_cart(product_id: int, db: AsyncSession = Depends(get_db)):
    try:
        data = {
            "action_type": "remove_from_cart",
            "product_id": product_id
        }
        result = await cart_agent.process(data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Product endpoints
@router.get("/products/")
async def get_products(
    action: str = "search_products",  # Set default action
    query: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = "relevance",
    page: Optional[int] = Query(1, ge=1),
    limit: Optional[int] = Query(12, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    try:
        data = {
            "action_type": action,  # Add action_type to match agent requirements
            "query": query,
            "category": category,
            "sort_by": sort_by,
            "page": page,
            "limit": limit
        }
        result = await product_agent.process(data, db)
        end_time = time.time()
        logger.info(f"Products API response time: {(end_time - start_time) * 1000:.2f}ms")
        return result
    except Exception as e:
        end_time = time.time()
        logger.error(f"Products API error after {(end_time - start_time) * 1000:.2f}ms: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/products/")
async def handle_product_request(action: str, data: dict, db: AsyncSession = Depends(get_db)):
    try:
        result = await product_agent.process(action, data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Customer endpoints
@router.get("/customers/")
async def get_customer_profile(
    action: str = Query(...),
    customer_id: str = "C1000",  # Default customer ID
    db: AsyncSession = Depends(get_db)
):
    try:
        data = {
            "action_type": action,
            "customer_id": customer_id
        }
        result = await customer_agent.process(data, db)
        return result
    except Exception as e:
        logger.error(f"Error in customer profile endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/customers/")
async def handle_customer_request(
    action: str,
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    try:
        data["action_type"] = action
        result = await customer_agent.process(data, db)
        return result
    except Exception as e:
        logger.error(f"Error in customer request endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Recommendation endpoints
@router.post("/recommendations/")
async def post_recommendations(
    data: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    try:
        result = await recommendation_agent.process(data, db)
        end_time = time.time()
        logger.info(f"Recommendations API response time: {(end_time - start_time) * 1000:.2f}ms")
        return result
    except Exception as e:
        end_time = time.time()
        logger.error(f"Recommendations API error after {(end_time - start_time) * 1000:.2f}ms: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/recommendations/")
async def get_recommendations(
    action: str = "get_recommendations",
    customer_id: Optional[int] = None,
    algorithm: str = "hybrid",
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    try:
        data = {
            "action_type": action,
            "customer_id": customer_id or 1,
            "algorithm": algorithm
        }
        result = await recommendation_agent.process(data, db)
        end_time = time.time()
        logger.info(f"Recommendations API response time: {(end_time - start_time) * 1000:.2f}ms")
        return result
    except Exception as e:
        end_time = time.time()
        logger.error(f"Recommendations API error after {(end_time - start_time) * 1000:.2f}ms: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Feedback endpoints
@router.post("/feedback/")
async def handle_feedback(feedback_type: str, data: dict, db: AsyncSession = Depends(get_db)):
    try:
        result = await feedback_agent.process(feedback_type, data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Admin endpoints
@router.get("/admin/stats")
async def get_system_stats(
    time_range: str = "7d",
    db: AsyncSession = Depends(get_db)
):
    try:
        # Get total users
        users_query = select(func.count()).select_from(Customer)
        total_users_result = await db.execute(users_query)
        total_users = total_users_result.scalar() or 0

        # Get total products
        products_query = select(func.count()).select_from(Product)
        total_products_result = await db.execute(products_query)
        total_products = total_products_result.scalar() or 0

        # Get total recommendations
        recommendations_query = select(func.count()).select_from(Recommendation)
        total_recommendations_result = await db.execute(recommendations_query)
        total_recommendations = total_recommendations_result.scalar() or 0

        # Get system configuration
        system_stats = {
            "total_users": total_users,
            "total_products": total_products,
            "total_recommendations": total_recommendations,
            "min_confidence": 0.5,  # Default values
            "max_recommendations": 10
        }
        
        return system_stats
    except Exception as e:
        logger.error(f"Error fetching system stats: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/admin/algorithm-stats")
async def get_algorithm_stats(
    time_range: str = "7d",
    db: AsyncSession = Depends(get_db)
):
    try:
        # Get algorithm usage counts
        usage_query = select(
            Recommendation.algorithm,
            func.count().label('usage_count'),
            func.avg(Feedback.rating).label('average_rating')
        ).outerjoin(
            Feedback, Recommendation.id == Feedback.recommendation_id
        ).group_by(
            Recommendation.algorithm
        )
        
        result = await db.execute(usage_query)
        algorithm_data = {}
        for row in result.fetchall():
            algorithm_data[row.algorithm] = {
                'usage_count': row.usage_count,
                'average_rating': float(row.average_rating or 0)
            }

        # Prepare stats with default values for missing algorithms
        default_algorithms = ['hybrid', 'collaborative', 'content', 'sequential']
        stats = []
        for algo in default_algorithms:
            data = algorithm_data.get(algo, {'usage_count': 0, 'average_rating': 0})
            stats.append({
                'algorithm': algo,
                'usage_count': data['usage_count'],
                'success_rate': 0.7 + (0.1 * default_algorithms.index(algo)),  # Default success rates
                'average_rating': data['average_rating'] or (4.0 - (0.2 * default_algorithms.index(algo)))  # Default ratings
            })

        return stats
    except Exception as e:
        logger.error(f"Error fetching algorithm stats: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Include router in app
app.include_router(router, prefix="/api")

# Run the application
if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True) 