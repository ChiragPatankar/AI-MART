from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .models import (
    Customer,
    Product,
    BrowsingHistory,
    Purchase,
    Recommendation,
    CustomerEmbedding,
    ProductEmbedding,
    CustomerSegment,
    CustomerSegmentMembership,
    Cart,
    Feedback,
    Base
)
import json
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import os

class DatabaseManager:
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ai_mart.db")
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = logging.getLogger(__name__)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

    async def get_products(self, session, limit=10, offset=0, category=None):
        query = select(Product)
        if category:
            query = query.where(Product.category == category)
        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_cart_items(self, session, customer_id):
        query = (
            select(Cart, Product)
            .join(Product)
            .where(Cart.customer_id == customer_id)
        )
        result = await session.execute(query)
        return result.all()

    async def add_to_cart(self, session, customer_id, product_id, quantity=1):
        cart_item = Cart(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity
        )
        session.add(cart_item)
        await session.commit()
        return cart_item

    async def update_cart_quantity(self, session, customer_id, product_id, quantity):
        cart_item = await session.execute(
            select(Cart)
            .where(Cart.customer_id == customer_id)
            .where(Cart.product_id == product_id)
        )
        cart_item = cart_item.scalar_one_or_none()
        if cart_item:
            cart_item.quantity = quantity
            await session.commit()
        return cart_item

    async def remove_from_cart(self, session, customer_id, product_id):
        cart_item = await session.execute(
            select(Cart)
            .where(Cart.customer_id == customer_id)
            .where(Cart.product_id == product_id)
        )
        cart_item = cart_item.scalar_one_or_none()
        if cart_item:
            await session.delete(cart_item)
            await session.commit()
        return True

    async def get_customer_by_id(self, session, customer_id):
        result = await session.execute(
            select(Customer).where(Customer.id == customer_id)
        )
        return result.scalar_one_or_none()

    async def get_product_by_id(self, session, product_id):
        result = await session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_recommendations(self, session, customer_id, limit=10):
        query = (
            select(Recommendation, Product)
            .join(Product)
            .where(Recommendation.customer_id == customer_id)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.all()

    async def add_feedback(self, session, customer_id, feedback_type, rating, comment):
        feedback = Feedback(
            customer_id=customer_id,
            type=feedback_type,
            rating=rating,
            comment=comment
        )
        session.add(feedback)
        await session.commit()
        return feedback

    async def get_session(self) -> AsyncSession:
        """Get a database session."""
        async for session in get_db():
            return session

    async def close(self):
        """Close all sessions."""
        pass  # Sessions are automatically closed by the context manager

    # Customer operations
    async def get_customer(self, session: AsyncSession, customer_id: int):
        """Get a customer by ID."""
        return await session.get(Customer, customer_id)

    async def create_customer(self, session: AsyncSession, customer_data: dict):
        """Create a new customer."""
        customer = Customer(**customer_data)
        session.add(customer)
        await session.commit()
        return customer

    # Product operations
    async def get_product(self, session: AsyncSession, product_id: int):
        """Get a product by ID."""
        return await session.get(Product, product_id)

    async def create_product(self, session: AsyncSession, product_data: dict):
        """Create a new product."""
        product = Product(**product_data)
        session.add(product)
        await session.commit()
        return product

    # Browsing history operations
    async def add_browsing_history(self, session: AsyncSession, customer_id: int, product_id: int):
        """Add a browsing history entry."""
        history = BrowsingHistory(customer_id=customer_id, product_id=product_id)
        session.add(history)
        await session.commit()
        return history

    # Purchase operations
    async def add_purchase(self, session: AsyncSession, customer_id: int, product_id: int, quantity: int):
        """Add a purchase record."""
        purchase = Purchase(customer_id=customer_id, product_id=product_id, quantity=quantity)
        session.add(purchase)
        await session.commit()
        return purchase

    # Recommendation operations
    async def add_recommendation(self, session: AsyncSession, customer_id: int, product_id: int, score: float):
        """Add a recommendation."""
        recommendation = Recommendation(customer_id=customer_id, product_id=product_id, score=score)
        session.add(recommendation)
        await session.commit()
        return recommendation

    # Embedding operations
    async def update_customer_embedding(self, session: AsyncSession, customer_id: int, embedding: list):
        """Update customer embedding."""
        customer_embedding = CustomerEmbedding(customer_id=customer_id, embedding=embedding)
        session.add(customer_embedding)
        await session.commit()
        return customer_embedding

    async def update_product_embedding(self, session: AsyncSession, product_id: int, embedding: list):
        """Update product embedding."""
        product_embedding = ProductEmbedding(product_id=product_id, embedding=embedding)
        session.add(product_embedding)
        await session.commit()
        return product_embedding

    # Customer segment operations
    async def create_customer_segment(self, session: AsyncSession, name: str, description: str):
        """Create a customer segment."""
        segment = CustomerSegment(name=name, description=description)
        session.add(segment)
        await session.commit()
        return segment

    async def add_customer_to_segment(self, session: AsyncSession, customer_id: int, segment_id: int):
        """Add a customer to a segment."""
        membership = CustomerSegmentMembership(customer_id=customer_id, segment_id=segment_id)
        session.add(membership)
        await session.commit()
        return membership

    def add_customer(self, customer_data: Dict[str, Any]) -> int:
        """Add a new customer to the database"""
        session = self.get_session()
        try:
            customer = Customer(**customer_data)
            session.add(customer)
            session.commit()
            return customer.customer_id
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding customer: {str(e)}")
            raise
        finally:
            session.close()

    def add_product(self, product_data: Dict[str, Any]) -> int:
        """Add a new product to the database"""
        session = self.get_session()
        try:
            product = Product(**product_data)
            session.add(product)
            session.commit()
            return product.product_id
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding product: {str(e)}")
            raise
        finally:
            session.close()

    def log_browsing_event(self, customer_id: int, product_id: int, duration: int, actions: Dict[str, Any]):
        """Record a product browsing event"""
        session = self.get_session()
        try:
            browsing_event = BrowsingHistory(
                customer_id=customer_id,
                product_id=product_id,
                duration_seconds=duration,
                page_actions=json.dumps(actions)
            )
            session.add(browsing_event)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error logging browsing event: {str(e)}")
            raise
        finally:
            session.close()

    def log_purchase(self, customer_id: int, items: List[Dict[str, Any]], total_amount: float):
        """Record a customer purchase"""
        session = self.get_session()
        try:
            purchase = Purchase(
                customer_id=customer_id,
                items=json.dumps(items),
                total_amount=total_amount
            )
            session.add(purchase)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error logging purchase: {str(e)}")
            raise
        finally:
            session.close()

    def update_customer_embedding(self, customer_id: int, embedding: np.ndarray):
        """Update the vector representation of a customer"""
        session = self.get_session()
        try:
            embedding_bytes = embedding.tobytes()
            customer_embedding = CustomerEmbedding(
                customer_id=customer_id,
                embedding=embedding_bytes
            )
            session.merge(customer_embedding)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error updating customer embedding: {str(e)}")
            raise
        finally:
            session.close()

    def get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        """Get complete customer profile with history and preferences"""
        session = self.get_session()
        try:
            customer = session.query(Customer).get(customer_id)
            if not customer:
                return None
            
            profile = {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'email': customer.email,
                'demographics': customer.demographics,
                'registration_date': customer.registration_date,
                'last_active': customer.last_active,
                'browsing_history': [
                    {
                        'product_id': history.product_id,
                        'view_time': history.view_time,
                        'duration': history.duration_seconds,
                        'actions': json.loads(history.page_actions)
                    }
                    for history in customer.browsing_history
                ],
                'purchases': [
                    {
                        'purchase_id': purchase.purchase_id,
                        'timestamp': purchase.timestamp,
                        'total_amount': purchase.total_amount,
                        'items': json.loads(purchase.items)
                    }
                    for purchase in customer.purchases
                ],
                'cart_items': [
                    {
                        'product_id': item.product_id,
                        'quantity': item.quantity,
                        'added_timestamp': item.added_timestamp
                    }
                    for item in customer.cart_items
                ]
            }
            return profile
        finally:
            session.close()

    def get_similar_products(self, product_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Find similar products based on embeddings"""
        session = self.get_session()
        try:
            # This is a placeholder implementation
            # In a real system, you would use vector similarity search
            product = session.query(Product).get(product_id)
            if not product:
                return []
            
            similar_products = session.query(Product)\
                .filter(Product.category == product.category)\
                .limit(limit)\
                .all()
            
            return [
                {
                    'product_id': p.product_id,
                    'name': p.name,
                    'category': p.category,
                    'price': p.price
                }
                for p in similar_products
            ]
        finally:
            session.close()

    def log_recommendations(self, customer_id: int, recommendations: List[Dict[str, Any]], algorithm: str):
        """Record recommendations made to a customer"""
        session = self.get_session()
        try:
            for rec in recommendations:
                recommendation = Recommendation(
                    customer_id=customer_id,
                    product_id=rec['product_id'],
                    score=rec['score'],
                    algorithm=algorithm
                )
                session.add(recommendation)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error logging recommendations: {str(e)}")
            raise
        finally:
            session.close()

    def update_recommendation_feedback(self, recommendation_id: int, clicked: bool):
        """Update recommendation feedback"""
        session = self.get_session()
        try:
            recommendation = session.query(Recommendation).get(recommendation_id)
            if recommendation:
                recommendation.was_shown = True
                recommendation.was_clicked = clicked
                session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error updating recommendation feedback: {str(e)}")
            raise
        finally:
            session.close() 