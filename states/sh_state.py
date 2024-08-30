from aiogram.dispatcher.filters.state import State, StatesGroup


class sh_state(StatesGroup):
    city = State()
    date = State()
    amount = State()
    photos = State()
    photo_amount = State()
    basedata = State()
    loading = State()

