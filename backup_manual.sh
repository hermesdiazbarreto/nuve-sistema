#!/bin/bash
# Script de backup manual para Linux/Mac/Git Bash
# Ejecuta este script cuando quieras hacer un backup de la base de datos Railway

echo "========================================"
echo "  Backup Manual de Base de Datos"
echo "========================================"
echo

# Crear directorio de backups si no existe
mkdir -p backups

# Generar nombre de archivo con fecha y hora
BACKUP_FILE="backups/backup_$(date +%Y%m%d_%H%M%S).json"

echo "Creando backup en: ${BACKUP_FILE}"
echo

# Ejecutar dumpdata en Railway
railway run python backend/almacen/manage.py dumpdata alm --indent 2 > "${BACKUP_FILE}"

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "  BACKUP CREADO EXITOSAMENTE!"
    echo "========================================"
    echo "Archivo: ${BACKUP_FILE}"
    ls -lh "${BACKUP_FILE}"
    echo
    echo "Para restaurar este backup:"
    echo "railway run python backend/almacen/manage.py loaddata ${BACKUP_FILE}"
else
    echo
    echo "========================================"
    echo "  ERROR AL CREAR BACKUP"
    echo "========================================"
    echo "Verifica que:"
    echo "1. Railway CLI esté instalado"
    echo "2. Hayas hecho login con 'railway login'"
    echo "3. El proyecto esté vinculado con 'railway link'"
    exit 1
fi

echo
