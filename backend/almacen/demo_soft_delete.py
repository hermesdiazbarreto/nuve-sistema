"""
Script de demostración del soft delete en Productos

Para ejecutar:
cd C:\Users\Tom\Documents\Django
venv\Scripts\activate
cd proyecto01\backend\almacen
python manage.py shell < demo_soft_delete.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almacen.settings')
django.setup()

from django.contrib.auth.models import User
from alm.models import Producto, Categoria, Marca

print("\n" + "="*60)
print("DEMOSTRACIÓN DE SOFT DELETE - PRODUCTOS")
print("="*60 + "\n")

# 1. Crear datos de prueba si no existen
print("1. Creando datos de prueba...")
categoria, _ = Categoria.objects.get_or_create(nombre="Demo Categoria")
marca, _ = Marca.objects.get_or_create(nombre="Demo Marca")
user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})

# Limpiar productos de demo anteriores
Producto.all_objects.filter(codigo__startswith="DEMO").delete()

# Crear productos de prueba
productos = []
for i in range(1, 4):
    producto = Producto.objects.create(
        codigo=f"DEMO{i:03d}",
        nombre=f"Producto Demo {i}",
        categoria=categoria,
        marca=marca,
        precio_compra=10.00 * i,
        precio_venta=20.00 * i
    )
    productos.append(producto)
    print(f"   ✓ Creado: {producto}")

print(f"\n   Total productos activos: {Producto.objects.count()}")
print(f"   Total productos (incluye eliminados): {Producto.all_objects.count()}\n")

# 2. Eliminar un producto (soft delete)
print("2. Eliminando producto DEMO001 (soft delete)...")
producto_a_eliminar = productos[0]
producto_a_eliminar.soft_delete(user=user)
print(f"   ✓ Producto eliminado")
print(f"   - is_deleted: {producto_a_eliminar.is_deleted}")
print(f"   - deleted_at: {producto_a_eliminar.deleted_at}")
print(f"   - deleted_by: {producto_a_eliminar.deleted_by.username}")

print(f"\n   Total productos activos: {Producto.objects.count()}")
print(f"   Total productos (incluye eliminados): {Producto.all_objects.count()}\n")

# 3. Listar productos activos
print("3. Productos activos (usando Producto.objects):")
for producto in Producto.objects.all():
    print(f"   - {producto.codigo}: {producto.nombre}")

# 4. Listar productos eliminados
print("\n4. Productos eliminados:")
for producto in Producto.all_objects.filter(is_deleted=True):
    print(f"   - {producto.codigo}: {producto.nombre} (eliminado el {producto.deleted_at})")

# 5. Restaurar producto
print("\n5. Restaurando producto DEMO001...")
producto_a_eliminar.restore()
print(f"   ✓ Producto restaurado")
print(f"   - is_deleted: {producto_a_eliminar.is_deleted}")
print(f"   - activo: {producto_a_eliminar.activo}")

print(f"\n   Total productos activos: {Producto.objects.count()}")
print(f"   Total productos (incluye eliminados): {Producto.all_objects.count()}\n")

# 6. Listar todos los productos después de restaurar
print("6. Productos activos después de restaurar:")
for producto in Producto.objects.all():
    print(f"   - {producto.codigo}: {producto.nombre}")

print("\n" + "="*60)
print("DEMOSTRACIÓN COMPLETADA")
print("="*60 + "\n")

print("Endpoints API disponibles:")
print("  - DELETE /api/productos/{id}/         → Eliminar (soft delete)")
print("  - POST   /api/productos/{id}/restaurar/ → Restaurar")
print("  - GET    /api/productos/               → Solo activos")
print("  - GET    /api/productos/?solo_eliminados=true → Solo eliminados")
print("  - GET    /api/productos/?incluir_eliminados=true → Todos")
print()