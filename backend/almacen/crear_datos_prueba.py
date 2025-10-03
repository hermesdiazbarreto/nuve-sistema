"""
Script para crear datos de prueba en el sistema de almacén
Ejecutar con: python manage.py shell < crear_datos_prueba.py
"""

from alm.models import Categoria, Marca, Talla, Color, Producto, ProductoVariante, Cliente, Proveedor
from django.contrib.auth.models import User

print("🚀 Creando datos de prueba...")

# Crear usuario administrador si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Usuario admin creado (user: admin, pass: admin123)")
else:
    print("ℹ️  Usuario admin ya existe")

# ========== CATEGORÍAS ==========
print("\n📁 Creando Categorías...")
categorias_data = [
    {'nombre': 'Ropa', 'descripcion': 'Prendas de vestir', 'activo': True},
    {'nombre': 'Calzado', 'descripcion': 'Zapatos y zapatillas', 'activo': True},
    {'nombre': 'Accesorios', 'descripcion': 'Complementos y accesorios', 'activo': True},
    {'nombre': 'Deportivo', 'descripcion': 'Artículos deportivos', 'activo': True},
]

for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults=cat_data
    )
    if created:
        print(f"  ✅ Categoría: {categoria.nombre}")
    else:
        print(f"  ℹ️  Categoría ya existe: {categoria.nombre}")

# ========== MARCAS ==========
print("\n🏷️  Creando Marcas...")
marcas_data = [
    {'nombre': 'Nike', 'descripcion': 'Marca deportiva internacional', 'activo': True},
    {'nombre': 'Adidas', 'descripcion': 'Marca deportiva alemana', 'activo': True},
    {'nombre': 'Puma', 'descripcion': 'Marca deportiva', 'activo': True},
    {'nombre': 'Reebok', 'descripcion': 'Marca de ropa deportiva', 'activo': True},
    {'nombre': 'Under Armour', 'descripcion': 'Ropa y calzado deportivo', 'activo': True},
]

for marca_data in marcas_data:
    marca, created = Marca.objects.get_or_create(
        nombre=marca_data['nombre'],
        defaults=marca_data
    )
    if created:
        print(f"  ✅ Marca: {marca.nombre}")
    else:
        print(f"  ℹ️  Marca ya existe: {marca.nombre}")

# ========== TALLAS ==========
print("\n📏 Creando Tallas...")
tallas_data = [
    {'nombre': 'XS', 'orden': 0},
    {'nombre': 'S', 'orden': 1},
    {'nombre': 'M', 'orden': 2},
    {'nombre': 'L', 'orden': 3},
    {'nombre': 'XL', 'orden': 4},
    {'nombre': 'XXL', 'orden': 5},
]

for talla_data in tallas_data:
    talla, created = Talla.objects.get_or_create(
        nombre=talla_data['nombre'],
        defaults=talla_data
    )
    if created:
        print(f"  ✅ Talla: {talla.nombre}")
    else:
        print(f"  ℹ️  Talla ya existe: {talla.nombre}")

# ========== COLORES ==========
print("\n🎨 Creando Colores...")
colores_data = [
    {'nombre': 'Rojo', 'codigo_hex': '#FF0000'},
    {'nombre': 'Azul', 'codigo_hex': '#0000FF'},
    {'nombre': 'Negro', 'codigo_hex': '#000000'},
    {'nombre': 'Blanco', 'codigo_hex': '#FFFFFF'},
    {'nombre': 'Verde', 'codigo_hex': '#00FF00'},
    {'nombre': 'Amarillo', 'codigo_hex': '#FFFF00'},
    {'nombre': 'Gris', 'codigo_hex': '#808080'},
    {'nombre': 'Naranja', 'codigo_hex': '#FFA500'},
]

for color_data in colores_data:
    color, created = Color.objects.get_or_create(
        nombre=color_data['nombre'],
        defaults=color_data
    )
    if created:
        print(f"  ✅ Color: {color.nombre}")
    else:
        print(f"  ℹ️  Color ya existe: {color.nombre}")

