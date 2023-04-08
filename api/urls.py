from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from rest_framework import routers

from api.views import (CategoryListView, ProductViewSet, cart_view,
                       categories_view, token_login, token_logout,
                       users_create, users_me)

app_name = 'api'

# users_create = UserViewSet.as_view(
#    {'post': 'create',})
# users_me = UserViewSet.as_view(
#    {'get': 'me'})
# users_set_password = UserViewSet.as_view(
#    {'post': 'set_password'})
# users_reset_password = UserViewSet.as_view(
#    {'post': 'reset_password'})
# users_reset_password_confirm = UserViewSet.as_view(
#    {'post': 'reset_password_confirm'})

users_urls = [
    path('', users_create),
    path('me/', users_me),
#    path('set_password/', users_set_password),
#    path('reset_password/', users_reset_password),
#    path('reset_password_confirm/', users_reset_password_confirm),
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
    path('my_cart/', cart_view),
    path('auth/token/', include(authtoken_urls)),
    path('', include(products_router.urls)),
#    path('auth/verify/<str:uid>/<str:token>/', UserActivationView.as_view()),
]
