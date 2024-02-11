from contextlib import suppress

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile

from keyboards.tg_keyboards import get_start_menu, get_menu_buttons, get_quantity, NumbersCallbackFactory, \
    get_cart_menu, get_cart_item_for_del, get_to_menu, get_keyboard_menu_cart, get_keyboard_yes_no
from shop import get_product, get_product_image, put_product_in_cart, show_cart, get_cart_product, \
    update_product_in_cart, delete_cart_products, create_customer, get_cart, update_cart

router = Router()

DATA = {}


class Customer(StatesGroup):
    input_email = State()


@router.callback_query(F.data == "to_start")
async def start_menu(callback: types.CallbackQuery, products):
    try:
        await callback.message.edit_text("Добро пожаловать в магазин рыбы!🐠🐡🐟",
                                         reply_markup=get_menu_buttons(products))
    except TelegramBadRequest:
        await callback.message.delete()
        await callback.message.answer("Добро пожаловать в магазин рыбы!🐠🐡🐟",
                                      reply_markup=get_menu_buttons(products))
    await callback.answer()


@router.callback_query(NumbersCallbackFactory.filter(F.action == "product_id"))
async def handle_description(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        redis_connect
):
    if callback_data.action == "product_id":
        base_url = redis_connect.get('base_url').decode('utf-8')
        product_id = callback_data.value
        product = get_product(base_url, product_id)['attributes']
        redis_connect.set(f'product_id_{callback.from_user.id}', product_id)
        img_url = get_product_image(base_url, product_id)

        image_from_url = URLInputFile(f'{img_url}')
        text = f"{product['title']}\n\n{product['descriptions']}\n\n{product['price']} руб."
        await callback.message.delete()
        await callback.message.answer_photo(
            image_from_url,
            caption=text,
            reply_markup=get_start_menu()
        )

        await callback.answer()


@router.callback_query(NumbersCallbackFactory.filter(F.action == "add"))
async def handle_add_to_cart(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        redis_connect
):
    base_url = redis_connect.get('base_url').decode('utf-8')
    if callback_data.action == "add":
        tg_id = callback.from_user.id
        quantity = int(redis_connect.get(f'quantity_{tg_id}').decode('utf-8'))
        product_id = redis_connect.get(f'product_id_{tg_id}').decode('utf-8')

        cart = show_cart(base_url, f'{tg_id}')
        if cart['data']['attributes']['card_products']['data']:
            for _, item in enumerate(cart['data']['attributes']['card_products']['data']):
                product = get_cart_product(base_url, item['id'])
                if product['data']['attributes']['product']['data']['id'] == int(product_id):
                    quantity += product['data']['attributes']['quantity']

                    update_product_in_cart(base_url, quantity, str(tg_id), item['id'])
        else:
            put_product_in_cart(base_url, int(product_id), quantity, str(tg_id))
        await callback.message.edit_text(
            f"Товар добавлен в корзину",
            reply_markup=get_keyboard_menu_cart())

        await callback.answer()


@router.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def handle_select_quantity(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        redis_connect
):
    tg_id = callback.from_user.id
    quantity = int(redis_connect.get(f'quantity_{tg_id}').decode('utf-8'))

    if callback_data.action == "change":
        num = quantity + callback_data.value
        if num < 1:
            num = 1
        redis_connect.set(f'quantity_{tg_id}', num)
        await update_num_text(callback.message, num)

    await callback.answer()


async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Выберите количество: {new_value}",
            reply_markup=get_quantity()
        )


@router.callback_query(F.data == "select_quantity")
async def handle_cart(callback: types.CallbackQuery, redis_connect):
    redis_connect.set(f'quantity_{callback.from_user.id}', 1)
    await callback.message.delete()
    await callback.message.answer(text='Выберите количество: 1',
                                  reply_markup=get_quantity())
    await callback.answer()


