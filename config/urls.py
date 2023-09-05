from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.ConfigValuesViewset import ConfigValuesViewset

router = DefaultRouter()
router.register(r'configs', ConfigValuesViewset)

urlpatterns = [
    path('', include(router.urls)),
]
