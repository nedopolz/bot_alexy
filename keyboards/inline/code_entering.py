from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

enter_code = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Ввести код приглашения", callback_data="code"),
    ]
])
