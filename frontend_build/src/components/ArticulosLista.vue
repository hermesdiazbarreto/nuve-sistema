<template>
  <div class="container mt-4">
    <h2>Lista de Productos</h2>
    <div class="mb-3">
      <router-link to="/adicionar-articulo" class="btn btn-primary">
        Agregar Producto
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
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Categoría</th>
            <th>Marca</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="producto in productos" :key="producto.id">
            <td>{{ producto.id }}</td>
            <td>{{ producto.nombre }}</td>
            <td>{{ producto.descripcion }}</td>
            <td>${{ producto.precio }}</td>
            <td>{{ producto.stock }}</td>
            <td>{{ producto.categoria_nombre }}</td>
            <td>{{ producto.marca_nombre }}</td>
            <td>
              <router-link 
                :to="'/articulo/' + producto.id" 
                class="btn btn-sm btn-info me-2">
                Ver
              </router-link>
              <button 
                @click="eliminarProducto(producto.id)" 
                class="btn btn-sm btn-danger">
                Eliminar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="productos.length === 0" class="alert alert-info">
        No hay productos registrados.
      </div>
    </div>
  </div>
</template>

<script>
import ArticuloServicioDatos from '../services/ArticuloServicioDatos'

export default {
  name: 'ArticulosLista',
  data() {
    return {
      productos: [],
      loading: true
    }
  },
  async created() {
    await this.cargarProductos()
  },
  methods: {
    async cargarProductos() {
      try {
        this.loading = true
        const response = await ArticuloServicioDatos.getProductos()
        this.productos = response.data
      } catch (error) {
        console.error('Error al cargar productos:', error)
        alert('Error al cargar los productos')
      } finally {
        this.loading = false
      }
    },
    async eliminarProducto(id) {
      if (confirm('¿Estás seguro de eliminar este producto?')) {
        try {
          await ArticuloServicioDatos.deleteProducto(id)
          await this.cargarProductos() // Recargar la lista
          alert('Producto eliminado correctamente')
        } catch (error) {
          console.error('Error al eliminar producto:', error)
          alert('Error al eliminar el producto')
        }
      }
    }
  }
}
</script>