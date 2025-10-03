<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Marcas</h2>
      <button @click="mostrarModal = true" class="btn btn-primary">
        ➕ Nueva Marca
      </button>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="marca in marcas" :key="marca.id">
              <td>{{ marca.id }}</td>
              <td>{{ marca.nombre }}</td>
              <td>{{ marca.descripcion || '-' }}</td>
              <td>
                <span class="badge" :class="marca.activo ? 'bg-success' : 'bg-secondary'">
                  {{ marca.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>
                <button @click="editarMarca(marca)" class="btn btn-sm btn-warning me-2">✏️</button>
                <button @click="eliminarMarca(marca.id)" class="btn btn-sm btn-danger">🗑️</button>
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
            <h5 class="modal-title">{{ marcaEditando ? 'Editar' : 'Nueva' }} Marca</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Nombre *</label>
              <input v-model="form.nombre" type="text" class="form-control" required>
            </div>
            <div class="mb-3">
              <label class="form-label">Descripción</label>
              <textarea v-model="form.descripcion" class="form-control" rows="2"></textarea>
            </div>
            <div class="mb-3 form-check">
              <input v-model="form.activo" type="checkbox" class="form-check-input" id="activo">
              <label class="form-check-label" for="activo">Activo</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarMarca">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'MarcasLista',
  data() {
    return {
      marcas: [],
      loading: true,
      mostrarModal: false,
      marcaEditando: null,
      form: { nombre: '', descripcion: '', activo: true }
    }
  },
  async created() {
    await this.cargarMarcas()
  },
  methods: {
    async cargarMarcas() {
      try {
        this.loading = true
        const response = await api.getMarcas()
        this.marcas = response.data.results || response.data || []
      } catch (error) {
        console.error('Error:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al cargar las marcas')
      } finally {
        this.loading = false
      }
    },
    editarMarca(marca) {
      this.marcaEditando = marca
      this.form = { ...marca }
      this.mostrarModal = true
    },
    async guardarMarca() {
      try {
        if (this.marcaEditando) {
          await api.updateMarca(this.marcaEditando.id, this.form)
        } else {
          await api.createMarca(this.form)
        }
        await this.cargarMarcas()
        this.cerrarModal()
        alert('Marca guardada correctamente')
      } catch (error) {
        console.error('Error:', error)
        alert('Error al guardar la marca')
      }
    },
    async eliminarMarca(id) {
      if (confirm('¿Eliminar esta marca?')) {
        try {
          await api.deleteMarca(id)
          await this.cargarMarcas()
          alert('Marca eliminada')
        } catch (error) {
          alert('Error al eliminar. Puede tener productos asociados.')
        }
      }
    },
    cerrarModal() {
      this.mostrarModal = false
      this.marcaEditando = null
      this.form = { nombre: '', descripcion: '', activo: true }
    }
  }
}
</script>
