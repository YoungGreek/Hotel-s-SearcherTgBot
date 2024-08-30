from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp

@dp.message_handler(CommandHelp())
async def help(message: types.Message):
    await message.answer('Данный БОТ распознаёт 4 команды:\n'
                         '1 - Топ самых дешёвых отелей в городе(/lowprice)\n'
                         '2 - Топ самых дорогих отелей в городе(/highprice)\n'
                         '3 - Топ отелей, наиболее подходящих по цене и расположению от центра(/bestdeal)\n'
                         '4 - История ваших запросов, дата и время, команда, а так же найденные отели. '
                         )
