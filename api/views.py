from rest_framework import generics

from api.pagination import CategoryPagination, ProductPagination
from api.serializers import CategorySerializer, ProductSerializer
from products.models import Category, Product


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
