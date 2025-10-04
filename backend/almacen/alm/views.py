from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db import models
from django.contrib.auth import authenticate
from .models import (
    Categoria, Marca, Talla, Color, Producto, ProductoVariante,
    Cliente, Venta, DetalleVenta, MovimientoInventario, Proveedor
)
from .serializers import (
    CategoriaSerializer, MarcaSerializer, TallaSerializer, ColorSerializer,
    ProductoSerializer, ProductoVarianteSerializer, ClienteSerializer,
    VentaSerializer, DetalleVentaSerializer, MovimientoInventarioSerializer,
    ProveedorSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class TallaViewSet(viewsets.ModelViewSet):
    queryset = Talla.objects.all()
    serializer_class = TallaSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoVarianteViewSet(viewsets.ModelViewSet):
    queryset = ProductoVariante.objects.all()
    serializer_class = ProductoVarianteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def create(self, request, *args, **kwargs):
        """
        Crear venta con sus detalles en una sola transacción.
        """
        from django.db import transaction

        data = request.data
        detalles_data = data.pop('detalles', [])

        with transaction.atomic():
            # Crear la venta
            venta_serializer = self.get_serializer(data=data)
            venta_serializer.is_valid(raise_exception=True)
            venta = venta_serializer.save()

            # Crear los detalles
            for detalle_data in detalles_data:
                detalle_data['venta'] = venta.id
                detalle_serializer = DetalleVentaSerializer(data=detalle_data)
                detalle_serializer.is_valid(raise_exception=True)
                detalle_serializer.save()

        # Retornar la venta completa con detalles
        venta_completa = Venta.objects.get(id=venta.id)
        return Response(
            VentaSerializer(venta_completa).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Actualizar venta - Al cambiar a CANCELADO, restaurar stock si es INGRESO
        """
        from django.db import transaction

        instance = self.get_object()
        estado_anterior = instance.estado

        # Actualizar la venta
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                venta = serializer.save()

                # Verificar si tiene el atributo tipo_movimiento (por compatibilidad)
                tipo_movimiento = getattr(venta, 'tipo_movimiento', 'INGRESO')

                # Si la venta cambió a CANCELADO y es un INGRESO, restaurar stock
                if (venta.estado == 'CANCELADO' and
                    estado_anterior != 'CANCELADO' and
                    tipo_movimiento == 'INGRESO'):

                    detalles = venta.detalles.all()

                    # Restaurar stock de cada detalle
                    for detalle in detalles:
                        variante = detalle.producto_variante
                        variante.stock_actual += detalle.cantidad
                        variante.save()

                        # Crear movimiento de inventario de ENTRADA (reversión)
                        MovimientoInventario.objects.create(
                            producto_variante=variante,
                            tipo_movimiento='ENTRADA',
                            cantidad=detalle.cantidad,
                            referencia=f'Cancelación de venta {venta.numero_venta}',
                            usuario=request.user if request.user.is_authenticated else None
                        )

            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar venta: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """
        Eliminar venta - Restaurar stock automáticamente si es INGRESO
        """
        from django.db import transaction
        import traceback

        instance = self.get_object()

        try:
            with transaction.atomic():
                # Verificar si tiene el atributo tipo_movimiento (por compatibilidad)
                tipo_movimiento = getattr(instance, 'tipo_movimiento', 'INGRESO')

                # Solo restaurar stock si es un INGRESO con productos y no está cancelado
                if tipo_movimiento == 'INGRESO' and instance.estado != 'CANCELADO':
                    detalles = instance.detalles.all()

                    for detalle in detalles:
                        variante = detalle.producto_variante
                        variante.stock_actual += detalle.cantidad
                        variante.save()

                        # Crear movimiento de inventario de ENTRADA (reversión)
                        MovimientoInventario.objects.create(
                            producto_variante=variante,
                            tipo_movimiento='ENTRADA',
                            cantidad=detalle.cantidad,
                            referencia=f'Eliminación de venta {instance.numero_venta}',
                            usuario=request.user if request.user.is_authenticated else None
                        )

                # Eliminar la venta (los detalles se eliminarán en cascada)
                instance.delete()

            return Response(
                {'message': 'Venta eliminada correctamente. Stock restaurado.'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            # Imprimir el traceback completo para debugging
            error_traceback = traceback.format_exc()
            print(f"ERROR AL ELIMINAR VENTA: {error_traceback}")

            return Response(
                {'error': f'Error al eliminar venta: {str(e)}', 'traceback': error_traceback},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class MovimientoInventarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

# Vistas de autenticación
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Por favor proporciona usuario y contraseña'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    else:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Sesión cerrada correctamente'})
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
