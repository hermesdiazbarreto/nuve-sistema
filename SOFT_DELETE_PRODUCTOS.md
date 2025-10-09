# Soft Delete para Productos - Documentación

## Descripción

Se ha implementado un sistema de **soft delete** (eliminación suave) para los productos del sistema de gestión de almacén. Esto significa que cuando se elimina un producto, no se borra físicamente de la base de datos, sino que se marca como eliminado. Esto preserva el histórico de ventas y compras.

## Cambios Realizados

### 1. Modelo Producto (`alm/models.py`)

Se agregaron los siguientes campos al modelo `Producto`:

- `is_deleted` (BooleanField): Indica si el producto está eliminado (default: False)
- `deleted_at` (DateTimeField): Fecha y hora de eliminación (nullable)
- `deleted_by` (ForeignKey a User): Usuario que eliminó el producto (nullable)

Se crearon dos **managers personalizados**:

- `objects`: Manager por defecto que **excluye** productos eliminados
- `all_objects`: Manager que **incluye** todos los productos (incluso eliminados)

Se agregaron dos **métodos** al modelo:

- `soft_delete(user=None)`: Marca el producto como eliminado
- `restore()`: Restaura un producto eliminado

### 2. ProductoViewSet (`alm/views.py`)

#### Endpoint de Eliminación (DELETE)
- **URL**: `DELETE /api/productos/{id}/`
- **Funcionalidad**: Realiza soft delete del producto
- **Respuesta**:
```json
{
  "message": "Producto eliminado correctamente. El producto ya no aparecerá en los listados pero su historial se mantiene.",
  "deleted_at": "2025-10-08T12:30:45.123456Z"
}
```

#### Endpoint de Restauración (POST)
- **URL**: `POST /api/productos/{id}/restaurar/`
- **Funcionalidad**: Restaura un producto eliminado
- **Respuesta**:
```json
{
  "message": "Producto restaurado correctamente.",
  "producto": { ... }
}
```

#### Parámetros de Consulta (GET)

El endpoint GET ahora acepta los siguientes parámetros:

- `GET /api/productos/` - Solo productos activos y no eliminados (default)
- `GET /api/productos/?incluir_inactivos=true` - Incluye inactivos pero no eliminados
- `GET /api/productos/?incluir_eliminados=true` - Incluye todos (eliminados y no eliminados)
- `GET /api/productos/?solo_eliminados=true` - Solo productos eliminados

### 3. ProductoSerializer (`alm/serializers.py`)

Se agregó el campo:
- `deleted_by_username`: Nombre de usuario que eliminó el producto (read-only)

Los campos `is_deleted`, `deleted_at` y `deleted_by` son de solo lectura.

## Instrucciones para Aplicar los Cambios

### Paso 1: Arreglar el Entorno Virtual

Hay un problema de compatibilidad entre Django y Django REST Framework. Necesitas reinstalar las dependencias:

```bash
# Opción 1: Reinstalar el entorno virtual
cd C:\Users\Tom\Documents\Django\proyecto01
rmdir /s venv3
python -m venv venv3
venv3\Scripts\activate
pip install -r requirements.txt

# Opción 2: Actualizar dependencias en el venv existente
cd C:\Users\Tom\Documents\Django
venv\Scripts\activate
pip install --upgrade django djangorestframework
```

### Paso 2: Crear y Ejecutar Migraciones

```bash
cd C:\Users\Tom\Documents\Django
venv\Scripts\activate
cd proyecto01\backend\almacen
python manage.py makemigrations
python manage.py migrate
```

### Paso 3: Verificar en Django Admin

1. Ejecuta el servidor:
```bash
python manage.py runserver
```

2. Accede al admin: `http://localhost:8000/admin`

3. Verifica que los nuevos campos aparezcan en el modelo Producto:
   - Eliminado (is_deleted)
   - Fecha de eliminación (deleted_at)
   - Eliminado por (deleted_by)

## Uso desde el Frontend

### Ejemplo: Eliminar un Producto

```javascript
// En services/api.js o donde hagas las llamadas API
async function deleteProducto(id) {
  try {
    const response = await axios.delete(`/api/productos/${id}/`);
    console.log(response.data.message);
    return response.data;
  } catch (error) {
    console.error('Error al eliminar producto:', error);
    throw error;
  }
}
```

### Ejemplo: Restaurar un Producto

```javascript
async function restaurarProducto(id) {
  try {
    const response = await axios.post(`/api/productos/${id}/restaurar/`);
    console.log(response.data.message);
    return response.data.producto;
  } catch (error) {
    console.error('Error al restaurar producto:', error);
    throw error;
  }
}
```

### Ejemplo: Ver Productos Eliminados

```javascript
async function getProductosEliminados() {
  try {
    const response = await axios.get('/api/productos/?solo_eliminados=true');
    return response.data;
  } catch (error) {
    console.error('Error al obtener productos eliminados:', error);
    throw error;
  }
}
```

## Comportamiento del Sistema

### Al Eliminar un Producto:
1. Se marca `is_deleted = True`
2. Se registra `deleted_at` con la fecha/hora actual
3. Se registra `deleted_by` con el usuario que realizó la acción
4. Se marca `activo = False`
5. Se desactivan todas las variantes del producto

### Al Restaurar un Producto:
1. Se marca `is_deleted = False`
2. Se limpia `deleted_at` (None)
3. Se limpia `deleted_by` (None)
4. Se marca `activo = True`
5. Se reactivan todas las variantes del producto

### Consultas por Defecto:
- `Producto.objects.all()` → Solo productos NO eliminados
- `Producto.all_objects.all()` → Todos los productos (incluye eliminados)

## Ventajas del Soft Delete

1. **Preserva el histórico**: Las ventas y compras antiguas mantienen la referencia al producto
2. **Reversible**: Se puede restaurar un producto eliminado por error
3. **Auditoría**: Se sabe quién eliminó el producto y cuándo
4. **Integridad referencial**: No se rompen las relaciones de base de datos

## Próximos Pasos (Opcional)

Si deseas implementar esto en el frontend Vue.js:

1. Agregar una vista para ver productos eliminados
2. Agregar botones de "Restaurar" en la lista de productos eliminados
3. Agregar confirmación antes de eliminar
4. Mostrar indicador visual de productos eliminados
5. Implementar filtros para mostrar/ocultar productos eliminados

## Testing

Para probar la funcionalidad:

```bash
# Crear tests en alm/tests.py
python manage.py test alm.tests.TestProductoSoftDelete
```

Ejemplo de test:

```python
from django.test import TestCase
from alm.models import Producto, Categoria, Marca

class TestProductoSoftDelete(TestCase):
    def test_soft_delete(self):
        # Crear producto de prueba
        categoria = Categoria.objects.create(nombre="Test")
        marca = Marca.objects.create(nombre="Test")
        producto = Producto.objects.create(
            codigo="TEST001",
            nombre="Producto Test",
            categoria=categoria,
            marca=marca,
            precio_compra=10.00,
            precio_venta=20.00
        )

        # Realizar soft delete
        producto.soft_delete()

        # Verificar que está eliminado
        self.assertTrue(producto.is_deleted)
        self.assertIsNotNone(producto.deleted_at)

        # Verificar que no aparece en consultas normales
        self.assertEqual(Producto.objects.count(), 0)

        # Verificar que sí aparece con all_objects
        self.assertEqual(Producto.all_objects.count(), 1)

        # Restaurar
        producto.restore()

        # Verificar que está restaurado
        self.assertFalse(producto.is_deleted)
        self.assertIsNone(producto.deleted_at)
        self.assertEqual(Producto.objects.count(), 1)
```
