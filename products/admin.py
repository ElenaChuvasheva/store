from django.contrib import admin

from products.models import Category, Product, Subcategory

admin.site.register(Category)
admin.site.register(Subcategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'subcategory', 'get_category')

    def get_category(self, obj):
        return obj.subcategory.category.name
