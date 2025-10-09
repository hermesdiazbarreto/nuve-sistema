<template>
  <v-container class="mt-4">
    <h2>Lista de Clientes</h2>
    <div class="mb-3">
      <v-btn :to="'/adicionar-cliente'" color="primary">
        <v-icon left>mdi-plus</v-icon> Agregar Cliente
      </v-btn>
    </div>

    <div v-if="loading" class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else>
      <v-table hover>
        <thead>
          <tr>
            <th>Documento</th>
            <th>Nombre Completo</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cliente in clientes" :key="cliente.id">
            <td>{{ cliente.tipo_documento }}: {{ cliente.numero_documento || 'N/A' }}</td>
            <td>{{ cliente.nombre_completo }}</td>
            <td>{{ cliente.email || 'N/A' }}</td>
            <td>{{ cliente.telefono || 'N/A' }}</td>
            <td>
              <v-chip
                :color="cliente.activo ? 'success' : 'error'"
                size="small"
                variant="flat"
              >
                {{ cliente.activo ? 'Activo' : 'Inactivo' }}
              </v-chip>
            </td>
            <td>
              <v-btn
                :to="'/adicionar-cliente/' + cliente.id"
                color="warning"
                size="small"
                class="me-2"
              >
                <v-icon>mdi-pencil</v-icon> Editar
              </v-btn>
              <v-btn
                @click="eliminarCliente(cliente.id)"
                color="error"
                size="small"
              >
                <v-icon>mdi-delete</v-icon> Eliminar
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>

      <v-alert
        v-if="clientes.length === 0"
        type="info"
        variant="tonal"
        class="mt-3"
      >
        No hay clientes registrados.
      </v-alert>
    </div>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

    <v-dialog v-model="dialogConfirm" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirmar eliminación</v-card-title>
        <v-card-text>¿Estás seguro de eliminar este cliente?</v-card-text>
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
  name: 'ClientesLista',
  data() {
    return {
      clientes: [],
      loading: true,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogConfirm: false,
      clienteIdToDelete: null
    }
  },
  async created() {
    await this.cargarClientes()
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarClientes() {
      try {
        this.loading = true
        const response = await api.getClientes()
        const clientes = response.data.results || response.data || []
        this.clientes = clientes
      } catch (error) {
        console.error('Error al cargar clientes:', error)
        this.showSnackbar('Error al cargar los clientes', 'error')
      } finally {
        this.loading = false
      }
    },
    eliminarCliente(id) {
      this.clienteIdToDelete = id
      this.dialogConfirm = true
    },
    async confirmarEliminar() {
      try {
        await api.deleteCliente(this.clienteIdToDelete)
        await this.cargarClientes()
        this.showSnackbar('Cliente eliminado correctamente', 'success')
      } catch (error) {
        console.error('Error al eliminar cliente:', error)
        this.showSnackbar('Error al eliminar el cliente', 'error')
      } finally {
        this.dialogConfirm = false
        this.clienteIdToDelete = null
      }
    }
  }
}
</script>
