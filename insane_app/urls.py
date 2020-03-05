from django.urls import path
from insane_app import views


app_name = 'insane_app'

urlpatterns = [
    path('', views.index, name='index'),
]
