<template>
  <v-dialog v-model="dialog" max-width="600px" persistent>
    <v-card>
      <v-card-title class="text-h5">
        <v-icon left>mdi-qrcode-scan</v-icon>
        Escanear Código QR
        <v-spacer></v-spacer>
        <v-btn icon @click="cerrarScanner">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text>
        <v-alert v-if="error" type="error" dismissible @click:close="error = null" class="mb-4">
          {{ error }}
        </v-alert>

        <v-alert v-if="success" type="success" dismissible @click:close="success = null" class="mb-4">
          {{ success }}
        </v-alert>

        <div v-if="!cameraError">
          <div id="qr-reader" style="width: 100%;"></div>
          <p class="text-center mt-3 text-caption grey--text">
            Coloca el código QR frente a la cámara
          </p>
        </div>

        <v-alert v-else type="warning" class="mb-4" style="white-space: pre-line;">
          {{ cameraError }}
        </v-alert>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" text @click="cerrarScanner">
          Cancelar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { Html5Qrcode } from 'html5-qrcode';

export default {
  name: 'QrScannerModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'codigo-escaneado'],
  data() {
    return {
      html5QrCode: null,
      error: null,
      success: null,
      cameraError: null,
      scanning: false,
      procesandoEscaneo: false // Bandera para evitar escaneos duplicados
    };
  },
  computed: {
    dialog: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit('update:modelValue', val);
      }
    }
  },
  watch: {
    dialog(newVal) {
      if (newVal) {
        this.iniciarScanner();
      } else {
        this.detenerScanner();
      }
    }
  },
  methods: {
    async iniciarScanner() {
      this.error = null;
      this.cameraError = null;
      this.success = null;
      this.procesandoEscaneo = false; // Resetear bandera al iniciar

      try {
        // Verificar si se está usando HTTPS (requerido para cámara)
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const isHttps = window.location.protocol === 'https:';

        if (!isLocalhost && !isHttps) {
          this.cameraError = '⚠️ HTTPS REQUERIDO: Tu navegador solo permite acceso a la cámara en sitios seguros (HTTPS). Contacta al administrador del sistema para habilitar HTTPS.';
          return;
        }

        // Esperar a que el DOM esté listo
        await this.$nextTick();

        // Verificar si el elemento existe
        const element = document.getElementById('qr-reader');
        if (!element) {
          console.error('Elemento qr-reader no encontrado');
          return;
        }

        // Verificar si el navegador soporta getUserMedia
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          this.cameraError = 'Tu navegador no soporta acceso a la cámara. Usa Chrome, Safari o Firefox actualizado.';
          return;
        }

        // Solicitar permisos de cámara primero
        try {
          await navigator.mediaDevices.getUserMedia({ video: true });
        } catch (permErr) {
          console.error('Error de permisos:', permErr);

          // Manejar errores específicos de permisos
          if (permErr.name === 'NotAllowedError' || permErr.name === 'PermissionDeniedError') {
            this.cameraError = '📷 PERMISO DENEGADO: Permite el acceso a la cámara en tu navegador:\n\n• Chrome/Android: Toca el candado 🔒 en la barra de direcciones → Permisos → Cámara → Permitir\n• Safari/iOS: Ajustes → Safari → Cámara → Permitir\n\nLuego recarga esta página.';
          } else if (permErr.name === 'NotFoundError') {
            this.cameraError = '📷 SIN CÁMARA: No se detectó ninguna cámara en tu dispositivo.';
          } else if (permErr.name === 'NotReadableError') {
            this.cameraError = '📷 CÁMARA EN USO: Otra aplicación está usando la cámara. Cierra otras apps y vuelve a intentar.';
          } else if (permErr.name === 'OverconstrainedError') {
            this.cameraError = '📷 CÁMARA NO COMPATIBLE: Tu cámara no cumple con los requisitos mínimos.';
          } else if (permErr.name === 'SecurityError') {
            this.cameraError = '🔒 ERROR DE SEGURIDAD: El acceso a la cámara fue bloqueado por políticas de seguridad del navegador. Asegúrate de estar en HTTPS.';
          } else {
            this.cameraError = `📷 ERROR: ${permErr.message || permErr.name || 'No se pudo acceder a la cámara'}. Intenta:\n\n1. Recargar la página\n2. Verificar permisos de cámara\n3. Cerrar otras apps que usen la cámara\n4. Reiniciar el navegador`;
          }
          return;
        }

        this.html5QrCode = new Html5Qrcode('qr-reader');

        const config = {
          fps: 10,
          qrbox: { width: 250, height: 250 },
          aspectRatio: 1.0
        };

        // Intentar con cámara trasera primero, si falla usar cualquiera
        try {
          await this.html5QrCode.start(
            { facingMode: 'environment' }, // Cámara trasera
            config,
            this.onScanSuccess,
            this.onScanFailure
          );
        } catch (backCamErr) {
          // Si falla la cámara trasera, intentar con cualquier cámara
          await this.html5QrCode.start(
            { facingMode: 'user' }, // Cámara frontal
            config,
            this.onScanSuccess,
            this.onScanFailure
          );
        }

        this.scanning = true;
      } catch (err) {
        console.error('Error al iniciar scanner:', err);

        // Manejar errores específicos del scanner
        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
          this.cameraError = '📷 PERMISO DENEGADO: Permite el acceso a la cámara:\n\n• Android: Toca el candado 🔒 → Permisos → Cámara → Permitir\n• iPhone: Ajustes → Safari → Cámara → Permitir\n\nLuego recarga esta página.';
        } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
          this.cameraError = '📷 SIN CÁMARA: No se detectó ninguna cámara en tu dispositivo.';
        } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
          this.cameraError = '📷 CÁMARA EN USO: Otra app está usando la cámara. Cierra otras apps y vuelve a intentar.';
        } else if (err.name === 'OverconstrainedError') {
          this.cameraError = '📷 CÁMARA NO COMPATIBLE: Tu cámara no soporta la configuración requerida. Intenta con otro dispositivo.';
        } else if (err.name === 'SecurityError') {
          this.cameraError = '🔒 ERROR DE SEGURIDAD:\n\n1. Verifica que la URL use HTTPS (no HTTP)\n2. Limpia la caché del navegador\n3. Verifica los permisos de la cámara\n\nSi el problema persiste, contacta al administrador.';
        } else if (err.name === 'AbortError') {
          this.cameraError = '⚠️ INICIALIZACIÓN INTERRUMPIDA: El proceso fue cancelado. Vuelve a intentar.';
        } else if (err.name === 'TypeError') {
          this.cameraError = '⚠️ ERROR DE CONFIGURACIÓN: Problema interno del scanner. Recarga la página.';
        } else {
          // Error desconocido - dar información detallada
          const errorMsg = err.message || err.toString() || 'Error desconocido';
          this.cameraError = `📷 ERROR AL INICIAR CÁMARA:\n\n${errorMsg}\n\n✅ Soluciones:\n1. Recarga la página\n2. Verifica permisos de cámara\n3. Cierra otras apps\n4. Usa HTTPS (no HTTP)\n5. Prueba otro navegador\n\nSi usas HTTP, pide al admin habilitar HTTPS.`;
        }
      }
    },

    async detenerScanner() {
      if (this.html5QrCode && this.scanning) {
        try {
          await this.html5QrCode.stop();
          this.html5QrCode.clear();
          this.html5QrCode = null;
          this.scanning = false;
        } catch (err) {
          console.error('Error al detener scanner:', err);
          this.scanning = false;
          this.html5QrCode = null;
        }
      }
    },

    async onScanSuccess(decodedText, decodedResult) {
      // Evitar múltiples escaneos del mismo código
      if (this.procesandoEscaneo) {
        return;
      }

      this.procesandoEscaneo = true;
      console.log('QR escaneado:', decodedText);
      this.success = `Código escaneado: ${decodedText}`;

      // DETENER EL SCANNER INMEDIATAMENTE para evitar escaneos duplicados
      await this.detenerScanner();

      // Emitir el código escaneado
      this.$emit('codigo-escaneado', decodedText);

      // Cerrar el modal después de 500ms (solo para mostrar el mensaje de éxito)
      setTimeout(() => {
        this.dialog = false;
        this.procesandoEscaneo = false;
      }, 500);
    },

    onScanFailure(error) {
      // No hacer nada, es normal que falle mientras busca el QR
      // console.warn('Scan failure:', error);
    },

    async cerrarScanner() {
      await this.detenerScanner();
      // Esperar un poco antes de cerrar el diálogo
      setTimeout(() => {
        this.dialog = false;
      }, 100);
    }
  },
  beforeUnmount() {
    this.detenerScanner();
  }
};
</script>

<style scoped>
#qr-reader {
  border: 2px dashed #ccc;
  border-radius: 8px;
  overflow: hidden;
}
</style>
