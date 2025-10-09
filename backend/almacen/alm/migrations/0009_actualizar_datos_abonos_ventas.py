# Generated manually to fix existing sales data
from django.db import migrations


def actualizar_abonos_ventas(apps, schema_editor):
    """
    Actualiza las ventas existentes con los valores correctos de monto_abonado y saldo_pendiente
    basándose en su estado actual.
    """
    Venta = apps.get_model('alm', 'Venta')

    ventas_actualizadas = 0

    for venta in Venta.objects.all():
        actualizar = False

        # Si la venta está PAGADA o CANCELADA, el monto abonado debe ser el total
        if venta.estado in ['PAGADO', 'CANCELADO']:
            if venta.monto_abonado == 0 or venta.saldo_pendiente != 0:
                venta.monto_abonado = venta.total
                venta.saldo_pendiente = 0
                actualizar = True

        # Si está PENDIENTE y monto_abonado es 0, el saldo pendiente debe ser el total
        elif venta.estado == 'PENDIENTE':
            if venta.monto_abonado == 0 and venta.saldo_pendiente == 0:
                venta.saldo_pendiente = venta.total
                actualizar = True

        # Si está en ABONO, validar que los cálculos sean correctos
        elif venta.estado == 'ABONO':
            if venta.saldo_pendiente != (venta.total - venta.monto_abonado):
                venta.saldo_pendiente = venta.total - venta.monto_abonado
                actualizar = True

        if actualizar:
            venta.save()
            ventas_actualizadas += 1

    print(f"Migración de datos completada. Ventas actualizadas: {ventas_actualizadas}")


def reversar_actualizacion(apps, schema_editor):
    """
    No se puede revertir esta migración de datos ya que no sabemos
    cuáles eran los valores originales incorrectos.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('alm', '0008_venta_monto_abonado_venta_saldo_pendiente_and_more'),
    ]

    operations = [
        migrations.RunPython(actualizar_abonos_ventas, reversar_actualizacion),
    ]
