from aiogram.dispatcher.filters.state import StatesGroup, State


class Addition(StatesGroup):
    url = State()
    type = State()
    reward = State()
