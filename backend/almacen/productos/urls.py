from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # Template HTML - página web
    path('', views.lista_productos, name='lista_productos'),
    
    # API endpoints - respuestas JSON
    path('api/', views.api_productos, name='api_productos'),
    path('api/<int:producto_id>/', views.api_producto_detalle, name='api_producto_detalle'),
    path('categorias/', views.api_categorias, name='api_categorias'),
]