import requests
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.errors import err_404_not_found, err_already_in_cart, err_not_in_cart
from api.pagination import CategoryPagination, ProductPagination
from api.serializers import (CartObjectSerializer, CategorySerializer,
                             CustomUserCreateSerializer, CustomUserSerializer,
                             ProductNotImageListSerializer, ProductSerializer)
from products.models import Cart, Category, Product

token_login = swagger_auto_schema(
      method='POST', tags=['Авторизация'], operation_id='Получение токена',
      operation_description='Получение токена авторизации для входа в систему',
      security=[])(TokenCreateView.as_view())
token_logout = swagger_auto_schema(
      method='POST', tags=['Авторизация'], operation_id='Удаление токена',
      operation_description='Удаление токена авторизации при выходе из системы')(
        TokenDestroyView.as_view())

user_get_me_responses = {status.HTTP_200_OK: openapi.Response('Успешное получение информации из профиля',
                                                           CustomUserSerializer)}
user_post_responses = {status.HTTP_201_CREATED: openapi.Response('Пользователь создан',
                                                                 CustomUserSerializer),
                        status.HTTP_400_BAD_REQUEST: openapi.Response(
        'Ошибки валидации', examples={'application/json': {'email': [
        'This field is required.'
    ]}})}

@swagger_auto_schema(method='GET', tags=['Пользователи'], operation_id='Профиль пользователя',
                     operation_description='Профиль пользователя',
                     responses=user_get_me_responses)
@api_view(['GET'])
def users_me(request):
    return UserViewSet.as_view({'get': 'me'})(request._request)


@swagger_auto_schema(method='POST', tags=['Пользователи'], operation_id='Регистрация пользователя',
                     operation_description='Регистрация пользователя',
                     responses=user_post_responses,
                     request_body=CustomUserCreateSerializer,
                     security=[])
@api_view(['POST'])
def users_create(request):
    return UserViewSet.as_view({'post': 'create'})(request._request)

post_shopping_cart_responses = {
    status.HTTP_201_CREATED: openapi.Response(
        'Успешное добавление в корзину', CartObjectSerializer),
    err_already_in_cart.status: openapi.Response(
        'Продукт уже есть в корзине', examples={'application/json': err_already_in_cart.get_errors_context()}),
    err_404_not_found.status: openapi.Response(
        'Объект не найден', examples={'application/json': err_404_not_found.get_errors_context()})
}

patch_shopping_cart_responses = {
    status.HTTP_200_OK: openapi.Response(
        'Успешное изменение количества', CartObjectSerializer),
    err_not_in_cart.status: openapi.Response(
        'Продукта нет в корзине', examples={'application/json': err_not_in_cart.get_errors_context()}),
    err_404_not_found.status: openapi.Response(
        'Объект не найден', examples={'application/json': err_404_not_found.get_errors_context()})
}

delete_shopping_cart_responses = {
    status.HTTP_204_NO_CONTENT: openapi.Response('Успешное удаление из корзины'),
    err_not_in_cart.status: openapi.Response(
        'Продукта нет в корзине', examples={'application/json': err_not_in_cart.get_errors_context()}),
    err_404_not_found.status: openapi.Response(
        'Объект не найден', examples={'application/json': err_404_not_found.get_errors_context()})
}


get_product_responses = {
    status.HTTP_200_OK: openapi.Response(
        'Успешное получение данных о продукте', ProductSerializer),
    err_404_not_found.status: openapi.Response(
        'Объект не найден', examples={'application/json': err_404_not_found.get_errors_context()})

}

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination

categories_view = swagger_auto_schema(
      method='GET', tags=['Категории'], operation_id='Список категорий',
      security=[])(
          CategoryListView.as_view())


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Получение списка продуктов',
    operation_id='Список продуктов', tags=['Продукты'], security=[]
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Получение информации о продукте',
    operation_id='Продукт', tags=['Продукты'],
    responses=get_product_responses, security=[]
))
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # на случай, если выдача рисунков списком некритична:
    # serializer_class = ProductNotImageListSerializer
    pagination_class = ProductPagination


    @swagger_auto_schema(method='POST',
                         request_body=no_body,
                         responses=post_shopping_cart_responses,
                         tags=['Корзина'],
                         operation_id='Добавление продукта в корзину')
    @swagger_auto_schema(method='PATCH',
                         request_body=CartObjectSerializer,
                         responses=patch_shopping_cart_responses,
                         tags=['Корзина'],
                         operation_id='Изменение количества продукта в корзине')
    @swagger_auto_schema(method='DELETE',
                         responses=delete_shopping_cart_responses,
                         tags=['Корзина'],
                         operation_id='Удаление продукта из корзины')
    @action(detail=True, methods=('POST', 'PATCH', 'DELETE',),
            url_path='shopping_cart')
    def shopping_cart_detail(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        current_user = request.user
        cart_objects = current_user.cart_of.filter(product=product)
        match request.method:
            case 'POST':
                if not cart_objects.exists():
                    cart_object = Cart.objects.create(
                        user=self.request.user, product=product)
                    serializer = CartObjectSerializer(cart_object)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return err_already_in_cart.get_error_response()
            case 'PATCH':
                if cart_objects.exists():
                    cart_object = cart_objects[0]
                    serializer = CartObjectSerializer(cart_object,
                                                data=request.data,
                                                partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return err_not_in_cart.get_error_response()
            case 'DELETE':
                if not cart_objects.exists():
                    return err_not_in_cart.get_error_response()
                cart_objects[0].delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


delete_all_cart_responses = {status.HTTP_204_NO_CONTENT: openapi.Response('Успешная очистка корзины')}

@swagger_auto_schema(method='GET',
                     responses=delete_shopping_cart_responses,
                     tags=['Корзина'],
                     operation_id='Получение списка продуктов в корзине')
@swagger_auto_schema(method='DELETE',
                     responses=delete_all_cart_responses,
                     tags=['Корзина'],
                     operation_id='Очистка корзины')
@api_view(('GET', 'DELETE',))
def cart_view(request):
    match request.method:
        case 'DELETE':
            request.user.cart_of.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response('lol', status=status.HTTP_200_OK)


class UserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/auth/verify/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data = post_data)
        content = result.text
        return Response(content)
