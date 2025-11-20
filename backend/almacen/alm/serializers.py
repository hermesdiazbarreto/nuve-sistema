from rest_framework import serializers
from .models import (
    Categoria, Marca, Talla, Color, Producto, ProductoVariante,
    Cliente, Venta, DetalleVenta, MovimientoInventario, Proveedor, PagoVenta,
    PromocionWhatsApp, EnvioWhatsApp
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
    deleted_by_username = serializers.CharField(source='deleted_by.username', read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ('is_deleted', 'deleted_at', 'deleted_by')

class ProductoVarianteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    talla_nombre = serializers.CharField(source='talla.nombre', read_only=True)
    color_nombre = serializers.CharField(source='color.nombre', read_only=True)
    codigo_variante = serializers.CharField(required=False, allow_blank=True)
    # Campos adicionales del producto para POS
    precio_venta = serializers.DecimalField(source='producto.precio_venta', max_digits=10, decimal_places=2, read_only=True)
    precio_compra = serializers.DecimalField(source='producto.precio_compra', max_digits=10, decimal_places=2, read_only=True)
    categoria_nombre = serializers.CharField(source='producto.categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='producto.marca.nombre', read_only=True)
    color_hex = serializers.CharField(source='color.codigo_hex', read_only=True)

    class Meta:
        model = ProductoVariante
        fields = '__all__'
        read_only_fields = ('id',)  # El ID se genera automáticamente, no debe enviarse desde el frontend

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

class PagoVentaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = PagoVenta
        fields = '__all__'
        read_only_fields = ('fecha_pago', 'usuario')

class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.SerializerMethodField(read_only=True)
    vendedor_nombre = serializers.CharField(source='vendedor.username', read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    pagos = PagoVentaSerializer(many=True, read_only=True)
    numero_venta = serializers.CharField(read_only=True)
    # monto_abonado y saldo_pendiente NO son read_only para permitir que el frontend los envíe
    # El modelo Venta.save() se encargará de calcular saldo_pendiente si es necesario

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

class EnvioWhatsAppSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)

    class Meta:
        model = EnvioWhatsApp
        fields = '__all__'
        read_only_fields = ('fecha_envio', 'mensaje_error', 'sid_twilio')

class PromocionWhatsAppSerializer(serializers.ModelSerializer):
    creado_por_nombre = serializers.CharField(source='creado_por.username', read_only=True)
    envios = EnvioWhatsAppSerializer(many=True, read_only=True)

    class Meta:
        model = PromocionWhatsApp
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_envio', 'total_destinatarios',
                           'mensajes_enviados', 'mensajes_fallidos', 'creado_por')
class CategoriaGastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaGasto
        fields = '__all__'
