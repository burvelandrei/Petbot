import datetime
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram_dialog import DialogManager, StartMode, Window, Dialog, ChatEvent
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    Start,
    SwitchTo,
    Button,
    Back,
    Cancel,
    Group,
    Calendar,
    ManagedCalendar,
)
from aiogram_dialog.widgets.input import TextInput, MessageInput, ManagedTextInput

import handlers.users_states as states
from lexicon.lexicon import LEXICON_HI
from handlers.common import MAIN_MENU_BUTTON
from config_bd.users import SQL
from config_bd.date_apointment import SQL_D_A


async def on_date_clicked(
    callback: ChatEvent,
    widget: ManagedCalendar,
    dialog_manager: DialogManager,
    selected_date: datetime.date,
    /,
):
    # date_app_bd = SQL_D_A()
    # tg_id = callback.from_user.id
    # date_app_bd.INSERT(tg_id, str(selected_date))
    dialog_manager.dialog_data["date"] = str(selected_date)
    await dialog_manager.switch_to(states.Sign_up.SELECT_TIME)


async def on_time_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, text: str):
    date = dialog_manager.dialog_data["date"]
    all_time = f"{date} {text}"
    date_app_bd = SQL_D_A()
    tg_id = callback.from_user.id
    date_app_bd.INSERT(tg_id, all_time)
    dialog_manager.dialog_data.update({"all_time": all_time})
    await dialog_manager.switch_to(states.Sign_up.CONFIRM_SIGN)



async def all_time_getter(dialog_manager: DialogManager, **kwargs):
    return {"all_time": dialog_manager.dialog_data["all_time"]}


sign_up_window = Window(
    Const("Выберите день записи"),
    Calendar(id="calendar", on_click=on_date_clicked),
    state=states.Sign_up.MAIN,
)

confirm_sign_window = Window(
    Format("Вы записаны на {all_time}"),
    MAIN_MENU_BUTTON,
    getter=all_time_getter,
    state=states.Sign_up.CONFIRM_SIGN,
)


sign_up_dialog = Dialog(sign_up_window, confirm_sign_window)
