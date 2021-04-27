from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.mesages_config import EARN_BUTTON, PERSONAL_CABINET_BUTTON, WITHDRAW_BUTTON, BUTTON_NAME

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=EARN_BUTTON),
            KeyboardButton(text=PERSONAL_CABINET_BUTTON)
        ],
        [
            KeyboardButton(text=WITHDRAW_BUTTON),
            KeyboardButton(text=BUTTON_NAME)
        ],
    ],
    resize_keyboard=True
)
