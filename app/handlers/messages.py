from aiogram import Bot, Dispatcher, html, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.utils.llm_client import create_sql_query
from app.db_config import local_session
from sqlalchemy import text

msg_router = Router()


@msg_router.message()
async def msg_handler(message: Message):
    # sql_query = await create_sql_query(str(message.text))

    # async with local_session() as db:
    #     res = await db.execute(text(str(sql_query)))
    #     answer = await res.scalar_one()

    # await message.answer(str(answer))
    await message.answer("Привет! Я могу ответить на вопросы о видео. Просто задай мне вопрос, и я постараюсь помочь!")