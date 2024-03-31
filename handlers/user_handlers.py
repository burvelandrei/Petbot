from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram_dialog import DialogManager, StartMode, Window, Dialog
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button, Back, Cancel

import handlers.users_states as states
from keyboards import inline_keyboards
from keyboards.keyboards import main_menu_kb
from lexicon.lexicon import LEXICON_HI
from config_bd.users import SQL

# Нужно написать два фильтра, для фильтрации имени и номера!!!!!

router = Router()


# Хэндлер на команду /start
@router.message(CommandStart())
async def process_start(message: Message, dialog_manager: DialogManager):
    s = SQL()
    if s.SELECT_USER(message.from_user.id) is None:
        s.INSERT(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        await dialog_manager.start(
            state=states.Begin_use.MAIN,
            data={"tg_id": message.from_user.id},
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(
            state=states.Begin_use.REPEAT_MAIN,
            data={"tg_id": message.from_user.id},
            mode=StartMode.RESET_STACK,
        )


async def name_user_getter(dialog_manager: DialogManager, **kwargs):
    s = SQL()
    tg_id = dialog_manager.start_data["tg_id"]
    user_db = s.SELECT_USER(tg_id)
    username = user_db[1]
    first_name = user_db[2]
    last_name = user_db[3]
    name_user = ""
    if first_name is None and last_name is None:
        name_user = username
    elif last_name is None:
        name_user = first_name
    else:
        name_user = f"{first_name} {last_name}"
    return {"name_user": name_user}


begin_use_window = Window(
    Format(
        "Привет {name_user}.\n"
        "Я бот салона красоты, "
        "здесь ты можешь записаться к мастеру.\n"
        "Для начала записи, оставь нам свой номер\n",
    ),
    SwitchTo(
        Const("Ввести номер"), id="input_number", state=states.Begin_use.INPUT_NUMBER
    ),
    getter=name_user_getter,
    state=states.Begin_use.MAIN,
)


repeat_use_window = Window(
    Format("С возвращением {name_user}."),
    getter=name_user_getter,
    state=states.Begin_use.REPEAT_MAIN,
)


begin_use_dialog = Dialog(begin_use_window, repeat_use_window)
