<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Colores</h2>
      <button @click="mostrarModal = true" class="btn btn-primary">➕ Nuevo Color</button>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else>
      <div class="row">
        <div v-for="color in colores" :key="color.id" class="col-md-3 mb-3">
          <div class="card">
            <div class="card-body">
              <div class="d-flex align-items-center mb-2">
                <div
                  class="color-preview me-2"
                  :style="{ backgroundColor: color.codigo_hex || '#cccccc' }"
                ></div>
                <h5 class="mb-0">{{ color.nombre }}</h5>
              </div>
              <p class="text-muted small mb-2">{{ color.codigo_hex || 'Sin código' }}</p>
              <div class="btn-group btn-group-sm w-100">
                <button @click="editarColor(color)" class="btn btn-warning">✏️ Editar</button>
                <button @click="eliminarColor(color.id)" class="btn btn-danger">🗑️</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="mostrarModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ colorEditando ? 'Editar' : 'Nuevo' }} Color</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Nombre * (ej: Rojo, Azul, Negro)</label>
              <input v-model="form.nombre" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Código Hex (ej: #FF0000)</label>
              <div class="input-group">
                <input v-model="form.codigo_hex" type="text" class="form-control" placeholder="#000000">
                <input v-model="form.codigo_hex" type="color" class="form-control form-control-color">
              </div>
            </div>
            <div v-if="form.codigo_hex" class="mb-3">
              <label class="form-label">Vista Previa:</label>
              <div class="color-preview-large" :style="{ backgroundColor: form.codigo_hex }"></div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarColor">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
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
      form: { nombre: '', codigo_hex: '#000000' }
    }
  },
  async created() {
    await this.cargarColores()
  },
  methods: {
    async cargarColores() {
      try {
        this.loading = true
        const response = await api.getColores()
        this.colores = response.data.results || response.data || []
      } catch (error) {
        console.error('Error:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al cargar colores')
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
        alert('Color guardado correctamente')
      } catch (error) {
        console.error('Error:', error)
        alert('Error al guardar el color')
      }
    },
    async eliminarColor(id) {
      if (confirm('¿Eliminar este color?')) {
        try {
          await api.deleteColor(id)
          await this.cargarColores()
          alert('Color eliminado')
        } catch (error) {
          alert('Error al eliminar. Puede tener variantes asociadas.')
        }
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

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
