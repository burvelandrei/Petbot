from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram_dialog import DialogManager, StartMode, Window, Dialog
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button, Back, Cancel, Group
from aiogram_dialog.widgets.input import TextInput, MessageInput, ManagedTextInput

import handlers.users_states as states
from keyboards import inline_keyboards
from keyboards.keyboards import main_menu_kb
from lexicon.lexicon import LEXICON_HI
from config_bd.users import SQL
from config_bd.date_apointment import SQL_D_A

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
        await dialog_manager.start(
            state=states.Begin_use.MAIN_MENU,
            data={"tg_id": message.from_user.id},
            mode=StartMode.RESET_STACK,
        )


async def correct_phone_number(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
):
    tg_id = dialog_manager.start_data["tg_id"]
    s = SQL()
    s.UPDATE_phonenumber(tg_id, text)
    await dialog_manager.switch_to(states.Begin_use.MAIN_MENU)


async def no_text(message: Message, dialog_manager: DialogManager, text: str):
    await message.answer("Вы ввели вообще не текст")


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


async def phone_number_getter(dialog_manager: DialogManager, **kwargs):
    s = SQL()
    tg_id = dialog_manager.start_data["tg_id"]
    user_db = s.SELECT_USER(tg_id)
    phone_number = user_db[4]
    return {"phone_number": phone_number}


async def appointments_getter(dialog_manager: DialogManager, **kwargs):
    date_app_bd = SQL_D_A()
    tg_id = dialog_manager.start_data["tg_id"]
    appoint_bd = date_app_bd.SELECT_apointment(tg_id)
    print(appoint_bd)
    appointments_out = ""
    for number in range(len(appoint_bd)):
        appointments_out += f"{number+1}. Дата - {appoint_bd[number][1]}\n"
    return {"appointments": appointments_out}


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


input_number_window = Window(
    Const("Введите Ваш номер"),
    TextInput(
        id="age_input",
        # type_factory=age_check,
        on_success=correct_phone_number,  # пока отлавливаем только не текст, надо придумать функцию которая будет выбивать неправильный номер
        # on_error=error_age_handler,
    ),
    SwitchTo(
        Const("Назад в Меню"),
        id="back_menu",
        state=states.Begin_use.MAIN_MENU,
        when="phone_number",
    ),
    MessageInput(func=no_text, content_types=ContentType.ANY),
    getter=phone_number_getter,
    state=states.Begin_use.INPUT_NUMBER,
)


main_menu_window = Window(
    Const("Главное меню"),
    Group(
        Start(Const("Записаться"), id="sign_up", state=states.Sign_up.MAIN),
        SwitchTo(
            Const("Мои записи"),
            id="my_appointment",
            state=states.Begin_use.MY_APPOINTMENTS,
        ),
        SwitchTo(
            Const("Наши контакты"),
            id="our_contacts",
            state=states.Begin_use.OUR_CONTACTS,
        ),
        SwitchTo(
            Const("Изменить номер"),
            id="update_number",
            state=states.Begin_use.INPUT_NUMBER,
        ),
        width=2,
    ),
    state=states.Begin_use.MAIN_MENU,
)


our_contacts_window = Window(
    Const("Наши контакты:\n" "Адресс - \n" "Телефоны - \n"),
    SwitchTo(Const("Назад в Меню"), id="back_menu", state=states.Begin_use.MAIN_MENU),
    state=states.Begin_use.OUR_CONTACTS,
)


my_appointments_window = Window(
    Format("Мои записи\n" "{appointments}"),
    SwitchTo(Const("Назад в Меню"), id="back_menu", state=states.Begin_use.MAIN_MENU),
    getter=appointments_getter,
    state=states.Begin_use.MY_APPOINTMENTS,
)

begin_use_dialog = Dialog(
    begin_use_window,
    repeat_use_window,
    input_number_window,
    main_menu_window,
    our_contacts_window,
    my_appointments_window,
)
