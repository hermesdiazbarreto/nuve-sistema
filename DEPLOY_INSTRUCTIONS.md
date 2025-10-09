# Instrucciones de Despliegue - Soft Delete

## ✅ Backend (Railway) - COMPLETADO

Los cambios ya están en GitHub y Railway los detectará automáticamente:

### Verificar Despliegue en Railway:

1. Ve a: https://railway.app/dashboard
2. Selecciona tu proyecto
3. Verás un nuevo despliegue en curso con el commit: "Implementar soft delete para productos"
4. Espera a que termine (muestra ✓ verde)
5. Railway ejecutará automáticamente:
   - `python manage.py migrate` (aplicará las migraciones del soft delete)
   - `python manage.py collectstatic`
   - Reiniciará Gunicorn

### URL del Backend:
```
https://nuve-sistema-production.up.railway.app/api/
```

### Verificar que funcionó:
```bash
# Probar endpoint de productos
curl https://nuve-sistema-production.up.railway.app/api/productos/

# Probar endpoint de productos eliminados
curl https://nuve-sistema-production.up.railway.app/api/productos/?solo_eliminados=true
```

---

## 🎨 Frontend (Vercel) - REQUIERE ACCIÓN

### Opción 1: Despliegue Automático desde GitHub (Recomendado)

Si tu proyecto ya está conectado a Vercel:

1. Ve a: https://vercel.com/dashboard
2. Selecciona tu proyecto
3. Vercel detectará automáticamente el push a `main`
4. El despliegue comenzará automáticamente
5. Espera a que termine (1-2 minutos)

### Opción 2: Despliegue Manual desde Vercel

Si el proyecto NO está conectado:

1. Ve a: https://vercel.com/new
2. Importa el repositorio: `hermesdiazbarreto/nuve-sistema`
3. Configura el proyecto:
   - **Framework Preset**: Vue.js
   - **Root Directory**: `frontend_build`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Configura variables de entorno:
   - `VUE_APP_API_URL` = `https://nuve-sistema-production.up.railway.app/api`
5. Click en "Deploy"

### Opción 3: Usar Vercel CLI

```bash
# Instalar Vercel CLI globalmente
npm install -g vercel

# Navegar al frontend
cd C:\Users\Tom\Documents\Django\proyecto01\frontend_build

# Login a Vercel
vercel login

# Desplegar a producción
vercel --prod
```

Durante el despliegue, responde:
- **Set up and deploy?** → Yes
- **Which scope?** → Tu cuenta
- **Link to existing project?** → Yes (si existe) o No (si es nuevo)
- **Project name?** → nuve-sistema-frontend (o el nombre que prefieras)
- **Override settings?** → No

---

## 🔧 Configuración de Variables de Entorno

### Railway (Backend)
Verifica que estas variables estén configuradas:

```env
DJANGO_SETTINGS_MODULE=almacen.settings
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,http://localhost:8080
DATABASE_URL=(automático por Railway)
```

### Vercel (Frontend)
Configura esta variable:

```env
VUE_APP_API_URL=https://nuve-sistema-production.up.railway.app/api
```

**Configurar en Vercel:**
1. Ve a tu proyecto en Vercel
2. Settings → Environment Variables
3. Agrega `VUE_APP_API_URL` con el valor del backend
4. Redeploy si es necesario

---

## 📋 Verificación Post-Despliegue

### 1. Verificar Backend (Railway)

```bash
# Productos activos
curl https://nuve-sistema-production.up.railway.app/api/productos/

# Productos eliminados
curl https://nuve-sistema-production.up.railway.app/api/productos/?solo_eliminados=true
```

### 2. Verificar Frontend (Vercel)

1. Abre tu app en Vercel: `https://tu-proyecto.vercel.app`
2. Ve a Productos
3. Verifica que aparezca el botón "🗑️ Ver Eliminados"
4. Haz una prueba:
   - Elimina un producto
   - Ve a "Ver Eliminados"
   - Verifica que aparezca
   - Restáuralo
   - Verifica que vuelva a la lista principal

### 3. Probar Flujo Completo

**Eliminar:**
```
1. Login → Dashboard → Productos
2. Click en 🗑️ de cualquier producto
3. Confirmar eliminación
4. Verificar que desaparece de la lista
```

**Ver eliminados:**
```
1. Click en "🗑️ Ver Eliminados"
2. Verificar que el producto aparece
3. Verificar fecha y usuario de eliminación
```

**Restaurar:**
```
1. En lista de eliminados, click en "♻️ Restaurar"
2. Confirmar restauración
3. Verificar que desaparece de eliminados
4. Volver a Productos
5. Verificar que aparece en la lista principal
```

---

## 🐛 Troubleshooting

### Backend: Error 500 en endpoints

**Problema:** Las migraciones no se ejecutaron

**Solución:**
```bash
# Acceder a Railway CLI
railway login
railway link
railway run python backend/almacen/manage.py migrate
```

### Frontend: No aparece botón "Ver Eliminados"

**Problema:** Código antiguo en caché de Vercel

**Solución:**
1. Ve a Vercel Dashboard
2. Deployments → Latest deployment
3. Click en "..." → Redeploy
4. Marca "Use existing Build Cache" como OFF
5. Click "Redeploy"

### CORS Error en navegador

**Problema:** El backend no permite peticiones del frontend

**Solución en Railway:**
1. Ve a Variables de entorno
2. Actualiza `CORS_ALLOWED_ORIGINS`:
   ```
   https://tu-frontend.vercel.app,https://tu-frontend-*.vercel.app,http://localhost:8080
   ```
3. Redeploy

### Error 404 en rutas del frontend

**Problema:** `vercel.json` no está configurado correctamente

**Solución:**
El archivo ya está correcto, pero verifica:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## 📊 Monitoreo

### Railway Logs
```bash
railway logs
```

### Vercel Logs
1. Ve a tu proyecto en Vercel
2. Click en el deployment
3. Ve a "Functions" o "Runtime Logs"

---

## ✅ Checklist de Despliegue

Backend (Railway):
- [x] Código pushed a GitHub
- [ ] Railway detectó el push
- [ ] Migraciones ejecutadas exitosamente
- [ ] Servicio reiniciado sin errores
- [ ] Endpoints responden correctamente

Frontend (Vercel):
- [ ] Conectado a GitHub (o desplegado manualmente)
- [ ] Variable `VUE_APP_API_URL` configurada
- [ ] Build exitoso
- [ ] Rutas funcionan correctamente
- [ ] Botón "Ver Eliminados" visible
- [ ] API calls funcionan (sin CORS errors)

Funcionalidad:
- [ ] Eliminar producto funciona
- [ ] Ver productos eliminados funciona
- [ ] Restaurar producto funciona
- [ ] Auditoría (fecha/usuario) se muestra correctamente

---

## 🎯 Próximos Pasos

Después del despliegue:

1. **Prueba en producción**: Realiza el flujo completo de soft delete
2. **Documenta URLs**: Anota las URLs finales de Railway y Vercel
3. **Monitorea logs**: Revisa logs por 24h para detectar errores
4. **Backup BD**: Railway hace backup automático, pero verifica que esté activo
5. **Notifica usuarios**: Si hay usuarios existentes, avísales de la nueva funcionalidad

---

## 📞 Soporte

Si hay problemas:
1. Revisa Railway logs: `railway logs`
2. Revisa Vercel deployment logs
3. Verifica variables de entorno
4. Verifica que las migraciones se ejecutaron: consulta la tabla `alm_producto` en PostgreSQL

¡Listo para desplegar! 🚀
