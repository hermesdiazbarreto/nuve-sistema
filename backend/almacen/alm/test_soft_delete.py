"""
Test para verificar el funcionamiento del soft delete en Productos
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Producto, Categoria, Marca

class TestProductoSoftDelete(TestCase):

    def setUp(self):
        """Configurar datos de prueba"""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.categoria = Categoria.objects.create(nombre="Test Categoria")
        self.marca = Marca.objects.create(nombre="Test Marca")

        self.producto = Producto.objects.create(
            codigo="TEST001",
            nombre="Producto Test",
            categoria=self.categoria,
            marca=self.marca,
            precio_compra=10.00,
            precio_venta=20.00
        )

    def test_producto_creado(self):
        """Verificar que el producto se crea correctamente"""
        self.assertEqual(Producto.objects.count(), 1)
        self.assertFalse(self.producto.is_deleted)
        self.assertIsNone(self.producto.deleted_at)
        self.assertIsNone(self.producto.deleted_by)

    def test_soft_delete(self):
        """Verificar que el soft delete funciona correctamente"""
        # Realizar soft delete
        self.producto.soft_delete(user=self.user)

        # Verificar que está marcado como eliminado
        self.assertTrue(self.producto.is_deleted)
        self.assertIsNotNone(self.producto.deleted_at)
        self.assertEqual(self.producto.deleted_by, self.user)
        self.assertFalse(self.producto.activo)

        # Verificar que no aparece en consultas normales
        self.assertEqual(Producto.objects.count(), 0)

        # Verificar que sí aparece con all_objects
        self.assertEqual(Producto.all_objects.count(), 1)

    def test_restore(self):
        """Verificar que la restauración funciona correctamente"""
        # Primero eliminar
        self.producto.soft_delete(user=self.user)
        self.assertEqual(Producto.objects.count(), 0)

        # Restaurar
        self.producto.restore()

        # Verificar que está restaurado
        self.assertFalse(self.producto.is_deleted)
        self.assertIsNone(self.producto.deleted_at)
        self.assertIsNone(self.producto.deleted_by)
        self.assertTrue(self.producto.activo)

        # Verificar que aparece en consultas normales
        self.assertEqual(Producto.objects.count(), 1)

    def test_manager_objects(self):
        """Verificar que el manager 'objects' excluye eliminados"""
        # Crear otro producto
        producto2 = Producto.objects.create(
            codigo="TEST002",
            nombre="Producto Test 2",
            categoria=self.categoria,
            marca=self.marca,
            precio_compra=15.00,
            precio_venta=25.00
        )

        # Inicialmente hay 2 productos
        self.assertEqual(Producto.objects.count(), 2)

        # Eliminar uno
        self.producto.soft_delete()

        # Solo debe quedar 1 en el manager normal
        self.assertEqual(Producto.objects.count(), 1)

        # Pero 2 con all_objects
        self.assertEqual(Producto.all_objects.count(), 2)

        # Verificar que el producto NO eliminado es el correcto
        self.assertEqual(Producto.objects.first(), producto2)
