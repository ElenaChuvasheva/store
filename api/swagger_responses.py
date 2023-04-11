from djoser.constants import Messages
from drf_yasg import openapi
from rest_framework import status
from rest_framework.validators import UniqueTogetherValidator

from api.errors import (err_already_in_cart, err_dict_401_unauthorized,
                        err_dict_404_not_found, err_not_in_cart, messages)
from api.serializers import CartSerializer, CustomUserSerializer

token_logout_responses = {status.HTTP_204_NO_CONTENT: openapi.Response(
    'Токен удалён'), **err_dict_401_unauthorized}
token_login_responses = {
    status.HTTP_200_OK: openapi.Response(
        'Токен получен',
        examples={
            'application/json': {
                'auth_token': 'b7f998457067d2ff1d0d78d31c36fa28e372ae7b'
            }
        }
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        'Невозможно войти с предоставленными учётными данными',
        examples={
            'application/json': {
                'non_field_errors': [Messages.INVALID_CREDENTIALS_ERROR]
            }
        }
    )
}

user_get_me_responses = {
    status.HTTP_200_OK: openapi.Response(
        'Успешное получение информации из профиля',
        CustomUserSerializer), **err_dict_401_unauthorized}
user_post_responses = {
    status.HTTP_201_CREATED: openapi.Response(
        'Пользователь создан',
        CustomUserSerializer),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        'Ошибки валидации',
        examples={
            'application/json': {
                'email': [UniqueTogetherValidator.missing_message]
            }
        }
    )
}

post_shopping_cart_responses = {
    status.HTTP_201_CREATED: openapi.Response(
        'Успешное добавление в корзину'),
    err_already_in_cart.status: openapi.Response(
        'Продукт уже есть в корзине',
        examples={
            'application/json': err_already_in_cart.get_errors_context()
        }), **err_dict_404_not_found, **err_dict_401_unauthorized}

patch_shopping_cart_responses = {
    status.HTTP_200_OK: openapi.Response('Успешное изменение количества'),
    err_not_in_cart.status: openapi.Response(
        'Продукта нет в корзине',
        examples={
            'application/json': err_not_in_cart.get_errors_context()
        }),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        'Ошибки валидации',
        examples={
            'application/json': {
                'amount': [messages['not_less_1']]
            }
        }
    ), **err_dict_404_not_found, **err_dict_401_unauthorized,
}

delete_shopping_cart_responses = {
    status.HTTP_204_NO_CONTENT: openapi.Response(
        'Успешное удаление из корзины'),
    err_not_in_cart.status: openapi.Response(
        'Продукта нет в корзине',
        examples={'application/json': err_not_in_cart.get_errors_context()}),
    **err_dict_404_not_found, **err_dict_401_unauthorized}

get_all_cart_responses = {
    status.HTTP_200_OK: openapi.Response(
        'Получен список продуктов в корзине', CartSerializer),
    **err_dict_401_unauthorized
}

delete_all_cart_responses = {
    status.HTTP_204_NO_CONTENT: openapi.Response(
        'Успешная очистка корзины'), **err_dict_401_unauthorized
}
