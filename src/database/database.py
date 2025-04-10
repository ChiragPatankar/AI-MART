from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Get absolute path for SQLite database
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'ai_mart.db')
DATABASE_URL = f"sqlite:///{db_path}"

# Convert SQLite URL to async SQLite URL
if DATABASE_URL.startswith('sqlite:///'):
    DATABASE_URL = DATABASE_URL.replace('sqlite:///', 'sqlite+aiosqlite:///', 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL echo to prevent auto-reload loop
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initialize the database by creating tables if they don't exist."""
    async with engine.begin() as conn:
        # Create tables without dropping existing ones
        await conn.run_sync(Base.metadata.create_all)  # Create tables if they don't exist

async def get_db():
    """Get a database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 