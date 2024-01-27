from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from core.funtions.logic import SINFLAR
from pprint import pprint as print

sinflar = ['5-A', '5-B', '6-A', '6-B', '7-A', '7-C', '8-A', '8-C', '9-A', '9-C', '9-O','10-A', '10-B', '10-C', '10-O', '11-A', '11-B']


def get_inline_keyboard():
    inline_keyboard=[]
    for i in range(0,len(sinflar),6):
        temp=[]
        for j in sinflar[i:i+6]:
            num, let = j.split('-')
            call_data = num+let
            if j[-1]=='O':
                call_data=j
            temp.append(InlineKeyboardButton(text=j,callback_data=call_data))
        inline_keyboard.append(temp)
    return inline_keyboard

markup4fixed=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Dushanba'), KeyboardButton(text='Seshanba'),KeyboardButton(text='Chorshanba')],
        [KeyboardButton(text='Payshanba'), KeyboardButton(text='Juma'), KeyboardButton(text='Shanba')],
    ],
    resize_keyboard=True, input_field_placeholder="Hafta kuni")


role = ReplyKeyboardMarkup(
        keyboard=[
                [KeyboardButton(text="O'qituvchi"),KeyboardButton(text="O'quvchi")]
            ], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Role'
        )

week7 = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Dushanba'), KeyboardButton(text='Seshanba'),KeyboardButton(text='Chorshanba')],
                [KeyboardButton(text='Payshanba'), KeyboardButton(text='Juma'), KeyboardButton(text='Shanba')],
                [KeyboardButton(text='Hammasi')]
            ],
            resize_keyboard=True,one_time_keyboard=True, input_field_placeholder="Hafta kuni")
week6=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='Dushanba'), KeyboardButton(text='Seshanba'),KeyboardButton(text='Chorshanba')],
                [KeyboardButton(text='Payshanba'), KeyboardButton(text='Juma'), KeyboardButton(text='Shanba')],
            ],
            resize_keyboard=True,one_time_keyboard=True, input_field_placeholder="Hafta kuni")
contact = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Telefon raqamni jo'natish",request_contact=True)]],resize_keyboard=True)

adminKeyBoard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/cancel")]],
    resize_keyboard=True,one_time_keyboard=True,input_field_placeholder="Yangi jadvalni yuboring"
)