# Configuración de Backups Automáticos

Este documento explica cómo configurar los backups automáticos de la base de datos usando GitHub Actions.

## Configuración Inicial

### 1. Obtener Railway Token

1. Ve a https://railway.app/account/tokens
2. Haz clic en "Create Token"
3. Dale un nombre descriptivo (ej: "GitHub Actions Backup")
4. Copia el token generado (solo se muestra una vez)

### 2. Obtener Railway Project ID

Opción A - Desde la terminal:
```bash
cd C:\Users\Tom\Documents\Django\proyecto01
railway status
```
Busca la línea que dice `Project ID: ...`

Opción B - Desde el dashboard de Railway:
1. Ve a tu proyecto en https://railway.app
2. En Settings, encontrarás el Project ID

### 3. Configurar Secretos en GitHub

1. Ve a tu repositorio en GitHub
2. Navega a: **Settings** → **Secrets and variables** → **Actions**
3. Haz clic en **"New repository secret"**
4. Añade estos dos secretos:

   **Secreto 1:**
   - Name: `RAILWAY_TOKEN`
   - Value: [pega el token que obtuviste en el paso 1]

   **Secreto 2:**
   - Name: `RAILWAY_PROJECT_ID`
   - Value: [pega el Project ID que obtuviste en el paso 2]

### 4. Crear directorio de backups

El workflow creará automáticamente el directorio `backups/` en tu repositorio.

### 5. (Opcional) Ignorar backups locales en .gitignore

Si quieres evitar que los backups locales se suban al repositorio:

```bash
echo "backup_*.json" >> .gitignore
```

## Cómo Funciona

### Ejecución Automática
- Se ejecuta **diariamente a las 3:00 AM UTC**
- Crea un backup JSON usando `dumpdata`
- Guarda el backup en el directorio `backups/` del repositorio
- Sube el backup como artifact de GitHub Actions (disponible por 30 días)
- Mantiene solo los últimos 7 backups en el repositorio

### Ejecución Manual

Puedes ejecutar el backup manualmente cuando quieras:

1. Ve a tu repositorio en GitHub
2. Navega a: **Actions** → **Backup Database**
3. Haz clic en **"Run workflow"** → **"Run workflow"**

## Restaurar desde Backup

### Desde GitHub Artifacts (últimos 30 días)

1. Ve a **Actions** en GitHub
2. Selecciona el workflow **"Backup Database"**
3. Haz clic en la ejecución que quieres restaurar
4. Descarga el artifact `database-backup-XXX`
5. Descomprime el archivo ZIP y obtén el JSON

### Desde el repositorio (últimos 7 días)

Los backups están en el directorio `backups/` del repositorio.

### Restaurar el backup en Railway

```bash
# Opción 1: Desde tu máquina local con Railway CLI
railway run python backend/almacen/manage.py loaddata backup_YYYYMMDD_HHMMSS.json

# Opción 2: Subir el archivo y ejecutar en Railway shell
railway run python backend/almacen/manage.py shell
# Luego usar loaddata manualmente
```

## Verificar que funciona

Después de configurar los secretos:

1. Ve a **Actions** en GitHub
2. Selecciona **"Backup Database"**
3. Haz clic en **"Run workflow"** (esquina derecha)
4. Espera unos minutos
5. Verifica que el workflow se completó exitosamente (check verde)
6. Descarga el artifact para verificar que el backup contiene datos

## Solución de Problemas

### Error: "Unauthorized"
- Verifica que `RAILWAY_TOKEN` esté correctamente configurado en GitHub Secrets
- El token debe tener permisos de lectura en el proyecto

### Error: "Project not found"
- Verifica que `RAILWAY_PROJECT_ID` sea correcto
- Asegúrate de tener acceso al proyecto en Railway

### Backup vacío o muy pequeño
- Verifica que la base de datos de Railway tenga datos
- Ejecuta `railway run python manage.py shell` y verifica las tablas

### El workflow no se ejecuta automáticamente
- Asegúrate de que el archivo esté en `.github/workflows/`
- Verifica que hayas hecho commit y push del workflow
- GitHub Actions debe estar habilitado en tu repositorio (Settings → Actions)

## Backup Manual Alternativo

Si prefieres hacer backups manuales, usa este comando:

```bash
# Desde Windows
cd C:\Users\Tom\Documents\Django\proyecto01
railway run python backend/almacen/manage.py dumpdata alm --indent 2 > backup_%date:~-4%%date:~3,2%%date:~0,2%.json
```

O usa el script `backup_manual.bat` incluido en el proyecto.
