# Instrucciones para Corregir Venta en Producción (Railway)

## El Problema
La venta de **557,000 con descuento de 5,000 (total: 552,000)** está marcada incorrectamente como **ABONO** cuando debería estar **PAGADA**.

## La Solución
Ya he pusheado el fix del frontend y el comando de corrección al repositorio. Railway se está redespliegando automáticamente.

---

## Opción 1: Usar Railway CLI (Recomendado)

### Paso 1: Esperar el redespliegue
Espera a que Railway termine de redesplegar (verifica en https://railway.app)

### Paso 2: Ejecutar el comando
```bash
cd C:\Users\Tom\Documents\Django\proyecto01
railway login
railway link
railway run python backend/almacen/manage.py corregir_ventas
```

---

## Opción 2: Usar Railway Dashboard Web

### Paso 1: Acceder al proyecto
1. Ve a https://railway.app
2. Abre tu proyecto del backend
3. Ve a la pestaña "Settings" o "Variables"

### Paso 2: Usar la consola de Railway
1. En el dashboard, busca la opción "Shell" o "Terminal"
2. Ejecuta:
```bash
python manage.py corregir_ventas
```

---

## Opción 3: Django Admin (Manual)

### Paso 1: Acceder al admin
1. Ve a tu URL de Railway: `https://tu-backend-railway.up.railway.app/admin`
2. Inicia sesión con tu superusuario

### Paso 2: Buscar la venta
1. Ve a "Ventas" en el admin
2. Busca la venta con:
   - Total: 552,000.00
   - Estado: ABONO
   - Descuento: 5,000.00

### Paso 3: Corregir manualmente
Edita la venta y cambia:
- **Estado**: PAGADO
- **Monto abonado**: 552000.00
- **Saldo pendiente**: 0.00

Guarda los cambios.

---

## Verificación

Después de corregir, verifica que:
1. La venta ahora aparece como **PAGADO** en la lista de ventas
2. El **Saldo pendiente** es **0.00**
3. Ya no aparece en el listado de "Pendientes"

---

## ¿Qué se corrigió?

### Frontend (NuevaVenta.vue)
- Ahora envía `monto_abonado = 0` para ventas pagadas completamente
- Solo abonos parciales tendrán `monto_abonado > 0`

### Backend (Comando Django)
- Comando `python manage.py corregir_ventas`
- Busca ventas ABONO donde `monto_abonado >= total`
- Las marca como PAGADO automáticamente

---

## Contacto
Si tienes problemas, avísame y te ayudo a ejecutar el comando.
