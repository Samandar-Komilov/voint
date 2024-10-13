from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from sqlalchemy import select, exists
from sqlalchemy.exc import NoResultFound
from io import BytesIO
import logging

from config import BOT_TOKEN, ADMIN_ID
from database import init_db, get_db
from db_utils import is_user_admin, is_user_exists
from models import User, Question, Response


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.startup()
async def on_startup():
    await init_db()
    logging.info("Database connected and tables created.")


@dp.message(Command("start"))
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

@dp.message(Command("help"))
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

# @dp.message(Command("create_question"))
# async def create_question_handler(message: types.Message):
#     if message.from_user.id != ADMIN_ID:
#         return
#     question_text = message.text.split(maxsplit=1)[1]
#     async for session in get_db():
#         async with session.begin():
#             new_question = Question(question_text=question_text)
#             session.add(new_question)
#         await message.answer(f"Question '{question_text}' created.")

# @dp.message(content_types=['photo'])
# async def add_response_with_image_handler(message: types.Message):
#     if message.from_user.id != ADMIN_ID:
#         return
#     if not message.caption:
#         await message.answer("Provide a caption in '<question_id> <response>' format.")
#         return

#     # Extract question_id and response_text
#     caption_parts = message.caption.split(maxsplit=1)
#     if len(caption_parts) < 2:
#         await message.answer("Usage: Send an image with caption '<question_id> <response_text>'")
#         return

#     question_id, response_text = caption_parts[0], caption_parts[1]

#     try:
#         question_id = int(question_id)
#     except ValueError:
#         await message.answer("Invalid question ID.")
#         return

#     # Download the image data
#     photo = message.photo[-1]
#     photo_file = await bot.download(photo.file_id)
#     image_data = BytesIO(photo_file.read()).read()

#     async for session in get_db():
#         async with session.begin():
#             question = await session.get(Question, question_id)
#             if not question:
#                 await message.answer(f"No question found with ID {question_id}.")
#                 return

#             new_response = Response(
#                 question_id=question_id,
#                 response_text=response_text,
#                 image_data=image_data
#             )
#             session.add(new_response)
#         await message.answer(f"Response with image added to question {question_id}.")

# @dp.message(Command("list_questions"))
# async def list_questions_handler(message: types.Message):
#     async for session in get_db():
#         async with session.begin():
#             questions = await session.execute(select(Question))
#             questions_list = questions.scalars().all()

#     if not questions_list:
#         await message.answer("No questions found.")
#     else:
#         reply_text = "\n".join([f"{q.id}: {q.question_text}" for q in questions_list])
#         await message.answer(reply_text)

if __name__ == "__main__":
    dp.run_polling(bot)
