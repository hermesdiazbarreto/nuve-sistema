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

        <v-alert v-else type="warning" class="mb-4">
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
      scanning: false
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

      try {
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
          this.cameraError = 'Necesitas dar permisos de cámara en tu navegador. Ve a Configuración → Permisos del sitio → Cámara.';
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
        if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
          this.cameraError = 'Permiso de cámara denegado. Por favor, permite el acceso a la cámara en la configuración de tu navegador.';
        } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
          this.cameraError = 'No se encontró ninguna cámara en tu dispositivo.';
        } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
          this.cameraError = 'La cámara está siendo usada por otra aplicación. Cierra otras apps que usen la cámara.';
        } else {
          this.cameraError = `Error al acceder a la cámara: ${err.message || 'Error desconocido'}. Intenta recargar la página.`;
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

    onScanSuccess(decodedText, decodedResult) {
      console.log('QR escaneado:', decodedText);
      this.success = `Código escaneado: ${decodedText}`;
      
      // Emitir el código escaneado
      this.$emit('codigo-escaneado', decodedText);
      
      // Cerrar el scanner después de 1 segundo
      setTimeout(() => {
        this.cerrarScanner();
      }, 1000);
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
