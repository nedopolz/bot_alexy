import datetime

from aiogram import types

from data.mesages_config import PERSONAL_CABINET_BUTTON, PERSONAL_CABINET, WITHDRAW_BUTTON, WITHDRAW, \
    REFERRAL_INFO, BUTTON_NAME, BUTTON_LINK
from keyboards.inline.withdraw_button import withdrawal_button
from loader import dp, db, bot


@dp.message_handler(regexp=PERSONAL_CABINET_BUTTON)
async def my_office(message: types.Message):
    db_record = (await db.get_user_info(message.from_user.id))
    db_record = db_record[0]
    completed_site_id = db_record.get('completed_site_id')
    completed_tiktok_id = db_record.get('completed_tiktok_id')
    earnings = db_record.get('earnings')
    registration_date = db_record.get('registration_date')
    attracted_users = db_record.get('attracted_users')
    user_name = message.from_user.first_name

    days_in_bot = (datetime.date.today() - registration_date).days

    if not completed_site_id:
        completed_site_number = 0
    else:
        completed_site_number = len(completed_site_id)

    if not completed_tiktok_id:
        completed_tiktok_number = 0
    else:
        completed_tiktok_number = len(completed_tiktok_id)

    await message.answer(
        PERSONAL_CABINET.format(user_name, days_in_bot, attracted_users, completed_tiktok_number, completed_site_number,
                                earnings))  # TODO когда переработаешь базу данных переработай и это


@dp.message_handler(regexp=WITHDRAW_BUTTON)
async def withdrawal_callback(message: types.Message):
    await message.answer(text=WITHDRAW, reply_markup=withdrawal_button)


@dp.message_handler(regexp=BUTTON_NAME)
async def additional_button(message: types.Message):
    await message.answer(BUTTON_LINK)


@dp.callback_query_handler(text_contains='referral')
async def referrals(call: types.CallbackQuery):
    db_record = (await db.get_user_info(call.from_user.id))
    db_record = db_record[0]
    attracted_users = db_record.get('attracted_users')
    user_id = str(call.from_user.id)
    bot_name = (await bot.me).username
    link = f'https://telegram.me/{bot_name}?start={user_id}'
    await call.message.answer(REFERRAL_INFO.format(attracted_users, link))
