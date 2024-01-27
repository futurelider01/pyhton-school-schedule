from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType
from aiogram.filters import CommandStart,Command
import os
import asyncio
import logging

from dotenv import load_dotenv

from core.states.states_reg import *
from core.funtions.basic import *
from core.funtions.adminFunc import *
from core.states.jadval import Jadval
from core.states.states_reg import User
from core.keyboards.keyboards import *

load_dotenv()
config = os.environ
TOKEN = config["TOKEN"]
ADMIN_ID = config["ADMIN_ID"]

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    dp.message.register(admin_func, Command('admin'), lambda message: str(message.chat.id) in ADMIN_ID)
    dp.message.register(load_schedule, file.schedule_file, F.document, lambda message: str(message.chat.id) in ADMIN_ID)
    dp.message.register(send_error, F.document, lambda message: str(message.chat.id) not in ADMIN_ID)

    dp.message.register(cmd_start,CommandStart())
    dp.message.register(cancel, Command('cancel',ignore_case=True))
    dp.message.register(cmd_help, Command('help',ignore_case=True))
    dp.message.register(cmd_schedule, Command('schedule',ignore_case=True))
    dp.message.register(all_teachers, Command('ustozlar',ignore_case=True))
    dp.message.register(daily, Command('daily',ignore_case=True))

    dp.message.register(process_role, Jadval.role)
    dp.message.register(process_day_of_week, Jadval.day_of_week)
    dp.callback_query.register(process_sinf, Jadval.sinf)
    dp.message.register(process_identity, Jadval.name)

    dp.message.register(auto_respone, Jadval.auto)

    dp.message.register(process_name, User.name )
    dp.message.register(process_role4user,User.role)
    dp.message.register(process_teacherName,User.teacher_name) 
    dp.message.register(process_contact,User.phone)

    dp.callback_query.register(get_grade_from_inline, User.sinf)

    dp.message.register(auto_respone, F.text)

    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())