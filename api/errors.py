from dataclasses import dataclass

from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.response import Response

messages = {'already_in_cart': 'Этот продукт уже есть в корзине',
            'not_in_cart': 'Этого продукта нет в корзине',
            'not_less_1': 'Количество не может быть меньше 1'}


@dataclass
class ErrorMessage:
    status: int
    key: str
    message: str

    def get_errors_context(self):
        return {self.key: self.message}

    def get_error_response(self):
        return Response(self.get_errors_context(), self.status)


def err_dict(err, description):
    return {err.status: openapi.Response(
        description, examples={'application/json': err.get_errors_context()})}


err_already_in_cart = ErrorMessage(
    status=status.HTTP_400_BAD_REQUEST, key='errors',
    message=messages['already_in_cart'])
err_not_in_cart = ErrorMessage(
    status=status.HTTP_400_BAD_REQUEST, key='errors',
    message=messages['not_in_cart'])
err_404_not_found = ErrorMessage(status=status.HTTP_404_NOT_FOUND,
                                 key='detail', message=NotFound.default_detail)
err_401_unauthorized = ErrorMessage(status=status.HTTP_401_UNAUTHORIZED,
                                    key='detail',
                                    message=NotAuthenticated.default_detail)

err_dict_404_not_found = err_dict(err_404_not_found, 'Объект не найден')
err_dict_401_unauthorized = err_dict(err_401_unauthorized,
                                     'Пользователь не авторизован')
