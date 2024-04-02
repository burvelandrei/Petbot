import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from config_data.config import load_config, Config
from handlers import user_handlers, other_handlers
from handlers.user_handlers import begin_use_dialog
from handlers.create_apointment import sign_up_dialog


logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="{filename}:{lineno} #{levelname:8} " "[{asctime}] - {name} - {message}",
        style="{",
    )

    logger.info("Starting BOT")

    config: Config = load_config()

    bot = Bot(config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(begin_use_dialog)
    dp.include_router(sign_up_dialog)
    dp.include_router(other_handlers.router)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(str(e))
    finally:
        bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
