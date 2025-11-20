#!/usr/bin/env python
"""
Script para crear categorías de gasto iniciales
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almacen.settings')
django.setup()

from alm.models import CategoriaGasto

def crear_categorias_gasto():
    categorias = [
        'GASTOS DE PERSONAL',
        'HONORARIO',
        'IMPUESTOS',
        'ARRENDAMIENTOS',
        'CONTRIBUCIONES Y AFILIACIONES',
        'SEGUROS',
        'SERVICIOS',
        'GASTOS LEGALES',
        'MANTENIMIENTO Y REPARACIONES',
        'ADECUACION E INSTALACION',
        'GASTOS DE VIAJE',
        'OTRO'
    ]

    print("Creando categorías de gasto...")
    creadas = 0
    existentes = 0

    for nombre in categorias:
        categoria, created = CategoriaGasto.objects.get_or_create(
            nombre=nombre,
            defaults={'activo': True}
        )
        if created:
            print(f"+ Creada: {nombre}")
            creadas += 1
        else:
            print(f"  Ya existe: {nombre}")
            existentes += 1

    print(f"\n=== Resumen ===")
    print(f"Categorías creadas: {creadas}")
    print(f"Categorías existentes: {existentes}")
    print(f"Total: {len(categorias)}")

if __name__ == '__main__':
    crear_categorias_gasto()
