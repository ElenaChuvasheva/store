from django.urls import include, path
from rest_framework import routers

from api.views import (ProductViewSet, categories_view, shopping_cart_view,
                       token_login, token_logout, users_create, users_me)

app_name = 'api'

users_urls = [
    path('', users_create),
    path('me/', users_me),
]

authtoken_urls = [
    path('login/', token_login),
    path('logout/', token_logout)
]


products_router = routers.DefaultRouter()
products_router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('categories/', categories_view),
    path('users/', include(users_urls)),
    path('shopping_cart/', shopping_cart_view),
    path('auth/token/', include(authtoken_urls)),
    path('', include(products_router.urls)),
]
