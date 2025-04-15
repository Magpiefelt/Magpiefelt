"""
URL Configuration for magpie_crafts project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog
from django.apps import apps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    
    # Oscar URLs
    path('', include(apps.get_app_config('oscar').urls[0])),
    
    # Django AllAuth
    path('accounts/', include('allauth.urls')),
    
    # Blog URLs
    path('blog/', include('blog.urls')),
    
    # JavaScript translations
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