# ========== PRODUCTOS ==========
print("\n📦 Creando Productos...")
productos_data = [
    {
        'codigo': 'PROD001',
        'nombre': 'Camiseta Deportiva',
        'descripcion': 'Camiseta de algodón para deporte',
        'categoria': 'Ropa',
        'marca': 'Nike',
        'precio_compra': 50.00,
        'precio_venta': 100.00,
    },
    {
        'codigo': 'PROD002',
        'nombre': 'Zapatillas Running',
        'descripcion': 'Zapatillas para correr con amortiguación',
        'categoria': 'Calzado',
        'marca': 'Adidas',
        'precio_compra': 150.00,
        'precio_venta': 299.99,
    },
    {
        'codigo': 'PROD003',
        'nombre': 'Pantalón Deportivo',
        'descripcion': 'Pantalón cómodo para entrenar',
        'categoria': 'Ropa',
        'marca': 'Puma',
        'precio_compra': 70.00,
        'precio_venta': 140.00,
    },
    {
        'codigo': 'PROD004',
        'nombre': 'Gorra Deportiva',
        'descripcion': 'Gorra ajustable con logo',
        'categoria': 'Accesorios',
        'marca': 'Nike',
        'precio_compra': 25.00,
        'precio_venta': 50.00,
    },
    {
        'codigo': 'PROD005',
        'nombre': 'Sudadera con Capucha',
        'descripcion': 'Sudadera cómoda y abrigada',
        'categoria': 'Ropa',
        'marca': 'Reebok',
        'precio_compra': 80.00,
        'precio_venta': 160.00,
    },
]

for prod_data in productos_data:
    categoria = Categoria.objects.get(nombre=prod_data['categoria'])
    marca = Marca.objects.get(nombre=prod_data['marca'])

    producto, created = Producto.objects.get_or_create(
        codigo=prod_data['codigo'],
        defaults={
            'nombre': prod_data['nombre'],
            'descripcion': prod_data['descripcion'],
            'categoria': categoria,
            'marca': marca,
            'precio_compra': prod_data['precio_compra'],
            'precio_venta': prod_data['precio_venta'],
            'activo': True,
        }
    )
    if created:
        print(f"  ✅ Producto: {producto.nombre}")
    else:
        print(f"  ℹ️  Producto ya existe: {producto.nombre}")

# ========== VARIANTES DE PRODUCTOS ==========
print("\n🔢 Creando Variantes de Productos...")

# Obtener objetos necesarios
talla_m = Talla.objects.get(nombre='M')
talla_l = Talla.objects.get(nombre='L')
talla_xl = Talla.objects.get(nombre='XL')

color_rojo = Color.objects.get(nombre='Rojo')
color_azul = Color.objects.get(nombre='Azul')
color_negro = Color.objects.get(nombre='Negro')
color_blanco = Color.objects.get(nombre='Blanco')

variantes_data = [
    # Camiseta Deportiva
    {'producto': 'PROD001', 'talla': talla_m, 'color': color_rojo, 'stock': 50, 'stock_min': 10},
    {'producto': 'PROD001', 'talla': talla_m, 'color': color_azul, 'stock': 45, 'stock_min': 10},
    {'producto': 'PROD001', 'talla': talla_l, 'color': color_negro, 'stock': 30, 'stock_min': 10},
    {'producto': 'PROD001', 'talla': talla_l, 'color': color_blanco, 'stock': 25, 'stock_min': 10},
    {'producto': 'PROD001', 'talla': talla_xl, 'color': color_negro, 'stock': 5, 'stock_min': 10},  # Stock bajo!

    # Zapatillas Running
    {'producto': 'PROD002', 'talla': talla_m, 'color': color_negro, 'stock': 20, 'stock_min': 5},
    {'producto': 'PROD002', 'talla': talla_l, 'color': color_azul, 'stock': 15, 'stock_min': 5},
    {'producto': 'PROD002', 'talla': talla_xl, 'color': color_blanco, 'stock': 3, 'stock_min': 5},  # Stock bajo!

    # Pantalón Deportivo
    {'producto': 'PROD003', 'talla': talla_m, 'color': color_negro, 'stock': 40, 'stock_min': 8},
    {'producto': 'PROD003', 'talla': talla_l, 'color': color_azul, 'stock': 35, 'stock_min': 8},

    # Sudadera
    {'producto': 'PROD005', 'talla': talla_m, 'color': color_negro, 'stock': 25, 'stock_min': 5},
    {'producto': 'PROD005', 'talla': talla_l, 'color': color_azul, 'stock': 2, 'stock_min': 5},  # Stock bajo!
]

