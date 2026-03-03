from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

cmd_router = Router()


@cmd_router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
