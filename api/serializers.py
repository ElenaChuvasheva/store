from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from products.models import Category, Product, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories', 'image')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.PrimaryKeyRelatedField(
        source='subcategory.category.name', read_only=True)
    image_large = HyperlinkedSorlImageField(
        '512x512',
        options={"crop": "center"},
        source='image',
    )
    image_medium = HyperlinkedSorlImageField(
        '256x256',
        options={"crop": "center"},
        source='image',
    )
    image_small = HyperlinkedSorlImageField(
        '128x128',
        options={"crop": "center"},
        source='image',
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'subcategory',
                  'price', 'category', 'image_large',
                  'image_medium', 'image_small')
