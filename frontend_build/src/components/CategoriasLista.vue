<template>
  <v-container class="mt-4">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Categorías</h2>
      <v-btn @click="mostrarModal = true" color="primary">
        <v-icon left>mdi-plus</v-icon> Nueva Categoría
      </v-btn>
    </div>

    <div v-if="loading" class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else>
      <v-table hover>
        <thead>
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
              <v-chip
                :color="categoria.activo ? 'success' : 'secondary'"
                size="small"
                variant="flat"
              >
                {{ categoria.activo ? 'Activo' : 'Inactivo' }}
              </v-chip>
            </td>
            <td>{{ formatFecha(categoria.fecha_creacion) }}</td>
            <td>
              <v-btn @click="editarCategoria(categoria)" color="warning" size="small" class="me-2">
                <v-icon>mdi-pencil</v-icon> Editar
              </v-btn>
              <v-btn @click="eliminarCategoria(categoria.id)" color="error" size="small">
                <v-icon>mdi-delete</v-icon> Eliminar
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>

      <v-alert v-if="categorias.length === 0" type="info" variant="tonal" class="mt-3">
        No hay categorías registradas.
      </v-alert>
    </div>

    <!-- Modal para crear/editar categoría -->
    <v-dialog v-model="mostrarModal" max-width="600">
      <v-card>
        <v-card-title class="text-h6">
          {{ categoriaEditando ? 'Editar' : 'Nueva' }} Categoría
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="guardarCategoria">
            <v-text-field
              v-model="form.nombre"
              label="Nombre *"
              variant="outlined"
              density="comfortable"
              required
              class="mb-3"
            ></v-text-field>
            <v-textarea
              v-model="form.descripcion"
              label="Descripción"
              variant="outlined"
              rows="3"
              class="mb-3"
            ></v-textarea>
            <v-checkbox
              v-model="form.activo"
              label="Activo"
              color="primary"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="cerrarModal">Cancelar</v-btn>
          <v-btn color="primary" @click="guardarCategoria">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

    <v-dialog v-model="dialogConfirm" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirmar eliminación</v-card-title>
        <v-card-text>¿Estás seguro de eliminar esta categoría?</v-card-text>
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
      },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogConfirm: false,
      categoriaIdToDelete: null
    }
  },
  async created() {
    await this.cargarCategorias()
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarCategorias() {
      try {
        this.loading = true
        const response = await api.getCategorias()
        this.categorias = response.data.results || response.data || []
      } catch (error) {
        console.error('Error al cargar categorías:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al cargar las categorías', 'error')
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
          this.showSnackbar('Categoría actualizada correctamente', 'success')
        } else {
          await api.createCategoria(this.form)
          this.showSnackbar('Categoría creada correctamente', 'success')
        }
        await this.cargarCategorias()
        this.cerrarModal()
      } catch (error) {
        console.error('Error al guardar categoría:', error)
        this.showSnackbar('Error al guardar la categoría', 'error')
      }
    },
    eliminarCategoria(id) {
      this.categoriaIdToDelete = id
      this.dialogConfirm = true
    },
    async confirmarEliminar() {
      try {
        await api.deleteCategoria(this.categoriaIdToDelete)
        this.showSnackbar('Categoría eliminada correctamente', 'success')
        await this.cargarCategorias()
      } catch (error) {
        console.error('Error al eliminar categoría:', error)
        this.showSnackbar('Error al eliminar la categoría. Puede tener productos asociados.', 'error')
      } finally {
        this.dialogConfirm = false
        this.categoriaIdToDelete = null
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
