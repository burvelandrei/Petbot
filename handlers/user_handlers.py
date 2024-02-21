from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU


router = Router()

# Хэндлер на команду /start
@router.message(CommandStart())
async def process_start(message:Message):
    await message.answer(text=LEXICON_RU["start"])


# Хэндлер на команду /help
@router.message(Command(commands='help'))
async def process_help(message:Message):
    await message.answer(text=LEXICON_RU["help"])


# Хэндлер на команду /contacts
@router.message(Command(commands='contacts'))
async def process_contacts(message:Message):
    await message.answer(text=LEXICON_RU["contacts"])
