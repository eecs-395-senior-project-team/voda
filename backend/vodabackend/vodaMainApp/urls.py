# temp filler from django tutorial
from django.urls import path

from . import views
"""
Parses http requests and sends it to the right view depending on the endpoint
"""
urlpatterns = [
    path('map', views.map, name='map'),
    path('summary', views.summary, name='summary'),
    path('details', views.details, name='details'),
]
