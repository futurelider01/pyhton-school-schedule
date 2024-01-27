from aiogram.fsm.state import StatesGroup, State

class Jadval(StatesGroup):
    role = State()
    day_of_week = State()
    name = State()
    sinf = State()
    auto = State()
    