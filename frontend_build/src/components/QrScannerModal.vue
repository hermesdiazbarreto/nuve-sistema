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
    value: {
      type: Boolean,
      default: false
    }
  },
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
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
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

        this.html5QrCode = new Html5Qrcode('qr-reader');

        const config = {
          fps: 10,
          qrbox: { width: 250, height: 250 },
          aspectRatio: 1.0
        };

        await this.html5QrCode.start(
          { facingMode: 'environment' }, // Cámara trasera
          config,
          this.onScanSuccess,
          this.onScanFailure
        );

        this.scanning = true;
      } catch (err) {
        console.error('Error al iniciar scanner:', err);
        this.cameraError = 'No se pudo acceder a la cámara. Por favor, verifica los permisos.';
      }
    },

    async detenerScanner() {
      if (this.html5QrCode && this.scanning) {
        try {
          await this.html5QrCode.stop();
          this.html5QrCode.clear();
          this.scanning = false;
        } catch (err) {
          console.error('Error al detener scanner:', err);
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

    cerrarScanner() {
      this.detenerScanner();
      this.dialog = false;
    }
  },
  beforeDestroy() {
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
