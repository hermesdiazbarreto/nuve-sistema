<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Tallas</h2>
      <button @click="mostrarModal = true" class="btn btn-primary">➕ Nueva Talla</button>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Orden</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="talla in tallas" :key="talla.id">
              <td>{{ talla.id }}</td>
              <td><strong>{{ talla.nombre }}</strong></td>
              <td>{{ talla.orden }}</td>
              <td>
                <button @click="editarTalla(talla)" class="btn btn-sm btn-warning me-2">✏️</button>
                <button @click="eliminarTalla(talla.id)" class="btn btn-sm btn-danger">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="mostrarModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ tallaEditando ? 'Editar' : 'Nueva' }} Talla</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Nombre * (ej: XS, S, M, L, XL)</label>
              <input v-model="form.nombre" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Orden (para ordenar)</label>
              <input v-model.number="form.orden" type="number" class="form-control" min="0">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarTalla">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'TallasLista',
  data() {
    return {
      tallas: [],
      loading: true,
      mostrarModal: false,
      tallaEditando: null,
      form: { nombre: '', orden: 0 }
    }
  },
  async created() {
    await this.cargarTallas()
  },
  methods: {
    async cargarTallas() {
      try {
        this.loading = true
        const response = await api.getTallas()
        this.tallas = response.data.results || response.data || []
      } catch (error) {
        console.error('Error:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al cargar tallas')
      } finally {
        this.loading = false
      }
    },
    editarTalla(talla) {
      this.tallaEditando = talla
      this.form = { ...talla }
      this.mostrarModal = true
    },
    async guardarTalla() {
      try {
        if (this.tallaEditando) {
          await api.updateTalla(this.tallaEditando.id, this.form)
        } else {
          await api.createTalla(this.form)
        }
        await this.cargarTallas()
        this.cerrarModal()
        alert('Talla guardada correctamente')
      } catch (error) {
        console.error('Error:', error)
        alert('Error al guardar la talla')
      }
    },
    async eliminarTalla(id) {
      if (confirm('¿Eliminar esta talla?')) {
        try {
          await api.deleteTalla(id)
          await this.cargarTallas()
          alert('Talla eliminada')
        } catch (error) {
          alert('Error al eliminar. Puede tener variantes asociadas.')
        }
      }
    },
    cerrarModal() {
      this.mostrarModal = false
      this.tallaEditando = null
      this.form = { nombre: '', orden: 0 }
    }
  }
}
</script>
