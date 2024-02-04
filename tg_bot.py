import logging
import os

from aiogram import Bot, Dispatcher
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import tg_common, tg_shop
from redis_connection import get_redis_pool

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    load_dotenv()
    base_url = os.getenv('BASE_URL')
    redis_connect = get_redis_pool()
    redis_connect.set('base_url', base_url)

    tg_token = os.getenv("TGTOKEN")
    admin_id = os.getenv('TELEGRAM_ADMIN_ID')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp['redis_connect'] = redis_connect

    bot = Bot(token=tg_token)
    dp.include_router(tg_common.router)
    dp.include_router(tg_shop.router)
    logger.info('Telegram bot started')

    await bot.send_message(admin_id, 'Telegram bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
