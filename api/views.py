import requests
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from api.errors import err_404_not_found, err_already_in_cart, err_not_in_cart
from api.pagination import CategoryPagination, ProductPagination
from api.serializers import (CartSerializer, CategorySerializer,
                             ProductNotImageListSerializer, ProductSerializer)
from products.models import Cart, Category, Product

post_shopping_cart_responses = {
    status.HTTP_201_CREATED: openapi.Response(
        'Успешное добавление в корзину', CartSerializer),
    err_already_in_cart.status: openapi.Response(
        'Продукт уже есть в корзине', examples={'application/json': err_already_in_cart.get_errors_context()}),
    err_404_not_found.status: openapi.Response(
        'Объект не найден', examples={'application/json': err_404_not_found.get_errors_context()})
}

patch_shopping_cart_responses = {
    status.HTTP_200_OK: openapi.Response(
        'Успешное изменение количества', CartSerializer),
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


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # на случай, если выдача рисунков списком некритична:
    # serializer_class = ProductNotImageListSerializer
    pagination_class = ProductPagination

#    @swagger_auto_schema(methods=['DELETE'],
#                         request_body=no_body,
#                         responses=post_shopping_cart_responses)
#    @action(detail=True, url_path='shopping_cart', methods=('POST',))
#    def shopping_cart(self, request, pk):
#        product = get_object_or_404(Product, pk=pk)
#        current_user = request.user
#        cart_objects = current_user.cart_of.filter(product=product)

#        if not cart_objects.exists():
#            cart_object = Cart.objects.create(
#                user=self.request.user, product=product)
#            serializer = CartSerializer(cart_object)
#            return Response(serializer.data,
#                            status=status.HTTP_201_CREATED)
#        return err_already_in_cart.get_error_response()
    

    @swagger_auto_schema(method='POST',
                         request_body=no_body,
                         responses=post_shopping_cart_responses)
    @swagger_auto_schema(method='PATCH',
                         request_body=CartSerializer,
                         responses=patch_shopping_cart_responses)
    @swagger_auto_schema(method='DELETE',
                         responses=delete_shopping_cart_responses)
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
                    serializer = CartSerializer(cart_object)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return err_already_in_cart.get_error_response()
            case 'PATCH':
                if cart_objects.exists():
                    cart_object = cart_objects[0]
                    serializer = CartSerializer(cart_object,
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
    

    @action(detail=False, methods=('GET', 'DELETE',),
            url_path='my_cart')
    def cart(self, request):
        return Response('lol', status=status.HTTP_200_OK)


class UserActivationView(APIView):
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/auth/verify/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data = post_data)
        content = result.text
        return Response(content)
