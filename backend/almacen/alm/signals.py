from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DetalleVenta, MovimientoInventario, ProductoVariante


@receiver(post_save, sender=DetalleVenta)
def actualizar_inventario_venta(sender, instance, created, **kwargs):
    """
    Signal que se ejecuta al crear un DetalleVenta.
    Actualiza el stock de la variante y registra el movimiento de inventario.
    """
    if created:
        variante = instance.producto_variante

        # Guardar el stock anterior
        stock_anterior = variante.stock_actual

        # Actualizar el stock
        variante.stock_actual -= instance.cantidad
        variante.save()

        # Crear movimiento de inventario
        # Obtener el vendedor de la venta
        vendedor = instance.venta.vendedor

        MovimientoInventario.objects.create(
            producto_variante=variante,
            tipo_movimiento='SALIDA',
            cantidad=instance.cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=variante.stock_actual,
            motivo=f'Venta {instance.venta.numero_venta}',
            usuario=vendedor,
            venta=instance.venta
        )
