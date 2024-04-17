import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
import logging
from datetime import datetime

from handlers import start, authors, help, news

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def run_bot():
    dp.include_routers(
        start.router,
        authors.router,
        help.router,
        news.router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(filename=f"logs/log_{datetime.now().strftime('%Y-%m-%d_%H')}.log", filemode='a', level=logging.DEBUG)
    asyncio.run(run_bot())