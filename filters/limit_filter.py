from aiogram.dispatcher.filters import BoundFilter
from data.config import MAX_PHOTOS, MAX_HOTELS
from aiogram import types


class LimitFilter(BoundFilter):
    key = 'limit'

    def __init__(self, limit):
        self.limit = limit

    async def check(self, message: types.Message) -> bool:
        if message.text.isdigit() and (int(message.text) < MAX_PHOTOS or int(message.text) < MAX_HOTELS):
            return False
        else:
            return True
