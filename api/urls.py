from django.urls import path
from rest_framework import routers

from api.views import CategoryList, ProductList

app_name = 'api'

products_router = routers.DefaultRouter()

urlpatterns = [
    path('categories/', CategoryList.as_view()),
    path('products/', ProductList.as_view()),
]
