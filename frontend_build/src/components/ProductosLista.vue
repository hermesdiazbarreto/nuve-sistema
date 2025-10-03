<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>📦 Productos</h2>
      <router-link to="/productos/nuevo" class="btn btn-primary">
        ➕ Nuevo Producto
      </router-link>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Categoría</th>
              <th>Marca</th>
              <th>Precio Venta</th>
              <th>Variantes</th>
              <th>Stock Total</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="producto in productos" :key="producto.id">
              <td><strong>{{ producto.codigo }}</strong></td>
              <td>{{ producto.nombre }}</td>
              <td><span class="badge bg-secondary">{{ producto.categoria_nombre }}</span></td>
              <td>{{ producto.marca_nombre }}</td>
              <td>${{ Number(producto.precio_venta).toFixed(2) }}</td>
              <td>
                <button @click="verVariantes(producto)" class="btn btn-sm btn-info">
                  🔍 {{ producto.total_variantes || 0 }} variante(s)
                </button>
              </td>
              <td>
                <span :class="getStockClass(producto.stock_total)">
                  {{ producto.stock_total || 0 }}
                </span>
              </td>
              <td>
                <span class="badge" :class="producto.activo ? 'bg-success' : 'bg-secondary'">
                  {{ producto.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>
                <router-link :to="`/productos/editar/${producto.id}`" class="btn btn-sm btn-warning me-1">
                  ✏️
                </router-link>
                <button @click="eliminarProducto(producto.id)" class="btn btn-sm btn-danger">
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="productos.length === 0" class="alert alert-info">
        No hay productos registrados.
      </div>
    </div>

    <!-- Modal de Variantes -->
    <div v-if="mostrarVariantes && productoSeleccionado" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Variantes de: {{ productoSeleccionado.nombre }}
            </h5>
            <button type="button" class="btn-close" @click="cerrarVariantes"></button>
          </div>
          <div class="modal-body">
            <router-link :to="`/variantes/nueva/${productoSeleccionado.id}`" class="btn btn-sm btn-primary mb-3">
              ➕ Agregar Variante
            </router-link>

            <div v-if="cargandoVariantes" class="text-center">
              <div class="spinner-border spinner-border-sm"></div>
            </div>
            <div v-else-if="variantesProducto.length === 0" class="alert alert-info">
              Este producto no tiene variantes.
            </div>
            <table v-else class="table table-sm">
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Talla</th>
                  <th>Color</th>
                  <th>Stock</th>
                  <th>Min</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="variante in variantesProducto" :key="variante.id">
                  <td>{{ variante.codigo_variante }}</td>
                  <td>{{ variante.talla_nombre }}</td>
                  <td>{{ variante.color_nombre }}</td>
                  <td :class="variante.stock_actual <= variante.stock_minimo ? 'text-danger fw-bold' : ''">
                    {{ variante.stock_actual }}
                  </td>
                  <td>{{ variante.stock_minimo }}</td>
                  <td>
                    <span class="badge" :class="variante.activo ? 'bg-success' : 'bg-secondary'">
                      {{ variante.activo ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarVariantes">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProductosLista',
  data() {
    return {
      productos: [],
      loading: true,
      mostrarVariantes: false,
      productoSeleccionado: null,
      variantesProducto: [],
      cargandoVariantes: false
    }
  },
  async created() {
    await this.cargarProductos()
  },
  methods: {
    async cargarProductos() {
      try {
        this.loading = true
        const [productosRes, variantesRes] = await Promise.all([
          api.getProductos(),
          api.getProductoVariantes()
        ])

        // Los datos pueden venir en .data o .data.results (DRF pagination)
        const productos = productosRes.data.results || productosRes.data || []
        const variantes = variantesRes.data.results || variantesRes.data || []

        // Calcular stock total y cantidad de variantes por producto
        this.productos = productos.map(producto => {
          const variantesProducto = variantes.filter(v => v.producto === producto.id)
          const stockTotal = variantesProducto.reduce((sum, v) => sum + (v.stock_actual || 0), 0)
          return {
            ...producto,
            total_variantes: variantesProducto.length,
            stock_total: stockTotal
          }
        })
      } catch (error) {
        console.error('Error al cargar productos:', error)
        console.error('Detalles del error:', error.response?.data)
        alert('Error al cargar los productos. Abre la consola (F12) para ver detalles.')
      } finally {
        this.loading = false
      }
    },
    async verVariantes(producto) {
      this.productoSeleccionado = producto
      this.mostrarVariantes = true
      this.cargandoVariantes = true

      try {
        const response = await api.getProductoVariantes()
        const variantes = response.data.results || response.data || []
        this.variantesProducto = variantes.filter(v => v.producto === producto.id)
      } catch (error) {
        console.error('Error al cargar variantes:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al cargar las variantes')
      } finally {
        this.cargandoVariantes = false
      }
    },
    cerrarVariantes() {
      this.mostrarVariantes = false
      this.productoSeleccionado = null
      this.variantesProducto = []
    },
    async eliminarProducto(id) {
      if (confirm('¿Estás seguro de eliminar este producto? Se eliminarán también sus variantes.')) {
        try {
          await api.deleteProducto(id)
          await this.cargarProductos()
          alert('Producto eliminado correctamente')
        } catch (error) {
          console.error('Error al eliminar producto:', error)
          alert('Error al eliminar el producto')
        }
      }
    },
    getStockClass(stock) {
      if (stock === 0) return 'badge bg-danger'
      if (stock < 10) return 'badge bg-warning'
      return 'badge bg-success'
    }
  }
}
</script>

<style scoped>
.table tbody tr {
  transition: background-color 0.2s;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}
</style>
