<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Cargando...</span>
      </div>
    </div>
    
    <div v-else-if="cliente">
      <h2>Detalle del Cliente</h2>
      
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ cliente.nombre }}</h5>
          <p class="card-text">
            <strong>Email:</strong> {{ cliente.email }}
          </p>
          <p class="card-text">
            <strong>Teléfono:</strong> {{ cliente.telefono }}
          </p>
          <p class="card-text">
            <strong>Dirección:</strong> {{ cliente.direccion }}
          </p>
          <p class="card-text">
            <strong>Ciudad:</strong> {{ cliente.ciudad }}
          </p>
          <p class="card-text" v-if="cliente.fecha_nacimiento">
            <strong>Fecha de Nacimiento:</strong> {{ formatDate(cliente.fecha_nacimiento) }}
          </p>
          <p class="card-text">
            <small class="text-muted">
              Registrado: {{ formatDate(cliente.created_at) }}
            </small>
          </p>
        </div>
        <div class="card-footer">
          <router-link 
            :to="'/adicionar-cliente/' + cliente.id" 
            class="btn btn-primary me-2">
            Editar
          </router-link>
          <button 
            @click="eliminarCliente" 
            class="btn btn-danger me-2">
            Eliminar
          </button>
          <router-link to="/clientes" class="btn btn-secondary">
            Volver a la Lista
          </router-link>
        </div>
      </div>
    </div>
    
    <div v-else class="alert alert-danger">
      Cliente no encontrado
    </div>
  </div>
</template>

<script>
import ClienteServicioDatos from '../services/ClienteServicioDatos'

export default {
  name: 'ClienteDetalle',
  data() {
    return {
      cliente: null,
      loading: true
    }
  },
  async created() {
    await this.cargarCliente()
  },
  methods: {
    async cargarCliente() {
      try {
        this.loading = true
        const response = await ClienteServicioDatos.getCliente(this.$route.params.id)
        this.cliente = response.data
      } catch (error) {
        console.error('Error al cargar cliente:', error)
        this.cliente = null
      } finally {
        this.loading = false
      }
    },
    async eliminarCliente() {
      if (confirm('¿Estás seguro de eliminar este cliente?')) {
        try {
          await ClienteServicioDatos.deleteCliente(this.cliente.id)
          alert('Cliente eliminado correctamente')
          this.$router.push('/clientes')
        } catch (error) {
          console.error('Error al eliminar cliente:', error)
          alert('Error al eliminar el cliente')
        }
      }
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES')
    }
  }
}
</script>