import requests

# base_url = 'http://localhost:1337'


def get_products(base_url):
    response = requests.get(f'{base_url}/api/products')
    response.raise_for_status()
    return response.json()


def get_product(base_url, product_id):
    response = requests.get(f'{base_url}/api/products/{product_id}')
    response.raise_for_status()
    raw_product = response.json().get('data')
    return raw_product


def get_product_image(base_url, image_id):
    url = f'{base_url}/api/products/{image_id}'
    payload = {
        'populate': '*',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    image_link = response.json().get('data').get('attributes').get('picturie') \
        .get('data')[0].get('attributes').get('url')
    image_url = f'{base_url}{image_link}'
    return image_url


def get_cart(base_url, tg_id):
    url = f'{base_url}/api/carts'
    payload = {
        'filters[tg_id][$eq]': tg_id,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    cart = response.json()
    if cart['data']:
        return cart['data'][0]['id']
    payload = {
        'data': {
            'tg_id': tg_id,
            'type': 'card_products',
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()['data']['id']


def put_product_in_cart(base_url, product_id, quantity, tg_id):
    url = f'{base_url}/api/card-products'
    payload = {
        "data": {
            'quantity': float(quantity),
            'type': 'card_product',
            'product': {
                'connect': [product_id]
            },
            'cart': {
                'connect': [get_cart(base_url, tg_id)]
            },
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def show_cart(base_url, tg_id):
    cart_id = get_cart(base_url, tg_id)
    url = f'{base_url}/api/carts/{cart_id}'
    payload = {
        'populate': '*',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def get_cart_product(base_url, cart_product_id):
    url = f'{base_url}/api/card-products/{cart_product_id}'
    payload = {
        'populate': '*',
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def update_product_in_cart(base_url, quantity, tg_id, cart_product_id):
    url = f'{base_url}/api/card-products/{cart_product_id}'
    payload = {
        "data": {
            'quantity': float(quantity),
            'cart': {
                'connect': [get_cart(base_url, tg_id)]
            },
        }
    }
    response = requests.put(url, json=payload)
    response.raise_for_status()
    return response.json()


def delete_cart_products(base_url, cart_product_id):
    response = requests.delete(f'{base_url}/api/card-products/{cart_product_id}')
    response.raise_for_status()
    return response.json()


def create_customer(base_url, customer_name, customer_email, tg_id):
    url = f'{base_url}/api/users'
    payload = {
        'filters[email][$eq]': customer_email,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    find_user = response.json()
    if find_user:
        return find_user[0]['id']

    payload = {
            "blocked": False,
            "confirmed": True,
            "username": f'{customer_name} tg_id:{tg_id}',
            "email": customer_email,
            "password": "123456789",
            "role": 1,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json().get('id')


def update_cart(base_url, cart_id, user_id):
    url = f'{base_url}/api/carts/{cart_id}'
    payload = {
        "data": {
            'users_permissions_users': user_id,
        }
    }
    response = requests.put(url, json=payload)
    response.raise_for_status()
    return response.json()
