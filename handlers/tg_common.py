from aiogram import Router, types
from aiogram.filters import Command

from keyboards.tg_keyboards import get_menu_buttons

router = Router()


@router.message(Command("start"))
async def process_start_command(message: types.Message, products):
    await message.answer("Добро пожаловать в магазин рыбы!🐠🐡🐟",
                         reply_markup=get_menu_buttons(products))


@router.message(Command('help'))
async def process_help_command(message: types.Message, products):
    await message.reply("Чтобы начать, нажмите: /start",
                        reply_markup=get_menu_buttons(products))


@router.message(Command('cancel'))
async def process_help_command(message: types.Message, products):
    await message.answer("Добро пожаловать в магазин рыбы!🐠🐡🐟",
                         reply_markup=get_menu_buttons(products))
