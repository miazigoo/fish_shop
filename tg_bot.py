import logging
import os
import asyncio

import redis
from redis.backoff import ConstantBackoff
from redis.exceptions import NoPermissionError
from redis.retry import Retry

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import tg_common, tg_shop
from shop import get_products

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    load_dotenv()
    base_url = os.getenv('BASE_URL')
    tg_token = os.getenv("TGTOKEN")
    admin_id = os.getenv('TELEGRAM_ADMIN_ID')

    redis_pool = redis.ConnectionPool(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=os.getenv('REDIS_PORT', 6379),
        retry=Retry(ConstantBackoff(10), 30),
        retry_on_error=[
            ConnectionError, TimeoutError, NoPermissionError, ConnectionRefusedError, PermissionError
        ],
        socket_timeout=300,
        socket_connect_timeout=300,
        health_check_interval=300,
    )
    redis_connection = redis.StrictRedis(connection_pool=redis_pool, db=0)

    products = get_products(base_url)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp['redis_connect'] = redis_connection
    dp['base_url'] = base_url
    dp['products'] = products

    bot = Bot(token=tg_token)
    dp.include_router(tg_common.router)
    dp.include_router(tg_shop.router)
    logger.info('Telegram bot started')

    await bot.send_message(admin_id, 'Telegram bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
