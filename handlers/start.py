from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(f'Hello {message.from_user.mention}')
