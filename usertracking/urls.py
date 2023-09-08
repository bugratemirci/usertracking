from django.contrib import admin
from django.urls import path, include
from user_core import urls as users
from config import urls as configs
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="USERTRACKING API",
        default_version='v1',
        description="USERTRACKING API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="bugrahanetemircii@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(users)),
    path('', include(configs)),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc')

]
