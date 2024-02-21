import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import load_config, Config
from handlers import user_handlers, other_handlers


logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format='{filename}:{lineno} #{levelname:8} '
        '[{asctime}] - {name} - {message}',
        style='{'
    )


    logger.info('Starting BOT')

    config: Config = load_config()

    bot = Bot(config.tg_bot.token,
              parse_mode='HTML'
              )
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())