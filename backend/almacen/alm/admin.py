from django.contrib import admin
from .models import (
    Categoria, Marca, Talla, Color, Producto, ProductoVariante,
    Cliente, Venta, DetalleVenta, MovimientoInventario, Proveedor
)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    search_fields = ['nombre']

@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden']
    list_editable = ['orden']
    ordering = ['orden']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_hex']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'marca', 'precio_venta', 'activo']
    list_filter = ['categoria', 'marca', 'activo']
    search_fields = ['codigo', 'nombre']

@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    list_display = ['codigo_variante', 'producto', 'talla', 'color', 'stock_actual', 'stock_minimo', 'activo']
    list_filter = ['producto__categoria', 'talla', 'color', 'activo']
    search_fields = ['codigo_variante', 'producto__nombre']
    list_editable = ['stock_actual']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre_completo', 'numero_documento', 'email', 'telefono', 'activo']
    list_filter = ['activo', 'tipo_documento']
    search_fields = ['nombres', 'apellidos', 'numero_documento', 'email']

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['numero_venta', 'cliente', 'vendedor', 'total', 'estado', 'fecha_venta']
    list_filter = ['estado', 'tipo_pago', 'fecha_venta']
    search_fields = ['numero_venta', 'cliente__nombres', 'cliente__apellidos']
    inlines = [DetalleVentaInline]
    readonly_fields = ['numero_venta', 'subtotal', 'total']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['venta', 'producto_variante', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['venta__fecha_venta']

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['producto_variante', 'tipo_movimiento', 'cantidad', 'stock_anterior', 'stock_nuevo', 'fecha_movimiento']
    list_filter = ['tipo_movimiento', 'fecha_movimiento']
    search_fields = ['producto_variante__producto__nombre']
    readonly_fields = ['stock_anterior', 'stock_nuevo', 'fecha_movimiento']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'ruc', 'telefono', 'email', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre', 'ruc']