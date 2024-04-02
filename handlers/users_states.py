from aiogram.fsm.state import StatesGroup, State

class Begin_use(StatesGroup):
    MAIN = State()
    REPEAT_MAIN = State()
    INPUT_NUMBER = State()
    MAIN_MENU = State()
    OUR_CONTACTS = State()
    MY_APPOINTMENTS = State()

class Sign_up(StatesGroup):
    MAIN = State()
    CONFIRM_SIGN = State()
