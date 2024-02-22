from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from keyboards import inline_keyboards
from lexicon.lexicon import LEXICON_HI

# Нужно написать два фильтра, для фильтрации имени и номера!!!!!

router = Router()

class FSMprofile(StatesGroup):
    name_request  = State()
    number_request = State()

# Хэндлер на команду /start
@router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON_HI["start"], reply_markup=inline_keyboards.name_request)


@router.callback_query(F.data == "yes_name", StateFilter(default_state))
async def name_request(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_HI['yes_name'])
    await callback.answer()
    await state.set_state(FSMprofile.name_request)


@router.message(F.text, StateFilter(FSMprofile.name_request))
async def number_request(message: Message, state: FSMContext):
    # Сохраняем имя в базу
    await message.answer(text=LEXICON_HI['number_request'], reply_markup=inline_keyboards.number_request)
    await state.set_state(FSMprofile.number_request)

@router.message(StateFilter(FSMprofile.name_request))
async def warning_name(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=LEXICON_HI['warning_name'])
    await state.set_state(FSMprofile.name_request)


@router.callback_query(F.data == "yes_number", StateFilter(FSMprofile.number_request))
async def yes_number(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_HI['yes_number'])
    await callback.answer()
    await state.set_state(FSMprofile.number_request)

@router.message(F.text, StateFilter(FSMprofile.number_request))
async def number_save(message: Message, state: FSMContext):
    # Сохраняем номер в базу и перводим на следующий шаг
    # следующий шаг
    await state.clear()

@router.message(StateFilter(FSMprofile.number_request))
async def warning_number(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=LEXICON_HI['warning_number'])
    await state.set_state(FSMprofile.number_request)



# # Хэндлер на команду /help
# @router.message(Command(commands='help'))
# async def process_help(message:Message):
#     await message.answer(text=LEXICON_HI["help"])


# # Хэндлер на команду /contacts
# @router.message(Command(commands='contacts'))
# async def process_contacts(message:Message):
#     await message.answer(text=LEXICON_HI["contacts"])
