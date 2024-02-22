from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import lexicon


def create_inline_kb(width: int,
                     *args: str,
                     lst_button: str|None = None,
                     **kwargs: str
                     ) ->InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=lexicon.LEXICON_HI[button] if button in lexicon.LEXICON_HI else button,
                callback_data=button
            ))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))

    kb_builder.row(*buttons, width=width)

    if lst_button:
        kb_builder.row(InlineKeyboardButton(
            text=lst_button,
            callback_data="lst_button"
        ))

    return kb_builder.as_markup()

name_request = create_inline_kb(1, **lexicon.LEXICON_NAME_REQUEST)
number_request = create_inline_kb(2, **lexicon.LEXICON_NUMBER_REQUEST)
