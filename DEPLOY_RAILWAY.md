# 🚀 Guía de Deploy en Railway.app - Sistema Nuve

## ✅ Archivos ya preparados

Los siguientes archivos ya están listos:
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `Procfile` - Comando de inicio para Railway
- ✅ `runtime.txt` - Versión de Python
- ✅ `settings_prod.py` - Configuración de producción
- ✅ Frontend compilado en `frontend_build/dist/`

---

## 📋 Pasos para Deploy

### **1. Crear cuenta en Railway**

1. Ve a [railway.app](https://railway.app)
2. Haz clic en "Start a New Project"
3. Inicia sesión con GitHub

### **2. Subir código a GitHub**

Desde tu computadora:

```bash
# Ir a la carpeta del proyecto
cd C:\Users\Tom\Documents\Django\proyecto01

# Inicializar git (si no lo has hecho)
git init

# Crear archivo .gitignore
echo "venv/" > .gitignore
echo "venv3/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "db.sqlite3" >> .gitignore
echo "node_modules/" >> .gitignore
echo ".DS_Store" >> .gitignore

# Agregar archivos
git add .
git commit -m "Deploy Nuve a Railway"

# Crear repositorio en GitHub y subir
# (Sigue las instrucciones de GitHub para crear nuevo repositorio)
git remote add origin https://github.com/TU_USUARIO/nuve-sistema.git
git branch -M main
git push -u origin main
```

### **3. Deploy en Railway**

1. **En Railway Dashboard:**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio `nuve-sistema`

2. **Configurar Backend (Django):**
   - Railway detectará automáticamente que es Python
   - Click en "Add Variables"
   - Agregar estas variables de entorno:

```
DJANGO_SETTINGS_MODULE=almacen.settings_prod
SECRET_KEY=genera-una-clave-secreta-aqui-muy-larga
DEBUG=False
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=https://tu-dominio-railway.up.railway.app
```

3. **Agregar Base de Datos PostgreSQL:**
   - En el mismo proyecto, click en "New"
   - Selecciona "Database" → "Add PostgreSQL"
   - Railway automáticamente creará la variable `DATABASE_URL`

4. **Ejecutar Migraciones:**
   - En Railway, ve a tu servicio Django
   - Click en "Settings" → "Deploy"
   - Espera a que termine el deploy
   - Luego ve a "Settings" → "Custom Start Command" (opcional)
   - O ejecuta desde la terminal de Railway:

```bash
python backend/almacen/manage.py migrate --settings=almacen.settings_prod
python backend/almacen/manage.py createsuperuser --settings=almacen.settings_prod
python backend/almacen/manage.py collectstatic --no-input --settings=almacen.settings_prod
```

### **4. Deploy Frontend (Opción fácil - Vercel)**

El frontend ya está compilado en `frontend_build/dist/`

**Opción A - Vercel (Recomendado):**

1. Ve a [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Conecta tu repositorio GitHub
4. Configuración:
   - **Framework Preset:** Vue.js
   - **Root Directory:** `frontend_build`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Variables de entorno:
   ```
   VUE_APP_API_URL=https://tu-backend-railway.up.railway.app
   ```
6. Click "Deploy"

**Opción B - Netlify:**

1. Ve a [netlify.com](https://netlify.com)
2. Arrastra la carpeta `frontend_build/dist/` directamente
3. ¡Listo!

**Opción C - Railway (ambos en mismo lugar):**

1. Sirve el frontend desde Django
2. Copia `frontend_build/dist/*` a `backend/almacen/staticfiles/`
3. Configura Django para servir archivos estáticos

---

## 🔧 Configuración post-deploy

### **1. Actualizar URLs del Frontend**

Edita `frontend_build/src/services/api.js`:

```javascript
const API_URL = process.env.VUE_APP_API_URL || 'https://tu-backend-railway.up.railway.app/api'
```

### **2. Crear superusuario**

Desde la terminal de Railway:

```bash
python manage.py createsuperuser
```

### **3. Cargar datos iniciales**

```bash
python manage.py loaddata initial_data.json
```

---

## 🌐 URLs finales

- **Backend API:** `https://nuve-backend-production.up.railway.app/api/`
- **Django Admin:** `https://nuve-backend-production.up.railway.app/admin/`
- **Frontend:** `https://nuve.vercel.app` (si usas Vercel)

---

## 🐛 Solución de problemas

### Error: "Application failed to respond"
- Verifica que `Procfile` esté correcto
- Revisa logs en Railway Dashboard

### Error de base de datos
- Asegúrate de que `DATABASE_URL` está configurado
- Ejecuta migraciones

### Error 500
- Cambia `DEBUG=True` temporalmente para ver el error
- Revisa logs en Railway

### Frontend no conecta con backend
- Verifica CORS en settings_prod.py
- Asegúrate de que la URL del API sea correcta

---

## 💰 Costos

- **Railway:** $5/mes gratis, luego ~$5-10/mes según uso
- **Vercel:** Gratis para proyectos personales
- **Total:** ~$0-10/mes

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway Dashboard
2. Verifica todas las variables de entorno
3. Asegúrate de que las migraciones se ejecutaron

¡Listo! Tu sistema Nuve estará en línea 24/7 🎉
