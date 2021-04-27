import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import allowed_withdrawal_amount
from data.mesages_config import NOT_ENOUGH_CREDIT, ENTER_ACCOUNT_NUMBER, NOT_VALID_NUMBER, \
    ENTER_WITHDRAWAL_AMOUNT, NOT_VALID_AMOUNT, CONFIRM_WITHDRAWAL, SUCSESS, UNDO
from keyboards.inline.withdraw_button import conformation_button
from loader import dp, db
from states.withdrawl import Withdrawal


@dp.callback_query_handler(text_contains='Withdrawal')
async def withdrawal(call: CallbackQuery, state: FSMContext):
    db_record = await db.get_user_info(call.from_user.id)
    db_record = db_record[0]
    earnings = db_record.get('earnings')
    await state.update_data(earnings=earnings)
    if earnings < allowed_withdrawal_amount:
        await call.message.answer(NOT_ENOUGH_CREDIT)
    else:
        await call.message.answer(ENTER_ACCOUNT_NUMBER)
        await Withdrawal.account_number.set()


@dp.message_handler(state=Withdrawal.account_number)
async def get_account_number(message: types.Message):
    account_number = re.findall(r'^\d{10}$', message.text)
    print(account_number)
    if not account_number:
        await message.answer(NOT_VALID_NUMBER)
    else:
        await message.answer(ENTER_WITHDRAWAL_AMOUNT)
        await Withdrawal.amount.set()


@dp.message_handler(state=Withdrawal.amount)
async def get_withdrawal_amount(message: types.Message, state: FSMContext):
    withdrawal_amount = re.findall(r'^\d{1,20}$', message.text)

    if not withdrawal_amount:
        await message.answer(NOT_VALID_AMOUNT)
    else:
        withdrawal_amount = withdrawal_amount[0]
        data = await state.get_data()
        available = data.get('earnings')

        withdrawal_amount = int(withdrawal_amount)

        if withdrawal_amount < allowed_withdrawal_amount:
            withdrawal_amount = allowed_withdrawal_amount

        if withdrawal_amount > available:
            withdrawal_amount = available

        await state.update_data(withdrawal_amount=withdrawal_amount)
        await message.answer(CONFIRM_WITHDRAWAL.format(withdrawal_amount), reply_markup=conformation_button)
        await Withdrawal.conformation.set()


@dp.callback_query_handler(text_contains='confirm', state=Withdrawal.conformation)
async def confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    withdrawal_amount = data.get('withdrawal_amount')
    await db.add_earnings(call.from_user.id, -withdrawal_amount)
    await call.message.answer(SUCSESS)
    await state.finish()


@dp.callback_query_handler(text_contains='undo', state=Withdrawal.conformation)
async def undo(call: CallbackQuery, state: FSMContext):
    await call.message.answer(UNDO)
    await state.finish()
