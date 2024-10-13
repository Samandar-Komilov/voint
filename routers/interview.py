from aiogram.filters import Command, CommandStart
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from sqlalchemy import select, exists

from database.database import get_db
from database.db_utils import is_user_admin, is_user_exists
from database.models import User, Question, Response


router = Router()


@router.message(Command("create_question"))
async def create_question_handler(message: types.Message):
    is_admin = is_user_admin(message.from_user.id)
    if not is_admin:
        return
    question_text = message.text.split(maxsplit=1)[1]
    async for session in get_db():
        async with session.begin():
            new_question = Question(question_text=question_text)
            session.add(new_question)
        await message.answer(f"Question '{question_text}' created.")


@router.message(Command("create_category"))
async def create_category_handler(message: types.Message):
    pass


@router.message(Command("create_topic"))
async def create_topic_handler(message: types.Message):
    pass


@router.message(Command("create_response"))
async def create_response_handler(message: types.Message):
    pass