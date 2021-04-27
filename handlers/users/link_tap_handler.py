from aiogram.types import CallbackQuery

from loader import dp


@dp.callback_query_handler(text_contains='earn')
async def earn(call: CallbackQuery):
    print("in")
    await call.answer("popo")
