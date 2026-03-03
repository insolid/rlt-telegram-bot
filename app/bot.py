import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import select

from app.config import settings
from app.db_config import local_session
from app.handlers import commands, messages
from app.models.video_snapshots import VideoSnapshot
from app.models.videos import Video
from app.utils.db import fill_db

TOKEN = settings.bot_token


dp = Dispatcher()
dp.include_routers(commands.cmd_router, messages.msg_router)


async def main():
    # Init database if it's empty
    async with local_session() as db:
        videos = await db.scalars(select(Video))
        snaps = await db.scalars(select(VideoSnapshot))
        if not videos.all() and not snaps.all():
            await fill_db()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