for var_data in variantes_data:
    producto = Producto.objects.get(codigo=var_data['producto'])
    codigo_variante = f"{producto.codigo}-{var_data['talla'].nombre}-{var_data['color'].nombre[:3].upper()}"

    variante, created = ProductoVariante.objects.get_or_create(
        producto=producto,
        talla=var_data['talla'],
        color=var_data['color'],
        defaults={
            'codigo_variante': codigo_variante,
            'stock_actual': var_data['stock'],
            'stock_minimo': var_data['stock_min'],
            'activo': True,
        }
    )
    if created:
        print(f"  ✅ Variante: {variante.codigo_variante} (Stock: {variante.stock_actual})")
    else:
        print(f"  ℹ️  Variante ya existe: {variante.codigo_variante}")

# ========== CLIENTES ==========
print("\n👥 Creando Clientes...")
clientes_data = [
    {
        'codigo': 'CLI001',
        'tipo_documento': 'DNI',
        'numero_documento': '12345678',
        'nombres': 'Juan',
        'apellidos': 'Pérez García',
        'email': 'juan.perez@email.com',
        'telefono': '987654321',
        'direccion': 'Av. Principal 123, Lima',
    },
    {
        'codigo': 'CLI002',
        'tipo_documento': 'DNI',
        'numero_documento': '87654321',
        'nombres': 'María',
        'apellidos': 'González López',
        'email': 'maria.gonzalez@email.com',
        'telefono': '987123456',
        'direccion': 'Jr. Los Pinos 456, Lima',
    },
    {
        'codigo': 'CLI003',
        'tipo_documento': 'CE',
        'numero_documento': '001234567',
        'nombres': 'Carlos',
        'apellidos': 'Rodríguez Sánchez',
        'email': 'carlos.rodriguez@email.com',
        'telefono': '956789123',
        'direccion': 'Calle Las Flores 789, Callao',
    },
]

for cli_data in clientes_data:
    cliente, created = Cliente.objects.get_or_create(
        numero_documento=cli_data['numero_documento'],
        defaults=cli_data
    )
    if created:
        print(f"  ✅ Cliente: {cliente.nombre_completo}")
    else:
        print(f"  ℹ️  Cliente ya existe: {cliente.nombre_completo}")

# ========== PROVEEDORES ==========
print("\n🏢 Creando Proveedores...")
proveedores_data = [
    {
        'codigo': 'PROV001',
        'nombre': 'Distribuidora Deportes SAC',
        'ruc': '20123456789',
        'telefono': '014567890',
        'email': 'ventas@distdeportes.com',
        'contacto': 'Luis Martínez',
        'direccion': 'Av. Industrial 100, Lima',
    },
    {
        'codigo': 'PROV002',
        'nombre': 'Importaciones Textiles SRL',
        'ruc': '20987654321',
        'telefono': '017891234',
        'email': 'contacto@imptextiles.com',
        'contacto': 'Ana Torres',
        'direccion': 'Jr. Comercio 250, Lima',
    },
]

for prov_data in proveedores_data:
    proveedor, created = Proveedor.objects.get_or_create(
        ruc=prov_data['ruc'],
        defaults=prov_data
    )
    if created:
        print(f"  ✅ Proveedor: {proveedor.nombre}")
    else:
        print(f"  ℹ️  Proveedor ya existe: {proveedor.nombre}")

# ========== RESUMEN ==========
print("\n" + "="*60)
print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
print("="*60)
print(f"📁 Categorías: {Categoria.objects.count()}")
print(f"🏷️  Marcas: {Marca.objects.count()}")
print(f"📏 Tallas: {Talla.objects.count()}")
print(f"🎨 Colores: {Color.objects.count()}")
print(f"📦 Productos: {Producto.objects.count()}")
print(f"🔢 Variantes: {ProductoVariante.objects.count()}")
print(f"👥 Clientes: {Cliente.objects.count()}")
print(f"🏢 Proveedores: {Proveedor.objects.count()}")
print("="*60)
print("\n🎉 ¡Listo para probar el sistema!")
print("\n📝 Acceso Admin:")
print("   URL: http://localhost:8000/admin")
print("   Usuario: admin")
print("   Contraseña: admin123")
print("\n🌐 Frontend Vue:")
print("   URL: http://localhost:8081")
print("="*60)
