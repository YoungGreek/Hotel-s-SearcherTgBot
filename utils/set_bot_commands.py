from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            # types.BotCommand("stop", "Отменить комманду"),
            types.BotCommand("lowprice", 'Топ самых дешёвых отелей в городе'),
            types.BotCommand("highprice", 'Топ самых дорогих отелей в городе'),
            types.BotCommand("bestdeal", 'Топ отелей, наиболее подходящих по цене и расположению от центра'),
            types.BotCommand("history", 'История запросов'),
        ]
    )
