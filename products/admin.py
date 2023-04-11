from django.contrib import admin

from products.models import Category, Product, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'get_subcategories')

    def get_subcategories(self, obj):
        return '; '.join([p.__str__() for p in obj.subcategories.all()])
    
    get_subcategories.short_description = 'ПОДКАТЕГОРИИ'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'category')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'subcategory', 'get_category')
    list_filter = ('subcategory', 'subcategory__category')
    search_fields = ('name',)

    def get_category(self, obj):
        return obj.subcategory.category.name
    
    get_category.short_description = 'КАТЕГОРИЯ'
