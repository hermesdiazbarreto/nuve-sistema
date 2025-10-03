from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, MarcaViewSet, TallaViewSet, ColorViewSet,
    ProductoViewSet, ProductoVarianteViewSet, ClienteViewSet,
    VentaViewSet, DetalleVentaViewSet, MovimientoInventarioViewSet,
    ProveedorViewSet, login_view, logout_view
)

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
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_view, name='logout'),
]
