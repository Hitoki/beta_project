from django.urls import path

from . import views

urlpatterns = [
    path('film/', views.index, name='index'),
]
