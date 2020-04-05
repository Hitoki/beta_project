"""
beta_project URL Configuration.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('cinema/', include('cinema.urls')),
    path('admin/', admin.site.urls),
    path('insane/', include('insane_app.urls')),
]
