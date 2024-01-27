from aiogram.fsm.state import StatesGroup, State

class User(StatesGroup):
    name = State()
    role = State()
    sinf = State()
    phone = State()
    teacher_name = State()
