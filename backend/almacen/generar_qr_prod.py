#!/usr/bin/env python
"""Script para generar QR codes en producción"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almacen.settings')
django.setup()

from alm.models import ProductoVariante

print('=== GENERANDO QR CODES EN PRODUCCIÓN ===\n')

# Obtener todas las variantes
variantes = ProductoVariante.objects.all()
total = variantes.count()
sin_qr = variantes.filter(qr_code='').count()

print(f'Total de variantes: {total}')
print(f'Variantes sin QR: {sin_qr}')
print(f'Variantes con QR: {total - sin_qr}\n')

if sin_qr == 0:
    print('✓ Todas las variantes ya tienen QR codes!')
else:
    print(f'Generando {sin_qr} códigos QR...\n')

    contador = 0
    errores = 0

    for variante in variantes.filter(qr_code=''):
        try:
            variante.generar_qr()
            variante.save()
            contador += 1
            print(f'[OK] {variante.codigo_variante}')
        except Exception as e:
            errores += 1
            print(f'[ERROR] {variante.codigo_variante}: {str(e)}')

    print(f'\n=== RESULTADO ===')
    print(f'QR generados: {contador}')
    print(f'Errores: {errores}')
    print(f'Total con QR ahora: {ProductoVariante.objects.exclude(qr_code="").count()}')
