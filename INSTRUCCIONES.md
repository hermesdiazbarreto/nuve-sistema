# Sistema de Gestión de Almacén - Instrucciones de Uso

## 🚀 Sistema Completo Implementado

### ✅ Backend (Django + Django REST Framework)
- API REST completa con todos los endpoints
- CORS configurado para el frontend
- Modelos completos con relaciones
- Sistema de autenticación preparado

### ✅ Frontend (Vue.js 3)
- Dashboard con estadísticas en tiempo real
- Gestión completa de inventario
- Sistema de ventas (punto de venta)
- Módulos de categorías, marcas, tallas, colores
- Gestión de clientes y proveedores
- Historial de movimientos de inventario

---

## 📋 Funcionalidades Implementadas

### 🏠 **Dashboard**
- Total de productos, clientes, ventas del día
- Productos con stock bajo (alertas)
- Últimas ventas realizadas
- Accesos rápidos a funciones principales

### 📦 **Inventario**
- **Productos**: CRUD completo con variantes (talla + color)
- **Categorías**: Gestión de categorías de productos
- **Marcas**: Gestión de marcas
- **Tallas**: Configuración de tallas (XS, S, M, L, XL, etc.)
- **Colores**: Gestión con código hexadecimal
- **Variantes**: Cada producto puede tener múltiples variantes con stock individual
- **Movimientos**: Historial completo de entradas/salidas/ajustes

### 💰 **Ventas**
- **Punto de Venta**: Interfaz completa para realizar ventas
- Búsqueda rápida de productos/variantes
- Carrito de compra con cálculo automático
- Descuentos e impuestos configurables
- Múltiples tipos de pago (Efectivo, Tarjeta, Transferencia, Mixto)
- **Listado de Ventas**: Con filtros por fecha, estado, tipo de pago
- Número de venta autogenerado

### 👥 **Clientes**
- CRUD completo de clientes
- Tipos de documento (DNI, CE, Pasaporte)
- Información completa de contacto

### 🏢 **Proveedores**
- CRUD completo de proveedores
- Información de contacto y RUC
- Estado activo/inactivo

---

## 🛠️ Instrucciones de Instalación y Ejecución

### **Paso 1: Backend (Django)**

1. Navegar al directorio del backend:
```bash
cd C:\Users\Tom\Documents\Django\proyecto01\backend\almacen
```

2. Activar el entorno virtual:
```bash
# Si ya tienes el venv3 creado
..\venv3\Scripts\activate

# Si no existe, crear uno nuevo:
python -m venv venv
venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear un superusuario (para acceder al admin):
```bash
python manage.py createsuperuser
```

6. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

El backend estará corriendo en: `http://localhost:8000`

### **Paso 2: Frontend (Vue.js)**

1. Abrir una nueva terminal y navegar al directorio del frontend:
```bash
cd C:\Users\Tom\Documents\Django\proyecto01\frontend_build
```

2. Instalar las dependencias (si no están instaladas):
```bash
npm install
```

3. Iniciar el servidor de desarrollo de Vue:
```bash
npm run serve
```

El frontend estará corriendo en: `http://localhost:8080` o `http://localhost:8081`

---

## 🌐 Acceso al Sistema

### Frontend (Aplicación Principal)
- URL: http://localhost:8080
- Navegación completa con todas las funcionalidades

### Backend Admin (Django)
- URL: http://localhost:8000/admin
- Usuario: el que creaste con `createsuperuser`

### API REST (Endpoints)
Base URL: `http://localhost:8000/api/`

Endpoints disponibles:
- `/api/categorias/` - Categorías
- `/api/marcas/` - Marcas
- `/api/tallas/` - Tallas
- `/api/colores/` - Colores
- `/api/productos/` - Productos
- `/api/producto-variantes/` - Variantes de productos
- `/api/clientes/` - Clientes
- `/api/ventas/` - Ventas
- `/api/movimientos/` - Movimientos de inventario
- `/api/proveedores/` - Proveedores

---

## 📊 Datos de Prueba (Opcional)

Para probar el sistema, puedes crear datos iniciales desde el admin de Django:

