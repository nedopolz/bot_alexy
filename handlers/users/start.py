import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import referral_reward
from data.mesages_config import WELCOME, NO_REF_CODE_FOUND, REF_CODE_ALREADY_ENTERED, YOU_USE_YOUR_LINK
from keyboards.default import menu
from loader import dp, db


@dp.message_handler(CommandStart(deep_link=re.compile(r'^[0-9]{4,15}$')))
async def start_deeplink(message: types.Message):
    code = int(message.get_args())
    user_id = message.from_user.id
    user_status = (await db.check_user(user_id))[0].get('count')
    if (await db.check_user(code))[0].get('count') == 1 and user_status == 0:
        await db.add_user(user_id, True)
        await db.add_earnings_for_referrals(code, referral_reward)
        await message.answer(WELCOME, reply_markup=menu)

    elif (await db.check_user(code))[0].get('count') == 0 and user_status == 0:
        await message.answer(NO_REF_CODE_FOUND, reply_markup=menu)
        await db.add_user(user_id, False)

    elif (await db.check_user_for_referal(user_id))[0].get('count') == 0:
        await message.answer(REF_CODE_ALREADY_ENTERED, reply_markup=menu)

    elif (await db.check_user_for_referal(user_id))[0].get('count') == 1 and code != user_id:
        await db.add_earnings_for_referrals(code, referral_reward)
        await db.set_invited_true(message.from_user.id)
        await message.answer(WELCOME, reply_markup=menu)
    else:
        await message.answer(YOU_USE_YOUR_LINK)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if (await db.check_user(message.from_user.id))[0].get('count') == 1:
        await message.answer(WELCOME, reply_markup=menu)
    else:
        await db.add_user(message.from_user.id, False)
        await message.answer(WELCOME, reply_markup=menu)
