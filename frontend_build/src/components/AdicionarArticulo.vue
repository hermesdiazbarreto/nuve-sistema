<template>
  <div class="container mt-4">
    <h2>{{ isEdit ? 'Editar Producto' : 'Agregar Producto' }}</h2>
    
    <form @submit.prevent="guardarProducto">
      <div class="mb-3">
        <label for="nombre" class="form-label">Nombre:</label>
        <input 
          type="text" 
          class="form-control" 
          id="nombre"
          v-model="producto.nombre" 
          required>
      </div>
      
      <div class="mb-3">
        <label for="descripcion" class="form-label">Descripción:</label>
        <textarea 
          class="form-control" 
          id="descripcion"
          v-model="producto.descripcion" 
          rows="3"
          required>
        </textarea>
      </div>
      
      <div class="mb-3">
        <label for="precio" class="form-label">Precio:</label>
        <input 
          type="number" 
          step="0.01"
          class="form-control" 
          id="precio"
          v-model="producto.precio" 
          required>
      </div>
      
      <div class="mb-3">
        <label for="stock" class="form-label">Stock:</label>
        <input 
          type="number" 
          class="form-control" 
          id="stock"
          v-model="producto.stock" 
          required>
      </div>
      
      <div class="mb-3">
        <label for="categoria" class="form-label">Categoría:</label>
        <input 
          type="text" 
          class="form-control" 
          id="categoria"
          v-model="producto.categoria" 
          required>
      </div>
      
      <div class="mb-3">
        <label for="marca" class="form-label">Marca:</label>
        <input 
          type="text" 
          class="form-control" 
          id="marca"
          v-model="producto.marca" 
          required>
      </div>
      
      <div class="mb-3">
        <button type="submit" class="btn btn-success me-2">
          {{ isEdit ? 'Actualizar' : 'Guardar' }}
        </button>
        <router-link to="/articulos" class="btn btn-secondary">
          Cancelar
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import ArticuloServicioDatos from '../services/ArticuloServicioDatos'

export default {
  name: 'AdicionarArticulo',
  data() {
    return {
      producto: {
        nombre: '',
        descripcion: '',
        precio: '',
        stock: '',
        categoria: '',
        marca: ''
      },
      isEdit: false
    }
  },
  async created() {
    if (this.$route.params.id) {
      this.isEdit = true
      await this.cargarProducto()
    }
  },
  methods: {
    async cargarProducto() {
      try {
        const response = await ArticuloServicioDatos.getProducto(this.$route.params.id)
        this.producto = response.data
      } catch (error) {
        console.error('Error al cargar producto:', error)
        alert('Error al cargar el producto')
      }
    },
    async guardarProducto() {
      try {
        if (this.isEdit) {
          await ArticuloServicioDatos.updateProducto(this.$route.params.id, this.producto)
          alert('Producto actualizado correctamente')
        } else {
          await ArticuloServicioDatos.createProducto(this.producto)
          alert('Producto creado correctamente')
        }
        this.$router.push('/articulos')
      } catch (error) {
        console.error('Error al guardar producto:', error)
        alert('Error al guardar el producto')
      }
    }
  }
}
</script>