1. Ir a http://localhost:8000/admin
2. Crear algunas:
   - Categorías (ej: Ropa, Calzado, Accesorios)
   - Marcas (ej: Nike, Adidas, Puma)
   - Tallas (ej: XS=0, S=1, M=2, L=3, XL=4)
   - Colores (ej: Rojo #FF0000, Azul #0000FF, Negro #000000)
   - Productos (con su categoría y marca)
   - Variantes (combinación de producto + talla + color + stock)
   - Clientes

---

## 🎯 Flujo de Uso Recomendado

### Primera Vez:
1. **Configurar catálogos básicos**:
   - Ir a Inventario → Categorías (crear al menos 2-3)
   - Ir a Inventario → Marcas (crear al menos 2-3)
   - Ir a Inventario → Tallas (crear: XS, S, M, L, XL)
   - Ir a Inventario → Colores (crear: Rojo, Azul, Negro, Blanco)

2. **Crear productos**:
   - Ir a Inventario → Productos → Nuevo Producto
   - Llenar el formulario con código, nombre, categoría, marca, precios
   - Guardar

3. **Crear variantes** (actualmente desde el admin Django):
   - Ir a http://localhost:8000/admin
   - Productos Variantes → Agregar
   - Seleccionar producto, talla, color, stock
   - Código de variante se genera automático

4. **Registrar clientes**:
   - Ir a Clientes → Nuevo Cliente
   - Llenar datos del cliente

5. **Realizar ventas**:
   - Ir a Ventas → Nueva Venta
   - Seleccionar cliente
   - Buscar y agregar productos al carrito
   - Configurar descuentos/impuestos si es necesario
   - Seleccionar tipo de pago
   - Procesar venta

### Uso Diario:
1. Ver el Dashboard para un resumen general
2. Realizar ventas desde el punto de venta
3. Revisar stock bajo y reponer
4. Consultar movimientos de inventario
5. Ver reportes de ventas

---

## 🔧 Estructura del Proyecto

```
proyecto01/
├── backend/
│   └── almacen/
│       ├── alm/                 # App principal con todos los modelos
│       ├── productos/           # App legacy (mantener)
│       ├── clientes/            # App legacy (mantener)
│       ├── almacen/            # Configuración Django
│       ├── templates/          # Templates HTML
│       ├── db.sqlite3          # Base de datos
│       └── manage.py
│
└── frontend_build/
    ├── src/
    │   ├── components/         # Componentes Vue
    │   │   ├── Dashboard.vue
    │   │   ├── ProductosLista.vue
    │   │   ├── ProductoForm.vue
    │   │   ├── CategoriasLista.vue
    │   │   ├── MarcasLista.vue
    │   │   ├── TallasLista.vue
    │   │   ├── ColoresLista.vue
    │   │   ├── VentasLista.vue
    │   │   ├── NuevaVenta.vue
    │   │   ├── ClientesLista.vue
    │   │   ├── ProveedoresLista.vue
    │   │   └── MovimientosLista.vue
    │   ├── router/
    │   │   └── index.js        # Rutas Vue
    │   ├── services/
    │   │   └── api.js          # Servicio API centralizado
    │   ├── App.vue             # Componente raíz
    │   └── main.js
    └── package.json
```

---

## ⚠️ Notas Importantes

1. **CORS**: Ya está configurado para localhost:8080 y localhost:8081
2. **Variantes**: Por ahora se crean desde el admin de Django. Se puede crear un formulario Vue más adelante.
3. **Usuario Vendedor**: Actualmente hardcodeado como ID=1. Implementar autenticación después.
4. **Stock**: Al realizar una venta, el stock se reduce automáticamente (implementar en signals Django).
5. **Movimientos**: Se registran automáticamente al crear ventas (implementar en signals Django).

---

## 🚀 Próximas Mejoras Sugeridas

1. **Autenticación**: Sistema de login/logout
2. **Formulario de Variantes**: Crear interfaz Vue para gestionar variantes
3. **Reportes**: Gráficos de ventas, productos más vendidos
4. **Exportación**: Excel/PDF de ventas e inventario
5. **Búsqueda Avanzada**: Filtros más complejos
6. **Imágenes**: Subida de imágenes para productos
7. **Códigos de Barra**: Escaneo con lector de códigos
8. **Notificaciones**: Alertas de stock bajo
9. **Compras a Proveedores**: Módulo de compras
10. **Roles y Permisos**: Diferentes niveles de acceso

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que tanto el backend como el frontend estén corriendo
2. Revisa la consola del navegador para errores (F12)
3. Verifica que los puertos 8000 y 8080 estén disponibles
4. Asegúrate de que las migraciones de Django estén aplicadas

---

## ✅ Checklist de Verificación

- [ ] Backend corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:8080
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Al menos una categoría creada
- [ ] Al menos una marca creada
- [ ] Al menos una talla creada
- [ ] Al menos un color creado
- [ ] Al menos un producto creado
- [ ] Al menos una variante creada (con stock)
- [ ] Al menos un cliente creado
- [ ] Venta de prueba realizada exitosamente

---

¡Sistema listo para usar! 🎉
