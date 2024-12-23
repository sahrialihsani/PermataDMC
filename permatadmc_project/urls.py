# permatadmc_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', admin.site.urls),
    # URL internasional
    path('i18n/', include('django.conf.urls.i18n')),
] + i18n_patterns(
    path('', include('tourism.urls')),
    # URL lainnya
)
