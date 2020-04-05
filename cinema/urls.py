from django.urls import path

from .views import CinemaTemplateView, ProductDetailTemplateView, \
    NewsListTemplateView, NewsDetailTemplateView
from .apps import CinemaConfig

app_name = CinemaConfig.name

urlpatterns = [
    path('', CinemaTemplateView.as_view(), name='index'),
    path('<int:pk>/', ProductDetailTemplateView.as_view(),
         name='product-detail'),
    path('news/', NewsListTemplateView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsDetailTemplateView.as_view(),
         name='news-detail'),
]
