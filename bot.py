import asyncio
from aiogram import Bot, Dispatcher
import config
import logging
from datetime import datetime

from handlers import start, authors, help

bot = Bot(config.BOT_TOKEN)

async def run_bot():
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        authors.router,
        help.router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(filename=f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H')}.log", filemode='a', level=logging.DEBUG)
    asyncio.run(run_bot())