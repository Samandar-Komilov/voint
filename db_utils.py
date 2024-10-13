from models import Base, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base, get_db


async def is_user_exists(session, user_id):
    # Check if the user exists in the database
    result = await session.execute(select(User).filter_by(telegram_id=user_id))
    return result.scalar() is not None


async def is_user_admin(message, user_id: int):
    async for session in get_db():
        async with session.begin():
            # Check if user exists with given ID
            user = await session.get(User, user_id)
            if user:
                # Check if user has is_admin set to True
                return user.is_admin  # Assuming is_admin is a boolean field in User
            else:
                return False  # User doesn't exist
            

async def is_table_empty(session: AsyncSession, model_class):
    result = await session.execute(select(model_class).limit(1))
    return result.scalar() is None