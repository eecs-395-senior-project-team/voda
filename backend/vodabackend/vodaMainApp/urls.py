# temp filler from django tutorial
from django.urls import path

from . import views

urlpatterns = [
    path('map', views.map, name='map'),
    path('summary', views.summary, name='summary'),
    path('details', views.details, name='details'),
]
