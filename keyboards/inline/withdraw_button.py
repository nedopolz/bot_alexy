from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.mesages_config import WITHDRAW_BUTTON

withdrawal_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=WITHDRAW_BUTTON, callback_data="Withdrawal"),
    ]
])

conformation_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="OK", callback_data="confirm"),
        InlineKeyboardButton(text="No", callback_data="undo")
    ]
])
