from functools import partial

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from api.errors import messages
from products.models import CartObject, Category, Product, Subcategory

User = get_user_model()

CustomDecimalField = partial(serializers.DecimalField, max_digits=6,
                             decimal_places=2, coerce_to_string=False)


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories', 'image')


class CustomImageSerializer(serializers.ListField):
    child = serializers.ImageField()

    def to_representation(self, value):
        sizes = ('128x128', '256x256', '512x512',)
        request = self.context.get('request', None)
        return [request.build_absolute_uri(
            get_thumbnail(value, size).url) for size in sizes]


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    images = CustomImageSerializer(source='image')
    price = CustomDecimalField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'subcategory',
                  'price', 'category', 'images')


class CartObjectSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='product.pk',
                                            read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    amount = serializers.IntegerField()
    price = CustomDecimalField(source='product.price', read_only=True)
    total_price = CustomDecimalField(read_only=True)

    class Meta:
        model = CartObject
        fields = ('id', 'name', 'amount', 'price', 'total_price')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(messages['not_less_1'])
        return value


class CartSerializer(serializers.ModelSerializer):
    products = CartObjectSerializer(source='cart_of', many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('products', 'total')

    @swagger_serializer_method(serializer_or_field=CustomDecimalField())
    def get_total(self, obj):
        return sum(object.total_price for object in obj.cart_of.all())


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'password', 'first_name',
                  'last_name')


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
