# temp filler from django tutorial
from django.urls import path

from . import views

urlpatterns = [
    path('', views.map, name='map'),
    path('<int:supply_id>/summary', views.summary, name='summary'),
    path('<int:supply_id>/details', views.details, name='details'),
]






