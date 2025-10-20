# Configuración de Twilio WhatsApp para Promociones

## Descripción

El sistema ahora incluye funcionalidad para enviar mensajes promocionales masivos a clientes vía WhatsApp usando la API de Twilio. Esta guía explica cómo configurar Twilio y las variables de entorno necesarias.

---

## 1. Crear Cuenta en Twilio

### Paso 1: Registro
1. Ir a [https://www.twilio.com/](https://www.twilio.com/)
2. Hacer clic en "Sign up" (Registrarse)
3. Completar el formulario con tus datos
4. Verificar tu correo electrónico y número de teléfono

### Paso 2: Cuenta de Prueba (Trial)
- Twilio ofrece una cuenta de prueba gratuita con:
  - Crédito inicial de $15 USD
  - Funcionalidad completa para testing
  - Limitaciones: solo puedes enviar a números verificados en tu cuenta

### Paso 3: Upgrade a Cuenta de Producción (Cuando estés listo)
- Para enviar a cualquier número, necesitas:
  1. Agregar tarjeta de crédito
  2. Completar verificación de negocio
  3. Costos aproximados:
     - WhatsApp: ~$0.005 USD por mensaje (varía por país)
     - Número de teléfono: ~$1 USD/mes

---

## 2. Configurar WhatsApp en Twilio

### Paso 1: Acceder al Sandbox de WhatsApp (Pruebas)
1. En el dashboard de Twilio, ir a **Messaging** > **Try it out** > **Send a WhatsApp message**
2. Encontrarás un número de WhatsApp de Twilio (ej: `+1 415 523 8886`)
3. Para probar, envía un mensaje desde tu WhatsApp personal al número indicado con el código que te proporcionan (ej: `join example-word`)

### Paso 2: Configurar WhatsApp para Producción (Opcional)
Para producción, necesitas:
1. **Solicitar un número dedicado de WhatsApp Business**:
   - Ir a **Messaging** > **Senders** > **WhatsApp senders**
   - Clic en "Request to enable your Twilio number for WhatsApp"
   - Seguir el proceso de verificación de Facebook Business

2. **Crear Plantillas de Mensajes (Message Templates)**:
   - Los mensajes promocionales requieren aprobación previa de WhatsApp
   - Ir a **Messaging** > **WhatsApp** > **Senders** > **Content Templates**
   - Crear y enviar plantillas para aprobación (pueden tardar 24-48 horas)

---

## 3. Obtener Credenciales de Twilio

### Paso 1: Account SID y Auth Token
1. En el dashboard de Twilio, ir a **Account** > **Keys & Credentials**
2. Copiar:
   - **Account SID**: Identificador único de tu cuenta
   - **Auth Token**: Token de autenticación (mantener secreto)

### Paso 2: Número de WhatsApp
- **Para pruebas (Sandbox)**: Usar el número proporcionado en el sandbox (ej: `+14155238886`)
- **Para producción**: Usar tu número de WhatsApp verificado

---

## 4. Configurar Variables de Entorno en Django

### En Desarrollo (local)

Crear archivo `.env` en `backend/almacen/`:

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
```

Instalar python-decouple:
```bash
pip install python-decouple
```

Actualizar `settings.py`:
```python
from decouple import config

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER', default='')
```

### En Producción (Railway)

1. Ir al proyecto en Railway
2. Ir a **Variables** (ícono de llave)
3. Agregar las siguientes variables:
   - `TWILIO_ACCOUNT_SID`: Tu Account SID de Twilio
   - `TWILIO_AUTH_TOKEN`: Tu Auth Token de Twilio
   - `TWILIO_WHATSAPP_NUMBER`: Tu número de WhatsApp (con formato +1234567890)

4. Hacer redeploy del proyecto para aplicar cambios

---

## 5. Formato de Números de Teléfono

### Importante
Los números de teléfono de los clientes deben estar en formato internacional:

- **Colombia**: `+573001234567` (incluir +57)
- **Estados Unidos**: `+11234567890` (incluir +1)
- **México**: `+521234567890` (incluir +52)

### En la Base de Datos
Asegúrate de que el campo `telefono` del modelo `Cliente` tenga el formato correcto:

```python
# Ejemplo de formato correcto en BD
cliente.telefono = "+573001234567"  # ✅ Correcto
cliente.telefono = "3001234567"     # ❌ Incorrecto (falta código de país)
cliente.telefono = "300-123-4567"   # ❌ Incorrecto (tiene guiones)
```

---

## 6. Probar el Sistema

### Paso 1: Verificar Configuración
1. Asegúrate de tener las variables de entorno configuradas
2. Reinicia el servidor Django

### Paso 2: Agregar Clientes de Prueba
1. En el admin de Django o desde el frontend, crear un cliente
2. Asegúrate de agregar el número de teléfono en formato internacional (ej: `+573001234567`)

### Paso 3: Crear Promoción
1. Ir a `/promociones-whatsapp` en el frontend
2. Hacer clic en "Nueva Promoción"
3. Completar:
   - **Título**: "Prueba de Promoción"
   - **Mensaje**: "Hola {nombre}, esta es una promoción de prueba. ¡Saludos!"
4. Guardar (se crea en estado BORRADOR)

### Paso 4: Enviar Promoción
1. En la tabla de promociones, hacer clic en el ícono de enviar (✉️)
2. Confirmar el envío
3. El sistema:
   - Cambia estado a ENVIANDO
   - Envía mensajes a todos los clientes con teléfono
   - Implementa rate limiting (5 mensajes por minuto)
   - Cambia estado a ENVIADO cuando termina
   - Registra estadísticas (enviados/fallidos)

### Paso 5: Verificar Resultados
1. Hacer clic en el ícono de ojo (👁️) para ver detalles
2. Revisar:
   - Total de destinatarios
   - Mensajes enviados exitosamente
   - Mensajes fallidos (si hay)
   - Lista detallada de cada envío

---

## 7. Limitaciones y Consideraciones

### Rate Limiting
- El sistema implementa espera de 12 segundos entre mensajes (5 por minuto)
- Esto evita que Twilio bloquee la cuenta por spam
- Para 100 clientes, el envío toma ~20 minutos

### Sandbox vs Producción

**Sandbox (Pruebas)**:
- ✅ Gratis con crédito inicial
- ❌ Solo envía a números verificados en tu cuenta
- ❌ Los destinatarios deben enviar "join code" primero
- ❌ Mensaje incluye "Sent from your Twilio trial account"

**Producción**:
- ✅ Envía a cualquier número de WhatsApp
- ✅ Mensajes sin marca de "trial account"
- ❌ Requiere pago
- ❌ Mensajes promocionales requieren plantillas aprobadas

### Costos Estimados (Producción)
- **Mensaje WhatsApp**: ~$0.005 USD cada uno
- **100 clientes**: ~$0.50 USD
- **1000 clientes**: ~$5.00 USD
- **Número de teléfono**: ~$1 USD/mes

---

## 8. Troubleshooting

### Error: "Twilio no está configurado"
**Causa**: Faltan variables de entorno
**Solución**:
- Verificar que `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, y `TWILIO_WHATSAPP_NUMBER` estén configuradas
- Reiniciar servidor Django

### Error: "No hay clientes con teléfono registrado"
**Causa**: No hay clientes con campo `telefono` lleno
**Solución**:
- Agregar números de teléfono a los clientes existentes
- Asegurarse de usar formato internacional (+código_país + número)

### Error: "Unable to create record"
**Causa**: Número de teléfono en formato incorrecto o destinatario no verificado (sandbox)
**Solución**:
- Verificar formato de número: `+573001234567`
- Si usas sandbox, verificar que el destinatario haya enviado "join code" primero

### Mensajes marcados como FALLIDO
**Causa**: Puede ser número inválido, WhatsApp no instalado, o bloqueado
**Solución**:
- Verificar número de teléfono del cliente
- Confirmar que el cliente tiene WhatsApp instalado
- Revisar `mensaje_error` en detalles del envío

---

## 9. Migración de Base de Datos

No olvides crear y aplicar las migraciones para los nuevos modelos:

```bash
cd backend/almacen
python manage.py makemigrations
python manage.py migrate
```

---

## 10. Recursos Adicionales

- **Documentación Twilio WhatsApp**: https://www.twilio.com/docs/whatsapp
- **Twilio Console**: https://console.twilio.com/
- **Pricing**: https://www.twilio.com/whatsapp/pricing
- **Sandbox Testing**: https://www.twilio.com/docs/whatsapp/sandbox

---

## 11. Endpoints API Creados

### Listar Promociones
```
GET /api/promociones-whatsapp/
```

### Crear Promoción
```
POST /api/promociones-whatsapp/
Body: {
  "titulo": "Título de la promoción",
  "mensaje": "Hola {nombre}, mensaje aquí..."
}
```

### Enviar Promoción
```
POST /api/promociones-whatsapp/{id}/enviar_promocion/
```

### Ver Detalles de Promoción
```
GET /api/promociones-whatsapp/{id}/
```

### Listar Envíos Individuales
```
GET /api/envios-whatsapp/
```

---

## 12. Flujo Completo de Uso

1. **Configurar Twilio** (una sola vez)
   - Crear cuenta en Twilio
   - Configurar WhatsApp sandbox o número de producción
   - Agregar variables de entorno

2. **Preparar Clientes** (continuo)
   - Asegurarse de que los clientes tengan teléfonos registrados
   - Formato internacional: +código_país + número

3. **Crear Promoción** (cuando sea necesario)
   - Ir a "Promociones WhatsApp" en el frontend
   - Crear nueva promoción con título y mensaje
   - Usar {nombre} para personalizar

4. **Enviar Promoción**
   - Hacer clic en botón enviar
   - El sistema procesa automáticamente
   - Ver estadísticas en tiempo real

5. **Monitorear Resultados**
   - Ver detalles de cada promoción
   - Revisar envíos exitosos y fallidos
   - Identificar problemas si hay mensajes fallidos

---

## Soporte

Si tienes problemas con la configuración:
1. Verificar logs del servidor Django
2. Revisar console de Twilio: https://console.twilio.com/
3. Consultar documentación de Twilio WhatsApp
