from aiogram import Router, types, F
from aiogram.filters import Command

from keyboards.tg_keyboards import get_menu_buttons

router = Router()


@router.message(Command("start"))
async def process_start_command(message: types.Message, redis_connect):
    await message.answer("Добро пожаловать в магазин рыбы!🐠🐡🐟",
                         reply_markup=get_menu_buttons(redis_connect))


@router.message(Command('help'))
async def process_help_command(message: types.Message, redis_connect):
    await message.reply("Чтобы начать, нажмите: /start",
                        reply_markup=get_menu_buttons(redis_connect))


@router.message(Command('cancel'))
async def process_help_command(message: types.Message, redis_connect):
    await message.answer("Добро пожаловать в магазин рыбы!🐠🐡🐟",
                         reply_markup=get_menu_buttons(redis_connect))
