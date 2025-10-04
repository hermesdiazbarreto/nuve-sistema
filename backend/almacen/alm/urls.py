from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, MarcaViewSet, TallaViewSet, ColorViewSet,
    ProductoViewSet, ProductoVarianteViewSet, ClienteViewSet,
    VentaViewSet, DetalleVentaViewSet, MovimientoInventarioViewSet,
    ProveedorViewSet, login_view, logout_view
)

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Nuve API is running'})

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'tallas', TallaViewSet)
router.register(r'colores', ColorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'producto-variantes', ProductoVarianteViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalle-ventas', DetalleVentaViewSet)
router.register(r'movimientos', MovimientoInventarioViewSet)
router.register(r'proveedores', ProveedorViewSet)

urlpatterns = [
    path('', health_check, name='health'),
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
]











