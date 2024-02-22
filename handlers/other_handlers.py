from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_HI


router = Router()

@router.message()
async def bad_input(message:Message):
    await message.delete()
