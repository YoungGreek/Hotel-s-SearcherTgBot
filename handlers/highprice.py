import aiogram
import datetime
import sqlite3 as sq
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import Command
import filters  # DO NOT TURN OFF
from data import config
from utils import search_request
from aiogram.dispatcher import FSMContext
from states.sh_state import sh_state
from loader import dp, bot


@dp.message_handler(limit=False, state=[sh_state.amount, sh_state.photo_amount])
async def wrong_amounts_answer(message: types.Message):
    await message.answer('Превышен максимум или введены некорректные данные')


@dp.message_handler(date_filter=False, state=sh_state.date)
async def wrong_date_answer(message: types.Message):
    await message.answer('Введена неправильная дата')

@dp.message_handler(Command('highprice'))
async def highprice(message: types.Message, state: FSMContext):
    await message.answer('Топ самых дорогих отелей в городе\n'
                         'Введите город')

    await sh_state.city.set()
    await state.update_data(hotels_sort='PRICE_HIGHEST_FIRST')


@dp.message_handler(state=sh_state.city)
async def get_city(message: types.Message, state: FSMContext):
    ans = message.text
    async with state.proxy() as data:
        data['city'] = ans
    await message.answer('Введите даты в формате yyyy-mm-dd, yyyy-mm-dd')
    await sh_state.next()


@dp.message_handler(state=sh_state.date)
async def get_date(message: types.Message, state: FSMContext):
    ans = message.text.split(', ')
    async with state.proxy() as data:
        data['checkin'] = ans[0]
        data['checkout'] = ans[1]


    await message.answer(f'Введите число отелей (Максимум: {config.MAX_HOTELS})')
    await sh_state.next()



@dp.message_handler(state=sh_state.amount)
async def get_amount(message: types.Message, state: FSMContext):
    ans = message.text
    async with state.proxy() as data:
        data['hotels_amount'] = int(ans)

    await message.answer('Фото отелей? Y/N')
    await sh_state.next()


@dp.message_handler(state=sh_state.photos)
async def get_photo(message: types.Message, state: FSMContext):
    ans = message.text.lower()
    if ans == 'y':
        await message.answer('Введите количество фото (макс. 10)')
        await sh_state.next()

    elif ans == 'n':
        async with state.proxy() as data:
            data['photos'] = -1

        data = await state.get_data()
        result = await search_request.lp_get(data, message.from_user.mention, )
        date_time = datetime.datetime.today()
        date = date_time.date()
        id = message.from_user.id
        for i in range(data['hotels_amount']):
            hotel_data = f'{result.names[i]}\n' \
                         f'Адрес: {result.addresses[i]}\n' \
                         f'Расстояние до центра: {result.center_distances[i]}\n' \
                         f'Цена: {result.prices[i]}\n'
            hotel_info = str(result.names[i]) + '\n' + str(result.addresses[i]) + \
                         '\n' + str(result.center_distances[i]) + \
                         '\n' + str(result.prices[i])
            time = date_time.time()
            with sq.connect('TelegramBot.sqlite3') as con:
                cur = con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS users (\n"
                            "        name TEXT,\n"
                            "        command TEXT,\n"
                            "        date TEXT,\n"
                            "        time TEXT,\n"
                            "        hotels TEXT\n"
                            "        )")
                cur.execute("""INSERT INTO users (name, command, date, time, hotels) VALUES (?, ?, ?, ?, ?)""",
                            (str(id), '/highprice', str(date), str(time), hotel_info,))
            await message.answer(hotel_data, disable_notification=True)

        await state.reset_state()


    else:
        await message.answer('Введены некорректные данные')


@dp.message_handler(state=sh_state.photo_amount)
async def get_photo_amount(message: types.Message, state: FSMContext):
    ans = int(message.text)
    async with state.proxy() as data:
        data['photos'] = ans

    data = await state.get_data()
    result = await search_request.lp_get(data, message.from_user.mention, )
    date_time = datetime.datetime.today()
    date = date_time.date()
    id = message.from_user.id
    for i in range(data['hotels_amount']):
        if data['photos'] > 0:
            media = types.MediaGroup()
            med_arr = list(map(types.InputMediaPhoto, result.photos_links[i]))
            media.attach_many(*med_arr)

            hotel_data = f'{result.names[i]}\n' \
                         f'Адрес: {result.addresses[i]}\n' \
                         f'Расстояние до центра: {result.center_distances[i]}\n' \
                         f'Цена: {result.prices[i]}\n'

            hotel_info = str(result.names[i]) + '\n' + str(result.addresses[i]) + \
                         '\n' + str(result.center_distances[i]) + \
                         '\n' + str(result.prices[i])
            time = date_time.time()
            with sq.connect('TelegramBot.sqlite3') as con:
                cur = con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS users (\n"
                            "        name TEXT,\n"
                            "        command TEXT,\n"
                            "        date TEXT,\n"
                            "        time TEXT,\n"
                            "        hotels TEXT\n"
                            "        )")
                cur.execute("""INSERT INTO users (name, command, date, time, hotels) VALUES (?, ?, ?, ?, ?)""",
                            (str(id), '/highprice', str(date), str(time), hotel_info,))

            med_arr[0].caption = hotel_data
            await bot.send_media_group(message.chat.id, media=media, disable_notification=True)


    await state.reset_state()


