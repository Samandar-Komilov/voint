from aiogram.filters import Command, CommandStart
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from sqlalchemy import select, exists

from database.database import get_db
from database.db_utils import is_user_admin, is_user_exists
from database.models import User


router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    async for session in get_db():
        async with session.begin():
            # Check if the user already exists
            user_exists = await is_user_exists(session, message.from_user.id)

            if not user_exists:
                # Check if the User table is empty
                db_not_empty = await session.execute(select(exists().where(User.id != None)))
                is_db_empty = not db_not_empty.scalar()

                # If the database is empty, make the first user an admin
                new_user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    is_admin=is_db_empty  # Set as admin if it's the first user
                )
                session.add(new_user)
            else:
                await message.answer("You have already been registered. Feel free to use the bot.")
            
            # Commit the changes to save the new user
            await session.commit()

    await message.answer("Welcome! Use /help for available commands.")

@router.message(Command("help"))
async def help_handler(message: types.Message):
    async for session in get_db():
        async with session.begin():
            result = await session.execute(
                select(User).filter_by(telegram_id=message.from_user.id, is_admin=True)
            )
            admin_user = result.scalar()

            if admin_user:
                admin_commands = """
                Admin Commands:
                /create_question <text> - Create a new question
                /edit_question <id> <new_text> - Edit a question
                /delete_question <id> - Delete a question
                /add_response <question_id> <text> [send as image] - Add a response
                /list_questions - List all questions
                """
                await message.answer(admin_commands)
            else:
                await message.answer("Use /list_questions to see questions.")