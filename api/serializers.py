from rest_framework import serializers

from products.models import Category, Product, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = serializers.SlugRelatedField(
        read_only=True, slug_field='name')
    category = serializers.PrimaryKeyRelatedField(
        source='subcategory.category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'subcategory', 'price', 'category')
