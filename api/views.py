from django.contrib.auth import get_user_model
from django.db.models import F, Prefetch
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from api import swagger_responses
from api.errors import (err_already_in_cart, err_dict_404_not_found,
                        err_not_in_cart)
from api.pagination import CategoryPagination, ProductPagination
from api.serializers import (CartObjectSerializer, CartSerializer,
                             CategorySerializer, CustomUserCreateSerializer,
                             ProductSerializer)
from products.models import CartObject, Category, Product

User = get_user_model()

token_login = swagger_auto_schema(
    method='POST', tags=['Авторизация'], operation_id='Получение токена',
    operation_description='Получение токена авторизации для входа в систему',
    security=[],
    responses=swagger_responses.token_login_responses)(
        TokenCreateView.as_view())
token_logout = swagger_auto_schema(
    method='POST', tags=['Авторизация'], operation_id='Удаление токена',
    operation_description='Удаление токена авторизации при выходе из системы',
    responses=swagger_responses.token_logout_responses)(
        TokenDestroyView.as_view())


@swagger_auto_schema(method='GET', tags=['Пользователи'],
                     operation_id='Профиль пользователя',
                     operation_description='Профиль пользователя',
                     responses=swagger_responses.user_get_me_responses)
@api_view(['GET'])
def users_me(request):
    return UserViewSet.as_view({'get': 'me'})(request._request)


@swagger_auto_schema(method='POST', tags=['Пользователи'],
                     operation_id='Регистрация пользователя',
                     operation_description='Регистрация пользователя',
                     responses=swagger_responses.user_post_responses,
                     request_body=CustomUserCreateSerializer,
                     security=[])
@api_view(['POST'])
def users_create(request):
    return UserViewSet.as_view({'post': 'create'})(request._request)


get_product_responses = {**{
    status.HTTP_200_OK: openapi.Response(
        'Успешное получение данных о продукте', ProductSerializer),
}, **err_dict_404_not_found}


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


categories_view = swagger_auto_schema(
    method='GET', tags=['Категории'], operation_id='Список категорий',
    security=[])(
        CategoryListView.as_view())


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=('Получение списка продуктов. '
                           'Доступна фильтрация по id категории '
                           'и подкатегории, поиск по названию.'),
    operation_id='Список продуктов', tags=['Продукты'], security=[]
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description='Получение информации о продукте',
    operation_id='Продукт', tags=['Продукты'],
    responses=get_product_responses, security=[]
))
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().select_related()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('subcategory', 'category',)
    search_fields = ('name',)

    @swagger_auto_schema(
        method='POST', request_body=no_body,
        responses=swagger_responses.post_shopping_cart_responses,
        tags=['Корзина'],
        operation_id='Добавление продукта в корзину')
    @swagger_auto_schema(
        method='PATCH',
        request_body=CartObjectSerializer,
        responses=swagger_responses.patch_shopping_cart_responses,
        tags=['Корзина'],
        operation_id='Изменение количества продукта в корзине')
    @swagger_auto_schema(
        method='DELETE',
        responses=swagger_responses.delete_shopping_cart_responses,
        tags=['Корзина'],
        operation_id='Удаление продукта из корзины')
    @action(detail=True, methods=('POST', 'PATCH', 'DELETE',),
            url_path='shopping_cart',
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart_detail(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        current_user = request.user
        cart_objects = current_user.cart_of.filter(product=product)
        match request.method:
            case 'POST':
                if not cart_objects.exists():
                    CartObject.objects.create(
                        user=self.request.user, product=product)
                    return Response(status=status.HTTP_201_CREATED)
                return err_already_in_cart.get_error_response()
            case 'PATCH':
                if cart_objects.exists():
                    cart_object = cart_objects[0]
                    serializer = CartObjectSerializer(
                        cart_object,
                        data=request.data,
                        partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return err_not_in_cart.get_error_response()
            case 'DELETE':
                if not cart_objects.exists():
                    return err_not_in_cart.get_error_response()
                cart_objects.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='GET',
    responses=swagger_responses.get_all_cart_responses,
    tags=['Корзина'],
    operation_id='Получение списка продуктов в корзине')
@swagger_auto_schema(
    method='DELETE',
    responses=swagger_responses.delete_all_cart_responses,
    tags=['Корзина'],
    operation_id='Очистка корзины')
@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def shopping_cart_view(request):
    current_user = request.user
    match request.method:
        case 'GET':
            user_obj = User.objects.prefetch_related(
                Prefetch(
                    'cart_of',
                    queryset=CartObject.objects.select_related(
                        'product').annotate(
                            total_price=F('amount') * F('product__price')))
            ).get(pk=current_user.id)
            serializer = CartSerializer(user_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        case 'DELETE':
            current_user.cart_of.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
