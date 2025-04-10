from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, BLOB, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    preferences = Column(Text)  # JSON string of preferences
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    browsing_history = relationship("BrowsingHistory", back_populates="customer")
    purchases = relationship("Purchase", back_populates="customer")
    recommendations = relationship("Recommendation", back_populates="customer")
    cart_items = relationship("Cart", back_populates="customer")
    segment_memberships = relationship("CustomerSegmentMembership", back_populates="customer")
    embedding = relationship("CustomerEmbedding", back_populates="customer", uselist=False)
    feedback = relationship("Feedback", back_populates="customer")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    price = Column(Float)
    category = Column(String(50))
    features = Column(Text)  # JSON string of features
    image_url = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    cart_items = relationship("Cart", back_populates="product")
    recommendations = relationship("Recommendation", back_populates="product")
    embedding = relationship("ProductEmbedding", back_populates="product", uselist=False)

class BrowsingHistory(Base):
    __tablename__ = 'browsing_history'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'))
    category = Column(String(50))
    view_time = Column(DateTime)
    duration_seconds = Column(Integer)
    page_actions = Column(Text)  # JSON string of actions
    
    # Relationships
    customer = relationship("Customer", back_populates="browsing_history")

class Purchase(Base):
    __tablename__ = 'purchases'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'))
    items = Column(Text)  # JSON string of items
    total_amount = Column(Float)
    timestamp = Column(DateTime)
    
    # Relationships
    customer = relationship("Customer", back_populates="purchases")

class Cart(Base):
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'))
    product_id = Column(String(10), ForeignKey('products.id'))
    quantity = Column(Integer, default=1)
    added_timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class Recommendation(Base):
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'))
    product_id = Column(String(10), ForeignKey('products.id'))
    algorithm = Column(String(50))
    score = Column(Float)
    explanation = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    clicked = Column(Boolean, default=False)
    purchased = Column(Boolean, default=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="recommendations")
    product = relationship("Product", back_populates="recommendations")

class CustomerSegment(Base):
    __tablename__ = 'customer_segments'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    description = Column(Text)
    criteria = Column(Text)  # JSON string of segment criteria
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    members = relationship("CustomerSegmentMembership", back_populates="segment")

class CustomerSegmentMembership(Base):
    __tablename__ = 'customer_segment_memberships'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'))
    segment_id = Column(Integer, ForeignKey('customer_segments.id'))
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="segment_memberships")
    segment = relationship("CustomerSegment", back_populates="members")

class CustomerEmbedding(Base):
    __tablename__ = 'customer_embeddings'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'), unique=True)
    embedding = Column(BLOB)  # Binary vector representation
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="embedding")

class ProductEmbedding(Base):
    __tablename__ = 'product_embeddings'
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(10), ForeignKey('products.id'), unique=True)
    embedding = Column(BLOB)  # Binary vector representation
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="embedding")

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(10), ForeignKey('customers.id'))
    type = Column(String(50))  # recommendation_feedback, system_feedback, etc.
    rating = Column(Integer)
    comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="feedback") 