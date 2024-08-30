from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from datetime import datetime


class DateFilter(BoundFilter):
    key = 'date_filter'

    def __init__(self, date_filter):
        self.date_filter = date_filter

    async def check(self, message: types.Message) -> bool:
        try:
            date = message.text.split(', ')
            datetime.strptime(date[0], '%Y-%m-%d')
            datetime.strptime(date[1], '%Y-%m-%d')
            return False
        except ValueError:
            return True
