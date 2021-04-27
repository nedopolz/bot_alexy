from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

choose_type = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="site", callback_data="site"),
        InlineKeyboardButton(text="tiktok", callback_data="tiktok"),
    ]
])
