<template>
  <div class="container mt-4">
    <h2>Lista de Clientes</h2>
    <div class="mb-3">
      <router-link to="/adicionar-cliente" class="btn btn-primary">
        Agregar Cliente
      </router-link>
    </div>
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Cargando...</span>
      </div>
    </div>
    
    <div v-else>
      <table class="table table-striped">
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
              <span :class="cliente.activo ? 'badge bg-success' : 'badge bg-danger'">
                {{ cliente.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td>
              <router-link
                :to="'/adicionar-cliente/' + cliente.id"
                class="btn btn-sm btn-warning me-2">
                ✏️ Editar
              </router-link>
              <button
                @click="eliminarCliente(cliente.id)"
                class="btn btn-sm btn-danger">
                🗑️ Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="clientes.length === 0" class="alert alert-info">
        No hay clientes registrados.
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ClientesLista',
  data() {
    return {
      clientes: [],
      loading: true
    }
  },
  async created() {
    await this.cargarClientes()
  },
  methods: {
    async cargarClientes() {
      try {
        this.loading = true
        const response = await api.getClientes()
        const clientes = response.data.results || response.data || []
        this.clientes = clientes
      } catch (error) {
        console.error('Error al cargar clientes:', error)
        alert('Error al cargar los clientes')
      } finally {
        this.loading = false
      }
    },
    async eliminarCliente(id) {
      if (confirm('¿Estás seguro de eliminar este cliente?')) {
        try {
          await api.deleteCliente(id)
          await this.cargarClientes() // Recargar la lista
          alert('Cliente eliminado correctamente')
        } catch (error) {
          console.error('Error al eliminar cliente:', error)
          alert('Error al eliminar el cliente')
        }
      }
    }
  }
}
</script>