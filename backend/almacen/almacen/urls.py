from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from productos.views import api_productos, api_categorias

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas API REST Framework (app alm - Sistema completo)
    path('', include('alm.urls')),

    # Rutas API directas (legacy - lo que espera el template JavaScript)
    path('api/productos/', api_productos, name='api_productos_directo'),
    path('api/categorias/', api_categorias, name='api_categorias_directo'),

    # Rutas de aplicaciones legacy
    path('productos/', include('productos.urls')),
    path('clientes/', include('clientes.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)