from django.core.management.base import BaseCommand
from alm.models import Categoria, Marca, Talla, Color, Producto, ProductoVariante, Cliente, Proveedor
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de almacen'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))

        # Crear usuario administrador si no existe
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Usuario admin creado (user: admin, pass: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('Usuario admin ya existe'))

        # CATEGORIAS
        self.stdout.write('\nCreando Categorias...')
        categorias_data = [
            {'nombre': 'Ropa', 'descripcion': 'Prendas de vestir', 'activo': True},
            {'nombre': 'Calzado', 'descripcion': 'Zapatos y zapatillas', 'activo': True},
            {'nombre': 'Accesorios', 'descripcion': 'Complementos y accesorios', 'activo': True},
            {'nombre': 'Deportivo', 'descripcion': 'Articulos deportivos', 'activo': True},
        ]

        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  Categoria: {categoria.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Categoria ya existe: {categoria.nombre}'))

        # MARCAS
        self.stdout.write('\nCreando Marcas...')
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
                self.stdout.write(self.style.SUCCESS(f'  Marca: {marca.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Marca ya existe: {marca.nombre}'))

        # TALLAS
        self.stdout.write('\nCreando Tallas...')
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
                self.stdout.write(self.style.SUCCESS(f'  Talla: {talla.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Talla ya existe: {talla.nombre}'))

        # COLORES
        self.stdout.write('\nCreando Colores...')
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
                self.stdout.write(self.style.SUCCESS(f'  Color: {color.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Color ya existe: {color.nombre}'))

        # PRODUCTOS
        self.stdout.write('\nCreando Productos...')
        productos_data = [
            {
                'codigo': 'PROD001',
                'nombre': 'Camiseta Deportiva',
                'descripcion': 'Camiseta de algodon para deporte',
                'categoria': 'Ropa',
                'marca': 'Nike',
                'precio_compra': 50.00,
                'precio_venta': 100.00,
            },
            {
                'codigo': 'PROD002',
                'nombre': 'Zapatillas Running',
                'descripcion': 'Zapatillas para correr con amortiguacion',
                'categoria': 'Calzado',
                'marca': 'Adidas',
                'precio_compra': 150.00,
                'precio_venta': 299.99,
            },
            {
                'codigo': 'PROD003',
                'nombre': 'Pantalon Deportivo',
                'descripcion': 'Pantalon comodo para entrenar',
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
                'descripcion': 'Sudadera comoda y abrigada',
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
                self.stdout.write(self.style.SUCCESS(f'  Producto: {producto.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Producto ya existe: {producto.nombre}'))

        # VARIANTES DE PRODUCTOS
        self.stdout.write('\nCreando Variantes de Productos...')

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
            {'producto': 'PROD001', 'talla': talla_xl, 'color': color_negro, 'stock': 5, 'stock_min': 10},

            # Zapatillas Running
            {'producto': 'PROD002', 'talla': talla_m, 'color': color_negro, 'stock': 20, 'stock_min': 5},
            {'producto': 'PROD002', 'talla': talla_l, 'color': color_azul, 'stock': 15, 'stock_min': 5},
            {'producto': 'PROD002', 'talla': talla_xl, 'color': color_blanco, 'stock': 3, 'stock_min': 5},

            # Pantalon Deportivo
            {'producto': 'PROD003', 'talla': talla_m, 'color': color_negro, 'stock': 40, 'stock_min': 8},
            {'producto': 'PROD003', 'talla': talla_l, 'color': color_azul, 'stock': 35, 'stock_min': 8},

            # Sudadera
            {'producto': 'PROD005', 'talla': talla_m, 'color': color_negro, 'stock': 25, 'stock_min': 5},
            {'producto': 'PROD005', 'talla': talla_l, 'color': color_azul, 'stock': 2, 'stock_min': 5},
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
                self.stdout.write(self.style.SUCCESS(f'  Variante: {variante.codigo_variante} (Stock: {variante.stock_actual})'))
            else:
                self.stdout.write(self.style.WARNING(f'  Variante ya existe: {variante.codigo_variante}'))

        # CLIENTES
        self.stdout.write('\nCreando Clientes...')
        clientes_data = [
            {
                'codigo': 'CLI001',
                'tipo_documento': 'DNI',
                'numero_documento': '12345678',
                'nombres': 'Juan',
                'apellidos': 'Perez Garcia',
                'email': 'juan.perez@email.com',
                'telefono': '987654321',
                'direccion': 'Av. Principal 123, Lima',
            },
            {
                'codigo': 'CLI002',
                'tipo_documento': 'DNI',
                'numero_documento': '87654321',
                'nombres': 'Maria',
                'apellidos': 'Gonzalez Lopez',
                'email': 'maria.gonzalez@email.com',
                'telefono': '987123456',
                'direccion': 'Jr. Los Pinos 456, Lima',
            },
            {
                'codigo': 'CLI003',
                'tipo_documento': 'CE',
                'numero_documento': '001234567',
                'nombres': 'Carlos',
                'apellidos': 'Rodriguez Sanchez',
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
                self.stdout.write(self.style.SUCCESS(f'  Cliente: {cliente.nombre_completo}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Cliente ya existe: {cliente.nombre_completo}'))

        # PROVEEDORES
        self.stdout.write('\nCreando Proveedores...')
        proveedores_data = [
            {
                'codigo': 'PROV001',
                'nombre': 'Distribuidora Deportes SAC',
                'ruc': '20123456789',
                'telefono': '014567890',
                'email': 'ventas@distdeportes.com',
                'contacto': 'Luis Martinez',
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
                self.stdout.write(self.style.SUCCESS(f'  Proveedor: {proveedor.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'  Proveedor ya existe: {proveedor.nombre}'))

        # RESUMEN
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('DATOS DE PRUEBA CREADOS EXITOSAMENTE'))
        self.stdout.write('='*60)
        self.stdout.write(f'Categorias: {Categoria.objects.count()}')
        self.stdout.write(f'Marcas: {Marca.objects.count()}')
        self.stdout.write(f'Tallas: {Talla.objects.count()}')
        self.stdout.write(f'Colores: {Color.objects.count()}')
        self.stdout.write(f'Productos: {Producto.objects.count()}')
        self.stdout.write(f'Variantes: {ProductoVariante.objects.count()}')
        self.stdout.write(f'Clientes: {Cliente.objects.count()}')
        self.stdout.write(f'Proveedores: {Proveedor.objects.count()}')
        self.stdout.write('='*60)
