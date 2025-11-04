@echo off
REM Script de backup manual para Windows
REM Ejecuta este script cuando quieras hacer un backup de la base de datos Railway

echo ========================================
echo   Backup Manual de Base de Datos
echo ========================================
echo.

REM Crear directorio de backups si no existe
if not exist "backups" mkdir backups

REM Generar nombre de archivo con fecha y hora
set FECHA=%date:~-4%%date:~3,2%%date:~0,2%
set HORA=%time:~0,2%%time:~3,2%%time:~6,2%
set HORA=%HORA: =0%
set BACKUP_FILE=backups\backup_%FECHA%_%HORA%.json

echo Creando backup en: %BACKUP_FILE%
echo.

REM Ejecutar dumpdata en Railway
railway run python backend/almacen/manage.py dumpdata alm --indent 2 > %BACKUP_FILE%

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   BACKUP CREADO EXITOSAMENTE!
    echo ========================================
    echo Archivo: %BACKUP_FILE%
    dir %BACKUP_FILE%
    echo.
    echo Para restaurar este backup:
    echo railway run python backend/almacen/manage.py loaddata %BACKUP_FILE%
) else (
    echo.
    echo ========================================
    echo   ERROR AL CREAR BACKUP
    echo ========================================
    echo Verifica que:
    echo 1. Railway CLI este instalado
    echo 2. Hayas hecho login con 'railway login'
    echo 3. El proyecto este vinculado con 'railway link'
)

echo.
pause
