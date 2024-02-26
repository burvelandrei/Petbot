from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_MAIN_MENU_COMMANDS


def create_kb(
        width: int,
        *args: str,
        lst_button: str|None = None,
        **kwargs: str) -> ReplyKeyboardMarkup:

    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(
                text=LEXICON_MAIN_MENU_COMMANDS[button] if button in LEXICON_MAIN_MENU_COMMANDS else button
            ))

    if kwargs:
        for text in kwargs.values():
            buttons.append(KeyboardButton(
                text=text
            ))

    kb_builder.row(*buttons, width=width)

    if lst_button:
        kb_builder.row(KeyboardButton(
            text=lst_button
            ))

    return kb_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
        )

main_menu_kb = create_kb(2, **LEXICON_MAIN_MENU_COMMANDS)