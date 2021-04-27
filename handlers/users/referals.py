from aiogram import types

from loader import dp, bot


@dp.message_handler(commands="invite")
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    bot_name = (await bot.me).username
    await message.answer(f'Привет, вот твоя реферальная ссылка https://telegram.me/{bot_name}?start={user_id}')
