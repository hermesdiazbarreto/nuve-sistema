<template>
  <v-container class="mt-4">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Marcas</h2>
      <v-btn @click="mostrarModal = true" color="primary">
        <v-icon left>mdi-plus</v-icon> Nueva Marca
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
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="marca in marcas" :key="marca.id">
            <td>{{ marca.id }}</td>
            <td>{{ marca.nombre }}</td>
            <td>{{ marca.descripcion || '-' }}</td>
            <td>
              <v-chip
                :color="marca.activo ? 'success' : 'secondary'"
                size="small"
                variant="flat"
              >
                {{ marca.activo ? 'Activo' : 'Inactivo' }}
              </v-chip>
            </td>
            <td>
              <v-btn @click="editarMarca(marca)" icon="mdi-pencil" size="small" color="warning" class="me-2"></v-btn>
              <v-btn @click="eliminarMarca(marca.id)" icon="mdi-delete" size="small" color="error"></v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Modal -->
    <v-dialog v-model="mostrarModal" max-width="600">
      <v-card>
        <v-card-title class="text-h6">{{ marcaEditando ? 'Editar' : 'Nueva' }} Marca</v-card-title>
        <v-card-text>
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
            rows="2"
            class="mb-3"
          ></v-textarea>
          <v-checkbox
            v-model="form.activo"
            label="Activo"
            color="primary"
          ></v-checkbox>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="cerrarModal">Cancelar</v-btn>
          <v-btn color="primary" @click="guardarMarca">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

    <v-dialog v-model="dialogConfirm" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirmar eliminación</v-card-title>
        <v-card-text>¿Eliminar esta marca?</v-card-text>
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
  name: 'MarcasLista',
  data() {
    return {
      marcas: [],
      loading: true,
      mostrarModal: false,
      marcaEditando: null,
      form: { nombre: '', descripcion: '', activo: true },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogConfirm: false,
      marcaIdToDelete: null
    }
  },
  async created() {
    await this.cargarMarcas()
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarMarcas() {
      try {
        this.loading = true
        const response = await api.getMarcas()
        this.marcas = response.data.results || response.data || []
      } catch (error) {
        console.error('Error:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al cargar las marcas', 'error')
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
        this.showSnackbar('Marca guardada correctamente', 'success')
      } catch (error) {
        console.error('Error:', error)
        this.showSnackbar('Error al guardar la marca', 'error')
      }
    },
    eliminarMarca(id) {
      this.marcaIdToDelete = id
      this.dialogConfirm = true
    },
    async confirmarEliminar() {
      try {
        await api.deleteMarca(this.marcaIdToDelete)
        await this.cargarMarcas()
        this.showSnackbar('Marca eliminada', 'success')
      } catch (error) {
        this.showSnackbar('Error al eliminar. Puede tener productos asociados.', 'error')
      } finally {
        this.dialogConfirm = false
        this.marcaIdToDelete = null
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