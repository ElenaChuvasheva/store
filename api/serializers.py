from decimal import Decimal
from functools import partial

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from api.errors import messages
from products.models import CartObject, Category, Product, Subcategory

User = get_user_model()

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories', 'image')


class ImageListField(serializers.ListField):
    child = serializers.ImageField()

class CustomImageSerializer(ImageListField):
    def to_representation(self, value):
        sizes = ('128x128', '256x256', '512x512',)
        request = self.context.get('request', None)
        return [request.build_absolute_uri(
            get_thumbnail(value, size).url) for size in sizes]


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.PrimaryKeyRelatedField(
        source='subcategory.category.name', read_only=True)
    images = CustomImageSerializer(source='image')
    price = serializers.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     coerce_to_string=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'subcategory',
                  'price', 'category', 'images')

#    @swagger_serializer_method(serializer_or_field=serializers.ListField(child=serializers.ImageField()))
#    def get_images(self, obj):
#        sizes = ('128x128', '256x256', '512x512',)
#        request = self.context.get('request', None)
#        return [request.build_absolute_uri(
#            get_thumbnail(obj.image, size).url) for size in sizes]


ProductImageSerializer = partial(HyperlinkedSorlImageField,
                                 source='image',)

class ProductNotImageListSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.PrimaryKeyRelatedField(
        source='subcategory.category.name', read_only=True)
    price = serializers.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     coerce_to_string=False)   
    image_large = ProductImageSerializer('512x512')
    image_medium = ProductImageSerializer('256x256')
    image_small = ProductImageSerializer('128x128')

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'subcategory',
                  'price', 'category', 'image_small',
                  'image_medium', 'image_large')


class ProductSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')

class CartObjectSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='product.pk',
#                                            queryset=Cart.objects.all(),
                                            read_only=True)
    name = serializers.CharField(source='product.name', read_only=True)
    amount = serializers.IntegerField()
    price = serializers.DecimalField(source='product.price', max_digits=6,
                                     decimal_places=2,
                                     coerce_to_string=False,
                                     read_only=True)

#    total_price = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     coerce_to_string=False,
                                     read_only=True)

    class Meta:
        model= CartObject
#        list_serializer_class = CartSerializer
        fields = ('id', 'name', 'amount', 'price', 'total_price')
    
    def validate_amount(self, value):
        return value if value >= 1 else 1
    
#    @swagger_serializer_method(serializer_or_field=serializers.DecimalField(max_digits=6, decimal_places=2, coerce_to_string=False))
#    def get_total_price(self, obj):
#        return obj.amount*obj.product.price

class CartListSerializer(serializers.ListSerializer):
    child = CartObjectSerializer()
#    wtf = serializers.SerializerMethodField()

    class Meta:
        fields = ('child')

#    def get_wtf(self, obj):
#        return 1

class CartSerializer(serializers.Serializer):
# class CartSerializer(serializers.ModelSerializer):
    # products = CartListSerializer(source='cart_of')
    cart_of = CartObjectSerializer(many=True)
    # products = CartObjectSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
#        model = User
        fields = ('cart_of', 'wtf')

    @swagger_serializer_method(serializer_or_field=serializers.DecimalField(max_digits=6, decimal_places=2, coerce_to_string=False))
    def get_total(self, obj):
        sum = Decimal('0')
        for cart_object in obj.cart_of.all():
            sum += cart_object.total_price
        print(sum)
        print(type(sum))
        return sum


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'password', 'first_name', 'last_name')

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
