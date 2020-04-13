from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from insane_app import views

app_name = 'insane'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='stories'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='insane_accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:pk>/', views.StoryDetailView.as_view(), name='story'),
    path('<int:pk>/like/', views.like_story, name='like_story'),
    path('create/', login_required(views.StoryCreateView.as_view()), name='create_story'),
    path('market/', views.ProductListView.as_view(), name='market'),
    path('market/<int:pk>/', views.ProductDetailView.as_view(), name='product'),
    path('market/create/', login_required(views.ProductCreateView.as_view()), name='create_product'),

    # path('', views.StoryListView.as_view(), name='stories'),
]
