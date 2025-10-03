from rest_framework import serializers
from .models import (
    Categoria, Marca, Talla, Color, Producto, ProductoVariante,
    Cliente, Venta, DetalleVenta, MovimientoInventario, Proveedor
)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class TallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talla
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'

class ProductoVarianteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    talla_nombre = serializers.CharField(source='talla.nombre', read_only=True)
    color_nombre = serializers.CharField(source='color.nombre', read_only=True)
    
    class Meta:
        model = ProductoVariante
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Cliente
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_info = serializers.CharField(source='producto_variante.__str__', read_only=True)
    
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField(read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.username', read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    numero_venta = serializers.CharField(read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'

    def get_cliente_nombre(self, obj):
        return obj.cliente.nombre_completo if obj.cliente else "Cliente General"

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto_info = serializers.CharField(source='producto_variante.__str__', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = MovimientoInventario
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'