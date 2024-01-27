from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from core.keyboards.keyboards import *
from core.funtions.changeSchedule import NEW_SCH
from core.states.jadval import Jadval
from core.states.adminState import file
from core.funtions.changeSchedule import *

async def admin_func(message: Message, state: FSMContext):
    await message.answer("Admin paneli... \nAdmin panelida siz yangi jadvalni yuklashingiz mumkin.",
                         reply_markup=adminKeyBoard)
    await state.set_state(file.schedule_file)
async def load_schedule(message: Message, bot: Bot, state: FSMContext):
    new_schedule = message.document
    if new_schedule.mime_type=='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        file_id = new_schedule.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, NEW_SCH+"\\file.xlsx")
        
        await message.answer("Saqlandi.",reply_markup=week6)    
        swap_schedules()
        await message.answer("Yangilandi!")
    await state.clear()
    
async def send_error(message: Message, state: FSMContext):
    await message.reply("Men faqat matn bilan ishlayman.")
    state.set_state(Jadval.auto)