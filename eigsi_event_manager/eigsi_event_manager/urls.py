from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import index


urlpatterns = [
    path('', index, name='index'),  # Page d'accueil
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),  # Inclure les URLs du dashboard
    path('__reload__/', include('django_browser_reload.urls')),  # Rechargement automatique
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
