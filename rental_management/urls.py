from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingCreatView,
    BuildingListView,
    LeaseContractCreatView,
    UnitCreateView,
    UnitListView,
)

router = DefaultRouter()


urlpatterns = [
    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('buildings/create/', BuildingCreatView.as_view(), name='building-create'),
    path('units/', UnitListView.as_view(), name='unit-list'),
    path('units/create/', UnitCreateView.as_view(), name='unit-create'),
    path('contracts/create/', LeaseContractCreatView.as_view(), name='contract-create'),
    
    path('api/', include(router.urls)),
]
