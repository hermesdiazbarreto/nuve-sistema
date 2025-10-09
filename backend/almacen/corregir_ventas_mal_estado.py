#!/usr/bin/env python
"""
Script para corregir ventas que fueron marcadas incorrectamente como ABONO
cuando en realidad están completamente pagadas.

Problema: Ventas con descuento se registraron con monto_abonado = total,
lo que las marcó como ABONO en lugar de PAGADO.

Solución: Buscar ventas con estado ABONO donde monto_abonado >= total
y marcarlas como PAGADO con saldo_pendiente = 0.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almacen.settings')
django.setup()

from alm.models import Venta
from decimal import Decimal

def corregir_ventas():
    """Corrige las ventas que tienen estado incorrecto"""

    # Buscar ventas con estado ABONO donde el monto abonado >= total
    ventas_problematicas = Venta.objects.filter(estado='ABONO')

    corregidas = 0
    print(f"\n{'='*60}")
    print("BUSCANDO VENTAS CON ESTADO INCORRECTO")
    print(f"{'='*60}\n")

    for venta in ventas_problematicas:
        # Si el monto abonado es >= al total, debería estar PAGADO
        if venta.monto_abonado >= venta.total:
            print(f"Venta: {venta.numero_venta}")
            print(f"  Estado actual: {venta.estado}")
            print(f"  Total: {venta.total}")
            print(f"  Monto abonado: {venta.monto_abonado}")
            print(f"  Saldo pendiente: {venta.saldo_pendiente}")
            print(f"  Descuento: {venta.descuento}")

            # Corregir el estado
            venta.estado = 'PAGADO'
            venta.monto_abonado = venta.total
            venta.saldo_pendiente = Decimal('0.00')
            venta.save()

            print(f"  ✅ CORREGIDA → Estado: PAGADO, Saldo pendiente: 0.00\n")
            corregidas += 1

    print(f"{'='*60}")
    print(f"TOTAL DE VENTAS CORREGIDAS: {corregidas}")
    print(f"{'='*60}\n")

    # Mostrar también las ventas ABONO que realmente son abonos (para verificar)
    ventas_abono_reales = Venta.objects.filter(
        estado='ABONO',
        monto_abonado__gt=0,
        monto_abonado__lt=models.F('total')
    )

    if ventas_abono_reales.exists():
        print("\n📋 VENTAS CON ABONO REAL (no se modificaron):")
        print(f"{'='*60}")
        for venta in ventas_abono_reales:
            print(f"Venta: {venta.numero_venta}")
            print(f"  Total: {venta.total}")
            print(f"  Monto abonado: {venta.monto_abonado}")
            print(f"  Saldo pendiente: {venta.saldo_pendiente}\n")

if __name__ == '__main__':
    corregir_ventas()
