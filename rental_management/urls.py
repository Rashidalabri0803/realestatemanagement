from django.urls import path

from .views import building_list

urlpatterns = [
    path('buildings/', building_list, name='building_list'),
]