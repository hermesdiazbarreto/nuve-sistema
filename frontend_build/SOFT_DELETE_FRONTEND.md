# Soft Delete - Frontend (Vue.js)

## Implementación Completada

Se ha implementado el sistema de **soft delete** para productos en el frontend Vue.js. Los cambios incluyen:

## Archivos Modificados/Creados

### 1. **services/api.js** ✅
Se agregaron los siguientes métodos:

```javascript
// Eliminar producto (soft delete)
deleteProducto(id)

// Restaurar producto eliminado
restaurarProducto(id)

// Obtener solo productos eliminados
getProductosEliminados()

// Obtener todos los productos incluyendo eliminados
getProductosConEliminados()
```

### 2. **components/ProductosLista.vue** ✅
- Se agregó botón "🗑️ Ver Eliminados" que redirige a `/productos/eliminados`
- Se mejoró el mensaje de confirmación al eliminar para informar que es soft delete
- Se muestra el mensaje del backend tras eliminar exitosamente

### 3. **components/ProductosEliminados.vue** ✅ (NUEVO)
Componente completamente nuevo que muestra:
- Lista de productos eliminados en tabla con estilo visual diferente (fila roja)
- Información de cuándo y quién eliminó cada producto
- Botón "♻️ Restaurar" para cada producto
- Modal con detalles completos del producto eliminado
- Mensaje informativo cuando no hay productos eliminados

### 4. **router/index.js** ✅
Se agregó la ruta:
```javascript
{
  path: '/productos/eliminados',
  name: 'ProductosEliminados',
  component: ProductosEliminados
}
```

## Flujo de Uso

### Eliminar un Producto

1. Ir a **Productos** (`/productos`)
2. Click en botón **🗑️** de cualquier producto
3. Confirmar la eliminación (mensaje indica que es reversible)
4. El producto desaparece del listado
5. Mensaje de confirmación del backend

### Ver Productos Eliminados

1. Ir a **Productos** (`/productos`)
2. Click en botón **"🗑️ Ver Eliminados"**
3. Se muestra tabla con productos eliminados que incluye:
   - Código del producto
   - Nombre
   - Categoría y Marca
   - Precio de venta
   - **Fecha de eliminación**
   - **Usuario que lo eliminó**
   - Botones de acción

### Restaurar un Producto

**Opción 1: Desde la tabla**
1. En `/productos/eliminados`
2. Click en botón **"♻️ Restaurar"** del producto deseado
3. Confirmar la restauración
4. El producto vuelve a estar activo

**Opción 2: Desde el modal de detalles**
1. En `/productos/eliminados`
2. Click en botón **"👁️"** para ver detalles
3. En el modal, click en **"♻️ Restaurar Producto"**
4. Confirmar la restauración

## Características Visuales

### ProductosEliminados.vue

- **Tabla con estilo rojo**: Las filas tienen clase `table-danger` para indicar visualmente que están eliminadas
- **Badge de usuario**: Muestra quién eliminó el producto con un badge oscuro
- **Formato de fecha**: Las fechas se muestran en formato español legible
- **Alerta informativa**: Se muestra un aviso amarillo explicando que los productos pueden restaurarse
- **Estado vacío**: Cuando no hay productos eliminados, muestra un mensaje positivo con ✅

### Mensajes al Usuario

- **Al eliminar**: "El producto no se borrará permanentemente, solo se marcará como eliminado. Podrás restaurarlo desde 'Ver Eliminados'."
- **Al restaurar**: "El producto volverá a estar activo y visible en el listado principal."
- **Lista vacía**: "✅ No hay productos eliminados. Todos los productos están activos."

## Endpoints Utilizados

```
GET  /api/productos/                     → Productos activos (default)
GET  /api/productos/?solo_eliminados=true → Solo eliminados
DELETE /api/productos/{id}/              → Soft delete
POST /api/productos/{id}/restaurar/      → Restaurar producto
```

## Estructura de Respuestas del Backend

### Al Eliminar
```json
{
  "message": "Producto eliminado correctamente. El producto ya no aparecerá en los listados pero su historial se mantiene.",
  "deleted_at": "2025-10-08T12:30:45.123456Z"
}
```

### Al Restaurar
```json
{
  "message": "Producto restaurado correctamente.",
  "producto": {
    "id": 1,
    "codigo": "PROD001",
    "nombre": "Producto Test",
    ...
  }
}
```

### Productos Eliminados (GET)
```json
[
  {
    "id": 1,
    "codigo": "PROD001",
    "nombre": "Producto Test",
    "categoria_nombre": "Categoría 1",
    "marca_nombre": "Marca 1",
    "precio_venta": "100.00",
    "is_deleted": true,
    "deleted_at": "2025-10-08T12:30:45.123456Z",
    "deleted_by_username": "admin",
    ...
  }
]
```

## Testing

### Probar el Soft Delete

1. **Iniciar el backend**:
```bash
cd C:\Users\Tom\Documents\Django
venv\Scripts\activate
cd proyecto01\backend\almacen
python manage.py runserver
```

2. **Iniciar el frontend**:
```bash
cd C:\Users\Tom\Documents\Django\proyecto01\frontend_build
npm run serve
```

3. **Flujo de prueba**:
   - Crear un producto de prueba
   - Eliminarlo desde la lista
   - Verificar que desaparece
   - Ir a "Ver Eliminados"
   - Verificar que aparece ahí
   - Restaurarlo
   - Verificar que vuelve a la lista principal

### Casos a Probar

✅ Eliminar producto y verificar desaparición
✅ Ver lista de productos eliminados
✅ Ver detalles de producto eliminado en modal
✅ Restaurar producto desde tabla
✅ Restaurar producto desde modal
✅ Verificar que producto restaurado vuelve a lista principal
✅ Verificar campos de auditoría (fecha y usuario)

## Estilos Personalizados

```css
/* ProductosEliminados.vue */

/* Filas con hover rojo claro */
.table tbody tr:hover {
  background-color: #f8d7da !important;
}

/* Botón de cerrar blanco en modal */
.btn-close-white {
  filter: brightness(0) invert(1);
}
```

## Compatibilidad

- ✅ Vue.js 3
- ✅ Vue Router 4
- ✅ Bootstrap 5
- ✅ Axios para peticiones HTTP
- ✅ Compatible con autenticación Token

## Próximas Mejoras (Opcional)

1. **Paginación**: Para listas grandes de productos eliminados
2. **Búsqueda**: Filtrar productos eliminados por código o nombre
3. **Eliminación permanente**: Opción para eliminar permanentemente (hard delete) desde la vista de eliminados
4. **Filtros por fecha**: Ver productos eliminados en un rango de fechas
5. **Exportar**: Exportar lista de productos eliminados a CSV/Excel
6. **Notificaciones toast**: Usar toasts en lugar de alerts para mejor UX
7. **Confirmación con modal**: Usar modales de Bootstrap en lugar de confirm() nativo

## Notas Importantes

- Los productos eliminados **NO** se borran de la base de datos
- Se mantiene el historial completo de ventas y compras
- Solo usuarios autenticados pueden eliminar/restaurar productos
- El campo `deleted_by` registra quién eliminó el producto
- Al restaurar, el producto vuelve al estado `activo=True`
- Las variantes del producto también se desactivan/activan automáticamente

## Soporte

Si encuentras algún problema:
1. Verifica que el backend esté ejecutándose
2. Abre la consola del navegador (F12) para ver errores
3. Verifica que el token de autenticación sea válido
4. Comprueba que las migraciones se hayan ejecutado correctamente
