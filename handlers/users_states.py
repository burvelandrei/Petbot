from aiogram.fsm.state import StatesGroup, State

class Begin_use(StatesGroup):
    MAIN = State()
    REPEAT_MAIN = State()
    INPUT_NUMBER = State()