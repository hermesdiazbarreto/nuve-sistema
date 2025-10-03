# 🧪 GUÍA RÁPIDA PARA PROBAR EL SISTEMA

## ✅ Estado Actual
- ✅ Backend Django configurado y corriendo en http://localhost:8000
- ⚠️ Frontend Vue necesita reiniciarse (arreglamos configuración ESLint)

---

## 📝 PASOS PARA PROBAR TODO

### **PASO 1: Detener y Reiniciar Frontend**

1. **Presiona** `Ctrl+C` en la terminal donde está corriendo Vue (si está corriendo)

2. **Ejecuta nuevamente:**
```bash
cd C:\Users\Tom\Documents\Django\proyecto01\frontend_build
npm run serve
```

3. **Espera** hasta ver el mensaje:
```
  App running at:
  - Local:   http://localhost:8080/
  - Network: http://192.168.x.x:8080/
```

---

### **PASO 2: Crear Datos Iniciales desde Django Admin**

1. **Abre tu navegador** en: http://localhost:8000/admin

2. **Inicia sesión** (si no tienes usuario, créalo con `python manage.py createsuperuser`)

3. **Crear Categorías:**
   - Click en "Categorías" → "Agregar categoría"
   - Crear 3-4 categorías:
     - Ropa (activo: ✓)
     - Calzado (activo: ✓)
     - Accesorios (activo: ✓)

4. **Crear Marcas:**
   - Click en "Marcas" → "Agregar marca"
   - Crear 3-4 marcas:
     - Nike (activo: ✓)
     - Adidas (activo: ✓)
     - Puma (activo: ✓)

5. **Crear Tallas:**
   - Click en "Tallas" → "Agregar talla"
   - Crear:
     - XS (orden: 0)
     - S (orden: 1)
     - M (orden: 2)
     - L (orden: 3)
     - XL (orden: 4)

6. **Crear Colores:**
   - Click en "Colores" → "Agregar color"
   - Crear:
     - Rojo (código: #FF0000)
     - Azul (código: #0000FF)
     - Negro (código: #000000)
     - Blanco (código: #FFFFFF)

7. **Crear Clientes:**
   - Click en "Clientes" → "Agregar cliente"
   - Crear 2-3 clientes con:
     - Código: CLI001, CLI002, CLI003
     - Nombres y apellidos
     - Tipo documento: DNI
     - Número documento: 12345678
     - Email y teléfono
     - Activo: ✓

---

### **PASO 3: Probar el Frontend Vue**

1. **Abre** http://localhost:8080 en tu navegador

2. **Verás el Dashboard** con:
   - 📊 Tarjetas de estadísticas
   - 📋 Productos con stock bajo (vacío por ahora)
   - 💰 Últimas ventas (vacío por ahora)
   - 🚀 Botones de acceso rápido

---

### **PASO 4: Crear Productos desde Vue**

1. **Click** en el menú "Inventario" → "Productos"

2. **Click** en "➕ Nuevo Producto"

3. **Llenar el formulario:**
   - Código: PROD001
   - Nombre: Camiseta Deportiva
   - Descripción: Camiseta de algodón
   - Categoría: Ropa
   - Marca: Nike
   - Precio compra: 50.00
   - Precio venta: 100.00
   - Activo: ✓

4. **Guardar**

5. **Repetir** para crear 3-4 productos más

---

### **PASO 5: Crear Variantes desde Django Admin**

*Las variantes aún se crean desde el admin porque es más rápido*

1. **Volver a** http://localhost:8000/admin

2. **Click** en "Productos Variantes" → "Agregar producto variante"

3. **Llenar:**
   - Producto: (seleccionar el que creaste)
   - Talla: M
   - Color: Rojo
   - Código variante: PROD001-M-R
   - Stock actual: 50
   - Stock mínimo: 5
   - Activo: ✓

4. **Guardar**

5. **Repetir** creando varias variantes:
   - Mismo producto, diferentes tallas/colores
   - Diferentes productos

6. **Crear algunas con stock bajo** (ej: stock_actual = 3, stock_minimo = 5)

---

### **PASO 6: Probar el Dashboard Actualizado**

1. **Volver a** http://localhost:8080

2. **Refresh** la página (F5)

3. **Deberías ver:**
   - 📦 Total Productos: 4 (o los que creaste)
   - 👥 Total Clientes: 3 (o los que creaste)
   - ⚠️ Stock Bajo: Variantes con stock bajo

---

### **PASO 7: Explorar todos los Módulos**

#### **A. Categorías**
- Click "Inventario" → "Categorías"
- Ver listado
- Crear nueva categoría con el botón modal
- Editar, eliminar

#### **B. Marcas**
- Click "Inventario" → "Marcas"
- Ver listado
- Crear, editar, eliminar

#### **C. Tallas**
- Click "Inventario" → "Tallas"
- Ver listado ordenado
- Crear, editar

#### **D. Colores**
- Click "Inventario" → "Colores"
- Ver tarjetas con colores visuales
- Crear color con selector
- Ver preview

#### **E. Productos**
- Click "Inventario" → "Productos"
- Ver listado completo
- Click "Ver variantes" en cualquier producto
- Ver stock total calculado

#### **F. Movimientos**
- Click "Inventario" → "Movimientos"
- Ver historial (vacío por ahora)
- Probar filtros por tipo y fecha

#### **G. Clientes**
- Click "Clientes"
- Ver listado de clientes

#### **H. Proveedores**
- Click "Proveedores"
- Crear proveedor con modal
- Llenar RUC, nombre, teléfono, etc.

---

### **PASO 8: ⭐ PROBAR PUNTO DE VENTA (Lo Más Importante)**

1. **Click** en "Ventas" → "Nueva Venta"

2. **Buscar producto:**
   - Escribe en el buscador: "camiseta" o el nombre de tu producto
   - Ver filtrado en tiempo real

3. **Agregar productos al carrito:**
   - Click "➕ Agregar" en las variantes que quieras
   - Ver el carrito llenarse a la derecha

4. **Modificar cantidades:**
   - Usar botones + / -
   - O escribir directamente la cantidad
   - Validación automática de stock

5. **Seleccionar cliente:**
   - Desplegable "Cliente"
   - Elegir uno

6. **Configurar venta:**
   - Descuento: 10.00 (opcional)
   - Impuesto: 18 (IGV/IVA %)
   - Tipo de pago: Efectivo/Tarjeta/Transferencia
   - Observaciones: "Venta de prueba"

7. **Ver cálculos automáticos:**
   - Subtotal se calcula solo
   - Descuento se resta
   - Impuesto se aplica
   - **TOTAL** se muestra en grande

8. **Procesar Venta:**
   - Click "💰 Procesar Venta"
   - Confirmar
   - ✅ Ver mensaje de éxito

9. **Verificar efectos:**
   - Ir a "Ventas" → Ver la venta creada
   - Ir a "Inventario" → "Movimientos" → Ver movimientos de salida
   - Ir a "Productos" → Ver stock reducido

---

### **PASO 9: Verificar el Sistema Completo**

1. **Volver al Dashboard**
   - Ver estadísticas actualizadas
   - "Ventas Hoy": 1
   - "Últimas Ventas": Tu venta aparece

2. **Ver Listado de Ventas:**
   - Click "Ventas"
   - Ver tabla con todas las ventas
   - Filtrar por estado/fecha
   - Ver totales calculados

3. **Ver Movimientos de Inventario:**
   - Click "Inventario" → "Movimientos"
   - Ver entrada "SALIDA" con:
     - Cantidad vendida
     - Stock anterior
     - Stock nuevo
     - Motivo: "Venta V-000001"
     - Usuario

---

## ✅ CHECKLIST DE PRUEBAS COMPLETAS

- [ ] ✅ Backend corriendo en http://localhost:8000
- [ ] ✅ Frontend corriendo en http://localhost:8080
- [ ] ✅ Dashboard muestra estadísticas
- [ ] ✅ Creadas 3+ categorías
- [ ] ✅ Creadas 3+ marcas
- [ ] ✅ Creadas 5 tallas
- [ ] ✅ Creados 4+ colores
- [ ] ✅ Creados 3+ productos
- [ ] ✅ Creadas 10+ variantes (con stock)
- [ ] ✅ Creados 3+ clientes
- [ ] ✅ Creado 1+ proveedor
- [ ] ✅ Probada navegación por todos los módulos
- [ ] ✅ Realizada 1+ venta desde el punto de venta
- [ ] ✅ Verificado stock reducido tras venta
- [ ] ✅ Verificados movimientos de inventario
- [ ] ✅ Probados filtros en ventas y movimientos
- [ ] ✅ Probados CRUD de categorías, marcas, tallas, colores
- [ ] ✅ Verificado funcionamiento de búsqueda en punto de venta

---

## 🎯 FUNCIONALIDADES CLAVE A PROBAR

### **Punto de Venta:**
- ✅ Búsqueda en tiempo real de productos
- ✅ Agregar/quitar del carrito
- ✅ Incrementar/decrementar cantidades
- ✅ Validación de stock máximo
- ✅ Cálculo automático de subtotal/descuento/impuesto/total
- ✅ Procesamiento de venta
- ✅ Reducción automática de stock
- ✅ Registro automático de movimiento

### **Gestión de Inventario:**
- ✅ Ver productos con variantes
- ✅ Stock total calculado
- ✅ Alertas de stock bajo
- ✅ Historial de movimientos
- ✅ Filtros por fecha y tipo

### **Maestros:**
- ✅ CRUD completo de categorías, marcas, tallas, colores
- ✅ Validaciones
- ✅ Estados activo/inactivo

---

## 🐛 Solución de Problemas

### **Frontend no compila:**
```bash
# Detener con Ctrl+C
# Limpiar cache
rm -rf node_modules/.cache
# Reiniciar
npm run serve
```

### **Error de CORS:**
- Verificar que Django esté corriendo
- Verificar CORS_ALLOWED_ORIGINS en settings.py

### **No aparecen datos:**
- Hacer refresh (F5)
- Abrir consola del navegador (F12) y ver errores
- Verificar que el backend responda: http://localhost:8000/api/productos/

### **Error al crear venta:**
- Asegúrate de tener variantes con stock > 0
- Verifica que el cliente esté seleccionado
- Verifica que el tipo de pago esté seleccionado

---

## 🎉 ¡Todo listo!

Si todos los pasos funcionan, tienes un sistema completo de gestión de almacén funcionando con:
- Dashboard interactivo
- Gestión de inventario con variantes
- Punto de venta profesional
- Registro automático de movimientos
- Sistema de clientes y proveedores

¡Disfruta probando tu sistema! 🚀
