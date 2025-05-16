import asyncio
import os
import sys
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from dotenv import load_dotenv
import django
import pytz
from django.utils.timezone import now
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
load_dotenv()

from main.models import User, Tasks
moscow_tz = pytz.timezone('Europe/Moscow')

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# All handlers should be attached to the Dispatcher
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    tg_id = message.from_user.id
    user, created = await User.objects.aget_or_create(
        tg_id=tg_id,
    )
    await message.answer(f"🫱🏼‍🫲🏻 Добро пожаловать, {message.from_user.full_name}!", parse_mode="HTML")


@dp.message(Command('mytasks'))
async def handler_mytasks(message: Message):
    tg_id = message.from_user.id
    current_time = now().astimezone(moscow_tz).replace(tzinfo=None)
    check_task= await Tasks.objects.filter(user__tg_id=tg_id).afirst()
    if check_task:
        [await send_message_to_user(telegram_id=task.user.tg_id,
                                            minutes=int((task.deadline - current_time).total_seconds()) // 60,
                                            seconds=int((task.deadline - current_time).total_seconds()) % 60,
                                            task_id=task.id) async for task in
                 Tasks.objects.filter(user__tg_id=tg_id, deadline__lte=current_time + timedelta(minutes=10),
                                      deadline__gte=current_time).select_related('user').all()]

    else:
        await bot.send_message(chat_id=tg_id, text='У вас нет активных задач', parse_mode="HTML")

@dp.message(Command('done'))
async def change_status_mytask(message: Message, command: CommandObject):
    task_id = command.args
    tg_id = message.from_user.id
    task = await Tasks.objects.filter(id=task_id, user__tg_id=tg_id).select_related('user').afirst()
    async with AiohttpSession() as session:
        bot = Bot(token=TOKEN, session=session)
        if task.status == 'done':
            await bot.send_message(chat_id=tg_id, text='Статус вашей задачи уже был изменен на "done"',
                                   parse_mode="HTML")
        elif task:
            task.status = 'done'
            await task.asave()
            await bot.send_message(chat_id=tg_id, text='Статус вашей задачи успешно изменен на "done"', parse_mode="HTML")
        else:
            await bot.send_message(chat_id=tg_id, text='У вас нет данной задачи', parse_mode="HTML")


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


async def send_message_to_user(telegram_id, minutes, seconds, task_id):
    async with AiohttpSession() as session:
        bot = Bot(token=TOKEN, session=session)
        msg = f'Ваша задача под id:{task_id} закочится через {minutes} минут : {seconds} секунд '
        return await bot.send_message(chat_id=telegram_id, text=msg, parse_mode="HTML")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
