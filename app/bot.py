import asyncio
import logging
import sys

import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.config import settings
from app.handlers import commands, messages
from app.utils.db import fill_db
from app.db_config import local_session
from app.models.videos import Video
from app.models.video_snapshots import VideoSnapshot
from sqlalchemy import select

TOKEN = settings.bot_token


dp = Dispatcher()
dp.include_routers(commands.cmd_router, messages.msg_router)


async def main():
    # Init database if it's empty
    async with local_session() as db:
        videos = await db.scalars(select(Video))
        snaps = await db.scalars(select(VideoSnapshot))
        if not videos and not snaps:
            await fill_db()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
