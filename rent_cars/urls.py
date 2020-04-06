from django.urls import path

from rent_cars.views import HomeView, AutoView, FeedView, PostView

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('<int:id>/', AutoView.as_view(), name='auto_page'),
    path('feed/', FeedView.as_view(), name='feed_page'),
    path('feed/<int:id>/', PostView.as_view(), name='post_page')
]
