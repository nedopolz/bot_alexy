from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.config import admins
from keyboards.inline.task_type import choose_type
from loader import dp, db
from states.task_addition import Addition


@dp.message_handler(Command("add_task"))
async def add_task(message: types.Message):
    if message.from_user.id in admins:
        await message.answer("Введите ссылку на целевой ресурс")
        await Addition.url.set()
    else:
        await message.answer("команда не доступна")


@dp.message_handler(state=Addition.url)
async def get_url(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data(url=url)
    await message.answer('выберите тип', reply_markup=choose_type)
    await Addition.type.set()


@dp.callback_query_handler(state=Addition.type, text_contains='site')
async def site_adding(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    await db.add_task_sites(url)
    await call.message.answer("успешно")
    await state.finish()


@dp.callback_query_handler(state=Addition.type, text_contains='tiktok')
async def site_adding(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    await db.add_task_tiktok(url)
    await call.message.answer("успешно")
    await state.finish()


@dp.message_handler(state=Addition.reward)
async def bot_start(message: types.Message, state: FSMContext):
    reward = message.text
    try:
        reward = int(reward)
    except ValueError:
        await message.answer("награда должна быть числом")
        return
    data = await state.get_data()
    url = data.get("url")
    await db.add_task(url, reward)
    await message.answer("успешно")
    await state.finish()
