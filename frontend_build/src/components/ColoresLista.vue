<template>
  <v-container class="mt-4">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Colores</h2>
      <v-btn @click="mostrarModal = true" color="primary">
        <v-icon left>mdi-plus</v-icon> Nuevo Color
      </v-btn>
    </div>

    <div v-if="loading" class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else>
      <v-row>
        <v-col v-for="color in colores" :key="color.id" cols="12" sm="6" md="3">
          <v-card elevation="3" class="color-card">
            <v-card-text>
              <div class="d-flex align-center mb-2">
                <div
                  class="color-preview me-2"
                  :style="{ backgroundColor: color.codigo_hex || '#cccccc' }"
                ></div>
                <h5 class="mb-0">{{ color.nombre }}</h5>
              </div>
              <p class="text-medium-emphasis text-body-2 mb-2">{{ color.codigo_hex || 'Sin código' }}</p>
              <div class="d-flex ga-2">
                <v-btn @click="editarColor(color)" color="warning" size="small" block>
                  <v-icon>mdi-pencil</v-icon> Editar
                </v-btn>
                <v-btn @click="eliminarColor(color.id)" color="error" size="small" icon="mdi-delete"></v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Modal -->
    <v-dialog v-model="mostrarModal" max-width="600">
      <v-card>
        <v-card-title class="text-h6">{{ colorEditando ? 'Editar' : 'Nuevo' }} Color</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="form.nombre"
            label="Nombre * (ej: Rojo, Azul, Negro)"
            variant="outlined"
            density="comfortable"
            required
            class="mb-3"
          ></v-text-field>
          <div class="mb-3">
            <label class="text-body-2 mb-2 d-block">Código Hex (ej: #FF0000)</label>
            <div class="d-flex ga-2">
              <v-text-field
                v-model="form.codigo_hex"
                variant="outlined"
                density="comfortable"
                placeholder="#000000"
                class="flex-grow-1"
              ></v-text-field>
              <input v-model="form.codigo_hex" type="color" class="color-picker">
            </div>
          </div>
          <div v-if="form.codigo_hex" class="mb-3">
            <label class="text-body-2 mb-2 d-block">Vista Previa:</label>
            <div class="color-preview-large" :style="{ backgroundColor: form.codigo_hex }"></div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="cerrarModal">Cancelar</v-btn>
          <v-btn color="primary" @click="guardarColor">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

    <v-dialog v-model="dialogConfirm" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirmar eliminación</v-card-title>
        <v-card-text>¿Eliminar este color?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="dialogConfirm = false">No</v-btn>
          <v-btn color="error" @click="confirmarEliminar">Sí</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ColoresLista',
  data() {
    return {
      colores: [],
      loading: true,
      mostrarModal: false,
      colorEditando: null,
      form: { nombre: '', codigo_hex: '#000000' },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogConfirm: false,
      colorIdToDelete: null
    }
  },
  async created() {
    await this.cargarColores()
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarColores() {
      try {
        this.loading = true
        const response = await api.getColores()
        this.colores = response.data.results || response.data || []
      } catch (error) {
        console.error('Error:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al cargar colores', 'error')
      } finally {
        this.loading = false
      }
    },
    editarColor(color) {
      this.colorEditando = color
      this.form = { ...color }
      this.mostrarModal = true
    },
    async guardarColor() {
      try {
        if (this.colorEditando) {
          await api.updateColor(this.colorEditando.id, this.form)
        } else {
          await api.createColor(this.form)
        }
        await this.cargarColores()
        this.cerrarModal()
        this.showSnackbar('Color guardado correctamente', 'success')
      } catch (error) {
        console.error('Error:', error)
        this.showSnackbar('Error al guardar el color', 'error')
      }
    },
    eliminarColor(id) {
      this.colorIdToDelete = id
      this.dialogConfirm = true
    },
    async confirmarEliminar() {
      try {
        await api.deleteColor(this.colorIdToDelete)
        await this.cargarColores()
        this.showSnackbar('Color eliminado', 'success')
      } catch (error) {
        this.showSnackbar('Error al eliminar. Puede tener variantes asociadas.', 'error')
      } finally {
        this.dialogConfirm = false
        this.colorIdToDelete = null
      }
    },
    cerrarModal() {
      this.mostrarModal = false
      this.colorEditando = null
      this.form = { nombre: '', codigo_hex: '#000000' }
    }
  }
}
</script>

<style scoped>
.color-preview {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  border: 2px solid #ddd;
}

.color-preview-large {
  width: 100%;
  height: 80px;
  border-radius: 4px;
  border: 2px solid #ddd;
}

.color-card {
  transition: transform 0.2s;
}

.color-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.color-picker {
  width: 60px;
  height: 40px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
