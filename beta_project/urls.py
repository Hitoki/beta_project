"""
beta_project URL Configuration.
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cinema/', include('cinema.urls')),
    path('admin/', admin.site.urls),
    path('insane/', include('insane_app.urls')),
    path('rent-cars/', include('rent_cars.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
]
