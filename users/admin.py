from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from products.models import CartObject

User = get_user_model()


class CartObjectInline(admin.TabularInline):
    model = CartObject
    raw_id_fields = ('product',)
    list_select_related = ('product',)
    verbose_name = 'Продукт в корзине'
    verbose_name_plural = 'Корзина'


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name',
                    'last_name', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': (
            'first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': (
            'is_active', 'is_staff', 'is_superuser')}),
    )
    list_filter = ('username', 'email')
    inlines = (CartObjectInline,)
