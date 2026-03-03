from aiogram import Router
from aiogram.types import Message
from sqlalchemy import text

from app.db_config import local_session
from app.utils.llm_client import create_sql_query

msg_router = Router()


@msg_router.message()
async def msg_handler(message: Message):
    """Handle user's text message"""
    sql_query, err = await create_sql_query(str(message.text))
    if err:
        await message.answer(err)
        return

    try:
        async with local_session() as db:
            res = await db.execute(text(sql_query))
            scalar = res.scalar_one()
            await message.answer(str(scalar))
    except:
        await message.answer("Не могу ответить на этот запрос")
