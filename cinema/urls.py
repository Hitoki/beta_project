from django.urls import path

from .views import ProductListView, ProductDetailView, \
    NewsListView, NewsDetailView, FilmDetailView, CinemaPersonDetailView
from .apps import CinemaConfig

app_name = CinemaConfig.name

urlpatterns = [
    path('blu-ray/', ProductListView.as_view(), name='product-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('blu-ray/<int:pk>/', ProductDetailView.as_view(),
         name='product-detail'),
    path('film/<int:pk>/', FilmDetailView.as_view(),
         name='film-detail'),
    path('movie-person/<int:pk>/', CinemaPersonDetailView.as_view(),
         name='movie-person-detail'),
    path('news/<int:pk>/', NewsDetailView.as_view(),
         name='news-detail'),
]
