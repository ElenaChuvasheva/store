from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from products.models import Cart

User = get_user_model()

class CartInline(admin.TabularInline):
    model = Cart
    raw_id_fields = ('product',)
    list_select_related = ('product',)
    verbose_name = 'Продукт в корзине'
    verbose_name_plural = 'Корзина'

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': (
            'first_name', 'last_name', 'email')}),
        ('Права доступа', {'fields': (
            'is_active', 'is_staff', 'is_superuser')}),
    )
    list_filter = ('username', 'email')
    inlines = (CartInline,)

    def get_list_display(self, request):
        return ['pk', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'is_staff']
