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
    Cliente, Venta, DetalleVenta, MovimientoInventario, Proveedor,
    DetalleCompra, PagoVenta
)
from .serializers import (
    CategoriaSerializer, MarcaSerializer, TallaSerializer, ColorSerializer,
    ProductoSerializer, ProductoVarianteSerializer, ClienteSerializer,
    VentaSerializer, DetalleVentaSerializer, MovimientoInventarioSerializer,
    ProveedorSerializer, PagoVentaSerializer
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
    queryset = Producto.objects.all()  # Usa el manager por defecto que excluye eliminados
    serializer_class = ProductoSerializer

    def get_queryset(self):
        """
        Permite filtrar productos por diferentes estados:
        - Por defecto: solo productos no eliminados
        - ?incluir_inactivos=true: incluye inactivos pero no eliminados
        - ?incluir_eliminados=true: incluye productos eliminados
        - ?solo_eliminados=true: solo productos eliminados
        """
        incluir_inactivos = self.request.query_params.get('incluir_inactivos', 'false').lower()
        incluir_eliminados = self.request.query_params.get('incluir_eliminados', 'false').lower()
        solo_eliminados = self.request.query_params.get('solo_eliminados', 'false').lower()

        if solo_eliminados == 'true':
            # Mostrar solo productos eliminados
            queryset = Producto.all_objects.filter(is_deleted=True)
        elif incluir_eliminados == 'true':
            # Incluir todos los productos (eliminados y no eliminados)
            queryset = Producto.all_objects.all()
        else:
            # Por defecto: solo productos no eliminados
            queryset = Producto.objects.all()

        # Filtrar por activo/inactivo solo si no están viendo eliminados
        if incluir_inactivos != 'true' and solo_eliminados != 'true':
            queryset = queryset.filter(activo=True)

        return queryset

    def destroy(self, request, *args, **kwargs):
        """
        Soft Delete - Marcar producto como eliminado sin borrarlo físicamente
        Esto preserva el histórico de ventas y compras
        """
        from django.db import transaction

        instance = self.get_object()

        try:
            with transaction.atomic():
                # Realizar soft delete usando el método del modelo
                instance.soft_delete(user=request.user if request.user.is_authenticated else None)

            return Response(
                {
                    'message': 'Producto eliminado correctamente. '
                              'El producto ya no aparecerá en los listados pero su historial se mantiene.',
                    'deleted_at': instance.deleted_at
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERROR AL ELIMINAR PRODUCTO: {error_traceback}")

            return Response(
                {'error': f'Error al eliminar producto: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def restaurar(self, request, pk=None):
        """
        Restaurar un producto eliminado
        """
        from django.db import transaction

        # Obtener el producto usando all_objects para incluir eliminados
        producto = Producto.all_objects.get(pk=pk)

        if not producto.is_deleted:
            return Response(
                {'error': 'Este producto no está eliminado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Restaurar usando el método del modelo
                producto.restore()

            return Response(
                {
                    'message': 'Producto restaurado correctamente.',
                    'producto': ProductoSerializer(producto).data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERROR AL RESTAURAR PRODUCTO: {error_traceback}")

            return Response(
                {'error': f'Error al restaurar producto: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """
        Activar un producto desactivado
        """
        from django.db import transaction

        producto = self.get_object()

        try:
            with transaction.atomic():
                producto.activo = True
                producto.save()

                # También activar todas sus variantes
                producto.variantes.update(activo=True)

            return Response(
                {'message': 'Producto activado correctamente.'},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERROR AL ACTIVAR PRODUCTO: {error_traceback}")

            return Response(
                {'error': f'Error al activar producto: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductoVarianteViewSet(viewsets.ModelViewSet):
    queryset = ProductoVariante.objects.filter(activo=True, producto__activo=True)  # Solo variantes activas de productos activos
    serializer_class = ProductoVarianteSerializer

    def get_queryset(self):
        """
        Opcionalmente permite ver variantes inactivas con ?incluir_inactivos=true
        """
        queryset = ProductoVariante.objects.all()
        incluir_inactivos = self.request.query_params.get('incluir_inactivos', 'false').lower()

        if incluir_inactivos != 'true':
            queryset = queryset.filter(activo=True, producto__activo=True)

        return queryset

    @action(detail=True, methods=['post'])
    def duplicar(self, request, pk=None):
        """
        Duplicar una variante de producto. Útil para crear variantes similares
        modificando solo talla o color.

        Body params opcionales:
        - talla: ID de la nueva talla (si no se proporciona, usa la misma)
        - color: ID del nuevo color (si no se proporciona, usa el mismo)
        - stock_actual: Stock inicial (default: 0)
        - stock_minimo: Stock mínimo (si no se proporciona, usa el mismo que el original)
        """
        from django.db import transaction

        variante_original = self.get_object()

        # Obtener los datos del request
        talla_id = request.data.get('talla', variante_original.talla.id)
        color_id = request.data.get('color', variante_original.color.id)
        stock_actual = request.data.get('stock_actual', 0)
        stock_minimo = request.data.get('stock_minimo', variante_original.stock_minimo)

        try:
            with transaction.atomic():
                # Verificar si ya existe esta combinación
                if ProductoVariante.objects.filter(
                    producto=variante_original.producto,
                    talla_id=talla_id,
                    color_id=color_id
                ).exists():
                    return Response(
                        {'error': 'Ya existe una variante con esta combinación de talla y color'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Obtener los objetos de talla y color
                talla = Talla.objects.get(id=talla_id)
                color = Color.objects.get(id=color_id)

                # Generar código de variante
                codigo_variante = f"{variante_original.producto.codigo}-{talla.nombre}-{color.nombre}"

                # Crear la nueva variante
                nueva_variante = ProductoVariante.objects.create(
                    producto=variante_original.producto,
                    talla=talla,
                    color=color,
                    codigo_variante=codigo_variante,
                    stock_actual=stock_actual,
                    stock_minimo=stock_minimo,
                    activo=True
                )

            return Response(
                {
                    'message': 'Variante duplicada exitosamente',
                    'variante': ProductoVarianteSerializer(nueva_variante).data
                },
                status=status.HTTP_201_CREATED
            )

        except Talla.DoesNotExist:
            return Response(
                {'error': 'La talla especificada no existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Color.DoesNotExist:
            return Response(
                {'error': 'El color especificado no existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERROR AL DUPLICAR VARIANTE: {error_traceback}")

            return Response(
                {'error': f'Error al duplicar variante: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
                        stock_anterior = variante.stock_actual
                        variante.stock_actual += detalle.cantidad
                        variante.save()

                        # Crear movimiento de inventario de ENTRADA (reversión)
                        MovimientoInventario.objects.create(
                            producto_variante=variante,
                            tipo_movimiento='ENTRADA',
                            cantidad=detalle.cantidad,
                            stock_anterior=stock_anterior,
                            stock_nuevo=variante.stock_actual,
                            motivo=f'Cancelación de venta {venta.numero_venta}',
                            usuario=request.user
                        )

            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Error al actualizar venta: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def registrar_pago(self, request, pk=None):
        """
        Registrar un pago/abono a una venta.

        Body params:
        - monto: Monto del pago (requerido)
        - tipo_pago: Tipo de pago (EFECTIVO, TARJETA, TRANSFERENCIA, MIXTO) (requerido)
        - observaciones: Observaciones del pago (opcional)
        """
        from django.db import transaction
        from decimal import Decimal

        venta = self.get_object()

        # Validar que la venta no esté cancelada
        if venta.estado == 'CANCELADO':
            return Response(
                {'error': 'No se pueden registrar pagos en ventas canceladas'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que la venta no esté completamente pagada
        if venta.estado == 'PAGADO':
            return Response(
                {'error': 'Esta venta ya está completamente pagada'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener datos del request
        monto = request.data.get('monto')
        tipo_pago = request.data.get('tipo_pago')
        observaciones = request.data.get('observaciones', '')

        # Validaciones
        if not monto:
            return Response(
                {'error': 'El monto es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            monto = Decimal(str(monto))
        except:
            return Response(
                {'error': 'El monto debe ser un número válido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if monto <= 0:
            return Response(
                {'error': 'El monto debe ser mayor a 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not tipo_pago:
            return Response(
                {'error': 'El tipo de pago es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar que el monto no exceda el saldo pendiente
        if monto > venta.saldo_pendiente:
            return Response(
                {'error': f'El monto excede el saldo pendiente (${venta.saldo_pendiente})'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Crear el registro de pago
                pago = PagoVenta.objects.create(
                    venta=venta,
                    monto=monto,
                    tipo_pago=tipo_pago,
                    usuario=request.user,
                    observaciones=observaciones
                )

                # Actualizar monto abonado en la venta
                venta.monto_abonado += monto
                venta.save()  # El método save() de Venta actualizará automáticamente el estado y saldo_pendiente

            # Retornar la venta actualizada con el pago
            venta_actualizada = Venta.objects.get(id=venta.id)
            return Response(
                {
                    'message': 'Pago registrado exitosamente',
                    'pago': PagoVentaSerializer(pago).data,
                    'venta': VentaSerializer(venta_actualizada).data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERROR AL REGISTRAR PAGO: {error_traceback}")

            return Response(
                {'error': f'Error al registrar pago: {str(e)}'},
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
                        stock_anterior = variante.stock_actual
                        variante.stock_actual += detalle.cantidad
                        variante.save()

                        # Crear movimiento de inventario de ENTRADA (reversión)
                        MovimientoInventario.objects.create(
                            producto_variante=variante,
                            tipo_movimiento='ENTRADA',
                            cantidad=detalle.cantidad,
                            stock_anterior=stock_anterior,
                            stock_nuevo=variante.stock_actual,
                            motivo=f'Eliminación de venta {instance.numero_venta}',
                            usuario=request.user
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
