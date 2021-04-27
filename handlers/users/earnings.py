from aiogram import types

from data.mesages_config import EARN_BUTTON, GET_MONEY
from keyboards.inline.earnings_factory import inline_link_factory
from loader import dp


@dp.message_handler(regexp=EARN_BUTTON)
async def earn(message: types.Message):
    user_id = message.from_user.id
    button = await inline_link_factory(user_id)
    await message.answer(GET_MONEY, reply_markup=button)
