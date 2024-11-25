from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuildingViewSet
from . import views

router = DefaultRouter()
router.register('buildings', BuildingViewSet, basename='buildings')

urlpatterns = [
    path('api/', include(router.urls)),
]