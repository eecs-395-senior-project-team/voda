# temp filler from django tutorial
from django.urls import path

from . import views


"""
Parses http requests and sends it to the right view depending on the endpoint
"""
urlpatterns = [
    path('', views.root, name='root'),
    path('debug', views.debug, name='debug'),
    path('map', views.map_endpoint, name='map'),
    path('summary', views.summary, name='summary'),
    path('details', views.details, name='details'),
]
