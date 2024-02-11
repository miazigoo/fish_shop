from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from shop import get_products


class NumbersCallbackFactory(CallbackData, prefix="quantity"):
    action: str
    value: Optional[int] = None


def get_menu_buttons(products):
    builder = InlineKeyboardBuilder()
    for key, product in enumerate(products['data']):
        builder.button(
            text=product['attributes']['title'],
            callback_data=NumbersCallbackFactory(action="product_id", value=product['id'])
        )
    builder.button(text='🧺Моя корзина', callback_data='cart')
    builder.adjust(2)
    return builder.as_markup()


def get_quantity():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="+1", callback_data=NumbersCallbackFactory(action="change", value=1)
    )

    builder.button(
        text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1)
    )
    builder.button(
        text="+5", callback_data=NumbersCallbackFactory(action="change", value=5)
    )

    builder.button(
        text="-5", callback_data=NumbersCallbackFactory(action="change", value=-5)
    )

    builder.button(
        text="✅ Добавить", callback_data=NumbersCallbackFactory(action="add")
    )
    builder.adjust(2)
    builder.button(text='🔙В меню', callback_data='to_start')
    return builder.as_markup()


def get_start_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Добавить в корзину', callback_data='select_quantity')
    builder.button(text='🧺Моя корзина', callback_data='cart')
    builder.button(text='🔙В меню', callback_data='to_start')
    builder.adjust(2)
    return builder.as_markup()


def get_cart_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text='❌ Убрать 1 товар', callback_data='del_product')
    builder.button(text='🗑❌ Очистить корзину', callback_data='del_all_product_in_cart')

    builder.button(text='💰 Оплатить', callback_data='to_pay')
    builder.button(text='🔙В меню', callback_data='to_start')
    builder.adjust(2)
    return builder.as_markup()


def get_cart_item_for_del(cart_products):
    builder = InlineKeyboardBuilder()
    for _, item in enumerate(cart_products):
        product = item['attributes']['product']['data']['attributes']
        builder.button(
            text=f'{product["title"]}',
            callback_data=NumbersCallbackFactory(action="del_item", value=item['id'])
        )
    builder.button(text='🔙 В меню', callback_data='to_start')
    builder.adjust(2)
    return builder.as_markup()


def get_to_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙В меню', callback_data='to_start')
    return builder.as_markup()


def get_keyboard_menu_cart():
    builder = InlineKeyboardBuilder()
    builder.button(text='🧺Моя корзина', callback_data='cart')
    builder.button(text='🔙В меню', callback_data='to_start')
    builder.adjust(2)
    return builder.as_markup()


def get_keyboard_yes_no():
    builder = InlineKeyboardBuilder()
    builder.button(text='✅Да', callback_data=NumbersCallbackFactory(action="select_yes_no", value=1))
    builder.button(text='❌Нет', callback_data=NumbersCallbackFactory(action="select_yes_no", value=0))
    builder.button(text='🔙В меню', callback_data='to_start')
    builder.adjust(2)
    return builder.as_markup()
