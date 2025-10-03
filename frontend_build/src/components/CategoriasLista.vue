<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Categorías</h2>
      <button @click="mostrarModal = true" class="btn btn-primary">
        ➕ Nueva Categoría
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
              <th>Fecha Creación</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="categoria in categorias" :key="categoria.id">
              <td>{{ categoria.id }}</td>
              <td>{{ categoria.nombre }}</td>
              <td>{{ categoria.descripcion || '-' }}</td>
              <td>
                <span class="badge" :class="categoria.activo ? 'bg-success' : 'bg-secondary'">
                  {{ categoria.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>{{ formatFecha(categoria.fecha_creacion) }}</td>
              <td>
                <button @click="editarCategoria(categoria)" class="btn btn-sm btn-warning me-2">
                  ✏️ Editar
                </button>
                <button @click="eliminarCategoria(categoria.id)" class="btn btn-sm btn-danger">
                  🗑️ Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="categorias.length === 0" class="alert alert-info">
        No hay categorías registradas.
      </div>
    </div>

    <!-- Modal para crear/editar categoría -->
    <div v-if="mostrarModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ categoriaEditando ? 'Editar' : 'Nueva' }} Categoría</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarCategoria">
              <div class="mb-3">
                <label class="form-label">Nombre *</label>
                <input v-model="form.nombre" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Descripción</label>
                <textarea v-model="form.descripcion" class="form-control" rows="3"></textarea>
              </div>
              <div class="mb-3 form-check">
                <input v-model="form.activo" type="checkbox" class="form-check-input" id="activo">
                <label class="form-check-label" for="activo">Activo</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarCategoria">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'CategoriasLista',
  data() {
    return {
      categorias: [],
      loading: true,
      mostrarModal: false,
      categoriaEditando: null,
      form: {
        nombre: '',
        descripcion: '',
        activo: true
      }
    }
  },
  async created() {
    await this.cargarCategorias()
  },
  methods: {
    async cargarCategorias() {
      try {
        this.loading = true
        const response = await api.getCategorias()
        this.categorias = response.data.results || response.data || []
      } catch (error) {
        console.error('Error al cargar categorías:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al cargar las categorías')
      } finally {
        this.loading = false
      }
    },
    editarCategoria(categoria) {
      this.categoriaEditando = categoria
      this.form = {
        nombre: categoria.nombre,
        descripcion: categoria.descripcion || '',
        activo: categoria.activo
      }
      this.mostrarModal = true
    },
    async guardarCategoria() {
      try {
        if (this.categoriaEditando) {
          await api.updateCategoria(this.categoriaEditando.id, this.form)
          alert('Categoría actualizada correctamente')
        } else {
          await api.createCategoria(this.form)
          alert('Categoría creada correctamente')
        }
        await this.cargarCategorias()
        this.cerrarModal()
      } catch (error) {
        console.error('Error al guardar categoría:', error)
        alert('Error al guardar la categoría')
      }
    },
    async eliminarCategoria(id) {
      if (confirm('¿Estás seguro de eliminar esta categoría?')) {
        try {
          await api.deleteCategoria(id)
          alert('Categoría eliminada correctamente')
          await this.cargarCategorias()
        } catch (error) {
          console.error('Error al eliminar categoría:', error)
          alert('Error al eliminar la categoría. Puede tener productos asociados.')
        }
      }
    },
    cerrarModal() {
      this.mostrarModal = false
      this.categoriaEditando = null
      this.form = {
        nombre: '',
        descripcion: '',
        activo: true
      }
    },
    formatFecha(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleDateString('es-ES')
    }
  }
}
</script>
