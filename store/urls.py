from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Store API",
        default_version='v1',
        description="Документация для проекта Store",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('for_staff_only/', admin.site.urls),
    re_path(r'^chaining/', include('smart_selects.urls')),
    path('api/', include('api.urls')),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
