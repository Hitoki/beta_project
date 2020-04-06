from django.urls import path

from insane_app import views

app_name = 'insane'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='stories'),
    path('<int:pk>/', views.StoryDetailView.as_view(), name='story'),
    path('market/', views.ProductListView.as_view(), name='market'),
    path('market/<int:pk>/', views.ProductDetailView.as_view(), name='product'),

    # path('', views.StoryListView.as_view(), name='stories'),
]