@router.callback_query(F.data == "cart")
async def handle_cart(callback: types.CallbackQuery, redis_connect):
    base_url = redis_connect.get('base_url').decode('utf-8')
    tg_id = callback.from_user.id
    cart = show_cart(base_url, f'{tg_id}')
    cart_products = []
    for _, item in enumerate(cart['data']['attributes']['card_products']['data']):
        product = get_cart_product(base_url, item['id'])
        cart_products.append(product['data'])

    message = ''
    total = 0
    for _, item in enumerate(cart_products):
        product = item['attributes']['product']['data']['attributes']
        message += f"🐠 *{product['title']}* \n"
        message += f"₽{product['price']} за еденицу, количество: {item['attributes']['quantity']}\n"
        cost = product['price'] * item['attributes']['quantity']
        total += cost
        message += f"Итого ₽ {cost}\n\n"

    message += f"Общая стоимость: ₽{total}"
    DATA[f"cart_products_{tg_id}"] = cart_products

    await callback.message.edit_text(message,
                                     reply_markup=get_cart_menu(),
                                     parse_mode=ParseMode.MARKDOWN_V2)
    await callback.answer()


@router.callback_query(F.data == "del_product")
async def handle_del_cart_item(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    cart_products = DATA.get(f"cart_products_{tg_id}")
    await callback.message.edit_text('Выберите товар, который нужно удалить из корзины:',
                                     reply_markup=get_cart_item_for_del(cart_products))
    await callback.answer()


@router.callback_query(NumbersCallbackFactory.filter(F.action == "del_item"))
async def handle_select_quantity(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        redis_connect
):
    base_url = redis_connect.get('base_url').decode('utf-8')
    if callback_data.action == "del_item":
        cart_product_id = callback_data.value
        delete_cart_products(base_url, cart_product_id)
        await callback.message.edit_text('Позиция удалена из корзины',
                                         reply_markup=get_to_menu())

    await callback.answer()


@router.callback_query(F.data == "del_all_product_in_cart")
async def handle_select_quantity(callback: types.CallbackQuery, redis_connect):
    base_url = redis_connect.get('base_url').decode('utf-8')
    tg_id = callback.from_user.id
    cart_products = DATA.get(f"cart_products_{tg_id}")
    for _, item in enumerate(cart_products):
        cart_product_id = item['id']
        delete_cart_products(base_url, cart_product_id)
    await callback.message.edit_text('Позиции удалены из корзины',
                                     reply_markup=get_to_menu())

    await callback.answer()


@router.callback_query(F.data == "to_pay")
async def get_email(callback: types.CallbackQuery, state: FSMContext):
    text = "Введите ваш *email* "
    await callback.message.edit_text(text=text,
                                     parse_mode=ParseMode.MARKDOWN_V2,
                                     reply_markup=get_to_menu()
                                     )
    await state.set_state(Customer.input_email)


@router.message(Customer.input_email)
async def select_email(message: Message, state: FSMContext, redis_connect):
    tg_id = message.from_user.id
    email = message.text.lower()
    redis_connect.set(f'email_{tg_id}', email)
    text = f"Вы прислали мне эту почту: {email} \nВсё верно?"
    await message.answer(
        text=text,
        reply_markup=get_keyboard_yes_no()
    )
    await state.clear()


@router.callback_query(NumbersCallbackFactory.filter(F.action == "select_yes_no"))
async def handle_select_quantity(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory,
        state: FSMContext,
        redis_connect
):
    base_url = redis_connect.get('base_url').decode('utf-8')
    tg_id = callback.from_user.id
    if callback_data.action == "select_yes_no":
        value = callback_data.value
        if value == 1:
            email = redis_connect.get(f'email_{tg_id}').decode('utf-8')
            customer_name = name if (name := callback.from_user.full_name) else 'None'
            customer_id = create_customer(base_url, customer_name, email, tg_id)
            cart_id = get_cart(base_url, tg_id)
            update_cart(base_url, cart_id, customer_id)
            await callback.message.edit_text("Ожидайте уведомлений на почте", reply_markup=get_to_menu())
            await state.clear()
        if value == 0:
            await callback.message.edit_text("Введите ваш e-mail")
            await state.set_state(Customer.input_email)

    await callback.answer()
