from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from database.models import Base, User
from sqlalchemy import select


# Create asynchronous SQLAlchemy engine
engine = create_async_engine(DATABASE_URL)

# Create a configured "Session" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    # Dependency to get a database session
    async with AsyncSessionLocal() as session:
        yield session