from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entidades', views.entidades, name='entidades')
]