<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Cargando...</span>
      </div>
    </div>
    
    <div v-else-if="producto">
      <h2>Detalle del Producto</h2>
      
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ producto.nombre }}</h5>
          <p class="card-text">
            <strong>Descripción:</strong> {{ producto.descripcion }}
          </p>
          <p class="card-text">
            <strong>Precio:</strong> ${{ producto.precio }}
          </p>
          <p class="card-text">
            <strong>Stock:</strong> {{ producto.stock }} unidades
          </p>
          <p class="card-text">
            <strong>Categoría:</strong> {{ producto.categoria_nombre }}
          </p>
          <p class="card-text">
            <strong>Marca:</strong> {{ producto.marca_nombre }}
          </p>
          <p class="card-text">
            <small class="text-muted">
              Creado: {{ formatDate(producto.created_at) }}
            </small>
          </p>
        </div>
        <div class="card-footer">
          <router-link 
            :to="'/adicionar-articulo/' + producto.id" 
            class="btn btn-primary me-2">
            Editar
          </router-link>
          <button 
            @click="eliminarProducto" 
            class="btn btn-danger me-2">
            Eliminar
          </button>
          <router-link to="/articulos" class="btn btn-secondary">
            Volver a la Lista
          </router-link>
        </div>
      </div>
    </div>
    
    <div v-else class="alert alert-danger">
      Producto no encontrado
    </div>
  </div>
</template>

<script>
import ArticuloServicioDatos from '../services/ArticuloServicioDatos'

export default {
  name: 'ArticuloDetalle',
  data() {
    return {
      producto: null,
      loading: true
    }
  },
  async created() {
    await this.cargarProducto()
  },
  methods: {
    async cargarProducto() {
      try {
        this.loading = true
        const response = await ArticuloServicioDatos.getProducto(this.$route.params.id)
        this.producto = response.data
      } catch (error) {
        console.error('Error al cargar producto:', error)
        this.producto = null
      } finally {
        this.loading = false
      }
    },
    async eliminarProducto() {
      if (confirm('¿Estás seguro de eliminar este producto?')) {
        try {
          await ArticuloServicioDatos.deleteProducto(this.producto.id)
          alert('Producto eliminado correctamente')
          this.$router.push('/articulos')
        } catch (error) {
          console.error('Error al eliminar producto:', error)
          alert('Error al eliminar el producto')
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