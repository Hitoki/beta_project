"""
beta_project URL Configuration.
"""

# from django.conf import settings
from django.contrib import admin
# from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('cinema/', include('cinema.urls')),
    path('admin/', admin.site.urls),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns