# Backup Web - Descarga con Un Clic

Este documento explica cómo usar el endpoint de backup web para descargar backups de la base de datos desde cualquier navegador.

## 🎯 Ventajas

- ✅ **Súper fácil**: Un clic desde el navegador
- ✅ **Desde cualquier lugar**: No necesitas estar en tu PC
- ✅ **Gratis**: No requiere Railway Pro
- ✅ **Seguro**: Requiere autenticación de administrador
- ✅ **Instantáneo**: Descarga inmediata

## 📖 Cómo Usar

### Método 1: Desde el Navegador (Recomendado)

1. **Inicia sesión en Django Admin**
   ```
   https://nuve-sistema-production.up.railway.app/admin/
   ```
   - Usuario: tu superusuario
   - Contraseña: tu contraseña de admin

2. **Abre el endpoint de backup** (en una nueva pestaña)
   ```
   https://nuve-sistema-production.up.railway.app/api/backup/
   ```

3. **El archivo se descarga automáticamente**
   - Nombre: `backup_YYYYMMDD_HHMMSS.json`
   - Contiene todos los datos de la app `alm`

¡Listo! ✅

### Método 2: Desde Postman/Insomnia (Desarrollo)

1. **GET** `https://nuve-sistema-production.up.railway.app/api/backup/`

2. **Headers:**
   ```
   Authorization: Token TU_TOKEN_DE_API
   ```

3. **Response**: Descarga el archivo JSON

### Método 3: Desde cURL (Terminal)

```bash
# Primero obtén tu token de API (login en /admin o /api/login/)
TOKEN="tu_token_aqui"

# Descarga el backup
curl -H "Authorization: Token $TOKEN" \
     https://nuve-sistema-production.up.railway.app/api/backup/ \
     -o backup_$(date +%Y%m%d).json
```

## 🔒 Seguridad

- **Requiere autenticación**: Solo usuarios `staff` o `superuser`
- **Protección automática**: Django REST Framework valida permisos
- **Sin exposición pública**: El endpoint devuelve 401 si no estás autenticado

## 📊 Contenido del Backup

El archivo JSON incluye todos los datos de la app `alm`:

- ✅ Categorías
- ✅ Marcas
- ✅ Tallas
- ✅ Colores
- ✅ Productos
- ✅ ProductoVariantes
- ✅ Clientes
- ✅ Ventas
- ✅ DetalleVentas
- ✅ MovimientoInventario
- ✅ Proveedores
- ✅ Compras
- ✅ Promociones WhatsApp
- ✅ Envíos WhatsApp
- ✅ Pagos de Ventas

## 🔄 Restaurar un Backup

### Desde Local

1. **Copia el archivo** descargado a tu proyecto:
   ```bash
   cp ~/Downloads/backup_20251104_123456.json C:\Users\Tom\Documents\Django\proyecto01\backend\almacen\
   ```

2. **Ejecuta loaddata:**
   ```bash
   cd C:\Users\Tom\Documents\Django\proyecto01\backend\almacen
   python manage.py loaddata backup_20251104_123456.json
   ```

### Desde Railway

1. **Sube el archivo** al servidor (vía Railway shell o similar)

2. **Ejecuta loaddata:**
   ```bash
   railway run python backend/almacen/manage.py loaddata backup_20251104_123456.json
   ```

## 📅 Frecuencia Recomendada

- **Antes de cambios importantes**: Siempre haz backup antes de actualizaciones
- **Semanal**: Todos los lunes por la mañana
- **Antes de migraciones**: Antes de ejecutar `python manage.py migrate`
- **Después de carga masiva**: Después de importar muchos productos

## ⚠️ Notas Importantes

1. **Tamaño del archivo**: El backup crece con tus datos. Actualmente ~14KB, puede llegar a varios MB
2. **Formato JSON**: Es un formato legible y compatible con Django
3. **No incluye archivos multimedia**: Solo datos de la base de datos
4. **No incluye usuarios de Django admin**: Solo datos de la app `alm`

## 🆘 Solución de Problemas

### Error 401 (Unauthorized)

**Causa**: No estás autenticado como admin

**Solución**:
1. Inicia sesión en `/admin/` primero
2. Luego abre el endpoint `/api/backup/`

### Error 403 (Forbidden)

**Causa**: Tu usuario no es staff ni superuser

**Solución**:
1. Pide a un admin que te otorgue permisos de staff
2. O usa una cuenta de superusuario

### No se descarga nada

**Causa**: Problema con el navegador

**Solución**:
1. Verifica que las descargas estén habilitadas
2. Intenta con otro navegador
3. Usa cURL como alternativa

### Archivo vacío o muy pequeño

**Causa**: La base de datos no tiene datos

**Solución**:
1. Verifica que existan datos en `/admin/`
2. Revisa los logs de Railway para errores

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de Railway: `railway logs`
2. Verifica que el deployment esté activo
3. Confirma que tu usuario tenga permisos de staff

---

## Comparación con Otras Opciones

| Método | Facilidad | Costo | Automático | Desde Cualquier Lugar |
|--------|-----------|-------|------------|----------------------|
| **Backup Web** | ⭐⭐⭐⭐⭐ | Gratis | No | ✅ Sí |
| Scripts Manuales | ⭐⭐⭐ | Gratis | No | ❌ No |
| Railway Pro | ⭐⭐⭐⭐⭐ | $20/mes | ✅ Sí | ✅ Sí |

**Recomendación**: Usa el Backup Web para backups bajo demanda (antes de cambios importantes) y considera Railway Pro si necesitas backups automáticos diarios.
