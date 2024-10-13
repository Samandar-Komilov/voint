from aiogram import Bot, Dispatcher, F, types
from io import BytesIO
import logging
import asyncio

from config import BOT_TOKEN
from database.database import init_db

from routers.common import router as common_router
from routers.interview import router as interview_router


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.startup()
async def on_startup():
    await init_db()
    logging.debug("Database connected and tables created.")


async def main() -> None:
    # storage = MemoryStorage()
    dp.include_router(common_router)
    dp.include_router(interview_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

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
