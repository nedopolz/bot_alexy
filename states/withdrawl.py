from aiogram.dispatcher.filters.state import StatesGroup, State


class Withdrawal(StatesGroup):
    account_number = State()
    amount = State()
    conformation = State()
