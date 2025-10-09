<template>
  <v-container class="mt-4">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Tallas</h2>
      <v-btn @click="mostrarModal = true" color="primary">
        <v-icon left>mdi-plus</v-icon> Nueva Talla
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
              <v-btn @click="editarTalla(talla)" icon="mdi-pencil" size="small" color="warning" class="me-2"></v-btn>
              <v-btn @click="eliminarTalla(talla.id)" icon="mdi-delete" size="small" color="error"></v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Modal -->
    <v-dialog v-model="mostrarModal" max-width="600">
      <v-card>
        <v-card-title class="text-h6">{{ tallaEditando ? 'Editar' : 'Nueva' }} Talla</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="form.nombre"
            label="Nombre * (ej: XS, S, M, L, XL)"
            variant="outlined"
            density="comfortable"
            required
            class="mb-3"
          ></v-text-field>
          <v-text-field
            v-model.number="form.orden"
            type="number"
            label="Orden (para ordenar)"
            variant="outlined"
            density="comfortable"
            min="0"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="cerrarModal">Cancelar</v-btn>
          <v-btn color="primary" @click="guardarTalla">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

    <v-dialog v-model="dialogConfirm" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirmar eliminación</v-card-title>
        <v-card-text>¿Eliminar esta talla?</v-card-text>
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
  name: 'TallasLista',
  data() {
    return {
      tallas: [],
      loading: true,
      mostrarModal: false,
      tallaEditando: null,
      form: { nombre: '', orden: 0 },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogConfirm: false,
      tallaIdToDelete: null
    }
  },
  async created() {
    await this.cargarTallas()
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarTallas() {
      try {
        this.loading = true
        const response = await api.getTallas()
        this.tallas = response.data.results || response.data || []
      } catch (error) {
        console.error('Error:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al cargar tallas', 'error')
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
        this.showSnackbar('Talla guardada correctamente', 'success')
      } catch (error) {
        console.error('Error:', error)
        this.showSnackbar('Error al guardar la talla', 'error')
      }
    },
    eliminarTalla(id) {
      this.tallaIdToDelete = id
      this.dialogConfirm = true
    },
    async confirmarEliminar() {
      try {
        await api.deleteTalla(this.tallaIdToDelete)
        await this.cargarTallas()
        this.showSnackbar('Talla eliminada', 'success')
      } catch (error) {
        this.showSnackbar('Error al eliminar. Puede tener variantes asociadas.', 'error')
      } finally {
        this.dialogConfirm = false
        this.tallaIdToDelete = null
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
