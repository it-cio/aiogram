import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types


''' DateTime '''
date = datetime.now().strftime('%Y-%m-%d')
time = datetime.now().strftime('%H:%M:%S')
dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

id_list = []
load_dotenv()
bot_name = os.getenv('token')
bot_id = os.getenv('id')
bot = Bot(token=bot_name)
dp = Dispatcher(bot)


@dp.message_handler(commands=['test'])
async def bot_answer(message: types.Message):
    await send_message('Тест пройден!')
    await message.delete()
    await asyncio.sleep(1)


async def fn(_):
    print('Aiogram bot')


async def send_message(message):
    bot_message = await bot.send_message(bot_id, message)
    message_id = bot_message.message_id
    id_list.append(message_id)
    await asyncio.sleep(1)
    print(f"{dt} Bot send message (id: {message_id})")
    return message_id


async def edit_message(message, message_id):
    await bot.edit_message_text(message, bot_id, message_id)
    print(f"{dt} Bot edit message (id: {message_id})")
    await asyncio.sleep(1)


async def delete_message(message_id):
    await bot.delete_message(bot_id, message_id)
    print(f"{dt} Bot delete message (id: {message_id})")
    await asyncio.sleep(1)


async def pin_message(message_id):
    await bot.pin_chat_message(bot_id, message_id)
    print(f"{dt} Bot pin message (id: {message_id})")
    await asyncio.sleep(1)


# delete all pinned message
@dp.message_handler(content_types=['pinned_message'])
async def delete_pinned(message: types.Message):
    print(f"{dt} Bot delete pinned_message")
    await message.delete()


async def on_startup(_):
    await send_message('Бот приступил к работе!')
    await asyncio.sleep(1)


async def on_shutdown(_):
    for message_id in id_list:
        await delete_message(message_id)
    await asyncio.sleep(1)


def run(startup=fn, shutdown=fn):
    executor.start_polling(dp, skip_updates=True, on_startup=(on_startup, startup), on_shutdown=(on_shutdown, shutdown))