import aiogram
import datetime
import sqlite3 as sq
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot

@dp.message_handler(Command('history'))
async def history(message: types.Message):
    id = message.from_user.id
    date_time = datetime.datetime.today()
    date = date_time.date()
    with sq.connect('TelegramBot.sqlite3') as con:
        cur = con.cursor()
        data = cur.execute("SELECT name, command, date, time, hotels FROM users"
                           " WHERE date = (?) AND name = (?) ORDER BY time DESC LIMIT 5", (date, str(id), ))
        for string in data:
            elements = list(string)
            await message.answer('ID пользоателя: ' + str(elements[0]) + '\n'
                                 'Введённая команда: ' + str(elements[1]) + '\n'
                                 'Дата: ' + str(elements[2]) + '\n'
                                 'Время: ' + str(elements[3]) + '\n'
                                 'Отель: ' + str(elements[4]) + '\n'
                                 , disable_notification=True)
