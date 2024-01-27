import logging
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery,
                            KeyboardButton, ReplyKeyboardMarkup, 
                            ReplyKeyboardRemove)

from core.states.jadval import Jadval
from core.keyboards.keyboards import *
from core.funtions.logic import *
from core.states.states_reg import User


async def cmd_start(message: Message, state: FSMContext):
    id = message.chat.id
    if id not in all_ids():
        await state.set_state(User.name)
        await state.set_data({'chat_id':id})
    
        await message.reply("Assalomu alaykum Men DRAFT Botman. Sizga dars jadvallari bo'yicha yordam berishim mumkin.\nKeling avval sizni ro'yxatga olib qoysam")
        await message.answer("Ismingiz kim?",reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(
            "Sizni yana qayta ko'rib turganimdan xursandman\nDars jadvallarini ko'rish uchun /schedule ni bosing.\nKo'proq ma'lumot uchun /help ni bosing.",
            reply_markup=markup4fixed
        )
        await state.update_data(chat_id=id)
        await state.set_state(Jadval.auto)
async def cmd_help(message: Message, bot):
    await message.answer("""Bu bot sizga Ellikqal'adagi Ixtisoslashriligan maktabning dars jadvallarini siz hoxlagan shaklda chiqarib beradi.\n\nMasalan o'qituvchi bolsangiz siz kirishingiz kerak bo'lgan sinflarni kunlik yoki haftalik qilib chiqarib beradi\n\nYoki o'quvchi bo'lsaniz sizga ham kunlik yoki haftalik dars jadvalini chiqarib beradi.
                    \nJadvallarni ko'rish uchun /schedule kommandasini yuboring
                    \n/start - Botni ishga tushirish
                    \n/help - Yordam
                    \n/daily - Kunlik jadvalni sizning profilingiz asosida chiqarib beradi
                    \n/schedule - Dars jadvali
                    \n/ustozlar - Bot bazasidagi ustozlarni ko'rish
                    \n/cancel - So'roq/protsesni to'xtatish
                    \nPowered by @Future_Leader_01""")


async def cmd_schedule(message: Message, state: FSMContext):
    await state.set_state(Jadval.role)
    await message.answer("Sizning rolingiz qanday?", reply_markup=role)



async def process_role(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    data = await state.get_data()
    await state.set_state(Jadval.day_of_week)
    if data.get('role')=="O'qituvchi":
        await message.answer("Qaysi hafta kun uchun dars jadvali kerak?", 
                            reply_markup=week7)
    elif data.get('role')=="O'quvchi":
        await message.answer("Qaysi hafta kun uchun dars jadvali kerak?", 
                            reply_markup=week6)
    else:
        await message.answer("Cancelled.\n/schedule ni bosib Rolingizni qaytadan to'g'ri kiriting")
        await state.clear()


async def process_day_of_week(message: Message, state: FSMContext):
    await state.update_data(day_of_week=message.text)
    day = await state.get_data()
    day = day.get('day_of_week')
    if day not in WEEK:
        await message.answer("Hafata kunini to'g'ri kiriting. \nShunchaki to'g'ri hafta kuni bosing👇👇👇") 
        await state.set_state(Jadval.day_of_week)
        return
    data = await state.get_data()
    if data.get('role')=="O'qituvchi":
        await state.set_state(Jadval.name)
        await message.answer("Ismingizni kiriting (Familiya Ism)", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Sinfingizni tanlang.".center(90,'.'), reply_markup=InlineKeyboardMarkup(
            inline_keyboard=get_inline_keyboard()
        ))
        await state.set_state(Jadval.sinf)
    

async def process_sinf(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sinf = call.data
    day = data.get('day_of_week')
    
    res = modify_data4pupils(get_classes_for_pupil(sinf_param=sinf,day_of_week=day))
    await call.message.answer(res)
    await state.clear()

async def process_identity(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data.get('name')

    await message.answer("Qidirilmoqda ...")
    if name not in teachers.values:
        
        await message.reply("Ismingizni to'pa olmadim. Ismingizni Familiya Ism formatida qayta kiriting"\
                            "\n Ismingizni to'g'ri kiritish uchun /ustozlar ni bosing"\
                            "\nYoki /cancel ni bosib qaytadan boshlang")
        await state.set_state(Jadval.name)
        return

    # await message.answer(f"Qidiruv shu {data} ma'lumotlar bo'yicha ketyabdi")
    day = data.get('day_of_week',None) if data.get('day_of_week',None)!='Hammasi' else None
    res = get_classes_for_teacher(name,day,True)
    res = modify_data4teachers(res)
    res += "\n\nThanks to creator @Future_Leader_01"
    await message.answer(res, reply_markup=week7)
    
    await state.set_state(Jadval.auto)

async def all_teachers(message: Message):
    t = ''
    for val in range(0,len(teachers),2):
        i1,i2 = teachers[val:val+2]
        
        t += f"{val+1}. {i1}, {val+2}. {i2}\n"
    t+= "\nMening bazamda shu ustozlar bor. Ismingiz shu yerdan olib jo'natsangiz bo'ladi"
    await message.reply(t)

async def daily(message: Message):
    chat_id = message.chat.id
    day = today_()
    if day=='Yakshanba':
        await message.answer("Bugun dam")
        return
    sinf = get_grade(chat_id)
    role = get_role(chat_id)
    if role=="O'quvchi":    
        res = get_classes_for_pupil(sinf,day)
        res = modify_data4pupils(res)
        text = f"{message.chat.first_name} siz uchun {day} kungi jadval:\n\n"
        text += res
        await message.answer(text)
    elif role=="O'qituvchi":
        name = get_name(chat_id)
        res = get_classes_for_teacher(name,day,True)
        res = modify_data4teachers(res)
        await message.answer(res)

async def auto_respone(message: Message, state: FSMContext):
    
    chat_id = message.chat.id
    day = message.text
    try:
        sinf = get_grade(chat_id)
    except:
        message.answer("/start ni bosing")
        return
    role = get_role(chat_id)
    if role=="O'quvchi":    
        res = get_classes_for_pupil(sinf,day)
        res = modify_data4pupils(res)
        text = f"{message.chat.first_name} siz uchun {day} kungi jadval:\n\n"
        text += res
        await message.answer(text)
    elif role=="O'qituvchi":
        name = get_name(chat_id)
        res = get_classes_for_teacher(name,day,True)
        res = modify_data4teachers(res)
        await message.answer(res)

async def get_grade_from_inline(call: CallbackQuery, state: FSMContext):
    data = call.data
    await state.update_data(sinf=data)
    await call.message.answer("Telefon raqamingizni kiriting",reply_markup=contact)
    await state.set_state(User.phone)


async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return    
    logging.info("Cancelling state %r",current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(User.role)
    await message.answer("Statusingiz qanday", reply_markup=role)

def writer(data: dict):
    with open('D:\Shohiddin\Shohiddin python\Botlar\Dars jadvallari\core\logging.csv','a') as f:
        text = f"{data.get('chat_id')},{data.get('name')},{data.get('role')},{data.get('sinf',None)},{data.get('phone')}\n"
        f.write(text)
async def process_role4user(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    
    data = await state.get_data()
    role = data.get('role')
    if role=='O\'quvchi':
        await message.answer("Sinfingizni kiriting",reply_markup=InlineKeyboardMarkup(
            inline_keyboard=get_inline_keyboard()
            ))
        await state.set_state(User.sinf)
    else:
        await message.answer("Ismingizni qaytadan, shu listdan olib yuborishingizni so'rayman.\nAvtamatlashtirish uch")
        t = ''
        for val in range(0,len(teachers),2):
            i1,i2 = teachers[val:val+2]
            
            t += f"{val+1}. {i1}, {val+2}. {i2}\n"
        t+= "\nMening bazamda shu ustozlar bor. Ismingiz shu yerdan olib jo'natsangiz bo'ladi"
        await message.reply(t)
        await state.set_state(User.teacher_name)

        

async def process_contact(message: Message, state: FSMContext):
    try:
        await state.update_data(phone=message.contact.phone_number)
        data = await state.get_data()
        writer(data)
        await message.answer("Sizni registratsiya qildim")
        text = f"Sizga olgan ma'lumotlarim:\n\nIsmingiz: {data.get('name')}\nStatusingiz: {data.get('role')}"
        if data.get('sinf'):
            text+=f"\nSinfingiz: {data.get('sinf')}"
        text+= f"\nTelefon raqamingiz: {data.get('phone')}"
        await message.answer(text, reply_markup=week6)
        await state.set_state(Jadval.auto)
    
    except AttributeError as e:
        await message.reply("Telefon raqamingizni knopka orqali yuboring👇👇👇")
        await state.set_state(User.phone)

async def process_grade(message: Message, state: FSMContext):
    sinf = message.text
    
    if sinf not in SINFLAR:
        await message.answer("Sinfingizni to'g'ri kiriting.")
        await state.set_state(User.sinf)
        return
    await state.update_data(sinf=message.text)
    await message.answer("Telefon raqamingizni kiriting",reply_markup=contact)
    await state.set_state(User.phone)

async def process_teacherName(message: Message, state: FSMContext):
    name = message.text
    if name not in TEACHERS:
        await message.reply("Ismingizni listdan olib yuboring")
        await state.set_state(User.teacher_name)
        return
    await state.update_data(name=name)
    await message.answer("Telefon raqamingizni kiriting",reply_markup=contact)
        
    await state.set_state(User.phone)