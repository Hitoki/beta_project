from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from insane_app import views

app_name = 'insane'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='stories'),
    path('login/', auth_views.LoginView.as_view(template_name='insane_accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.StoryDetailView.as_view(), name='story'),
    path('<int:pk>/like/', views.like_story, name='like_story'),
    path('market/', views.ProductListView.as_view(), name='market'),
    path('market/<int:pk>/', views.ProductDetailView.as_view(), name='product'),

    # path('', views.StoryListView.as_view(), name='stories'),
]
