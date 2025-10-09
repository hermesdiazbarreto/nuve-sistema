<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>🗑️ Productos Eliminados</h2>
      <div>
        <router-link to="/productos" class="btn btn-outline-secondary me-2">
          ← Volver a Productos
        </router-link>
      </div>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else>
      <div v-if="productos.length === 0" class="alert alert-info">
        <h5>✅ No hay productos eliminados</h5>
        <p class="mb-0">Todos los productos están activos.</p>
      </div>

      <div v-else class="alert alert-warning">
        <strong>ℹ️ Información:</strong> Estos productos han sido eliminados pero aún se conservan en la base de datos. Puedes restaurarlos cuando quieras.
      </div>

      <div v-if="productos.length > 0" class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Categoría</th>
              <th>Marca</th>
              <th>Precio Venta</th>
              <th>Fecha Eliminación</th>
              <th>Eliminado Por</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="producto in productos" :key="producto.id" class="table-danger">
              <td><strong>{{ producto.codigo }}</strong></td>
              <td>{{ producto.nombre }}</td>
              <td><span class="badge bg-secondary">{{ producto.categoria_nombre }}</span></td>
              <td>{{ producto.marca_nombre }}</td>
              <td>${{ Number(producto.precio_venta).toFixed(2) }}</td>
              <td>{{ formatFecha(producto.deleted_at) }}</td>
              <td>
                <span class="badge bg-dark">
                  {{ producto.deleted_by_username || 'Desconocido' }}
                </span>
              </td>
              <td>
                <button @click="restaurarProducto(producto.id)" class="btn btn-sm btn-success me-1" title="Restaurar producto">
                  ♻️ Restaurar
                </button>
                <button @click="verDetalles(producto)" class="btn btn-sm btn-info" title="Ver detalles">
                  👁️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal de Detalles -->
    <div v-if="mostrarDetalles && productoSeleccionado" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              📋 Detalles del Producto Eliminado
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="cerrarDetalles" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <p><strong>Código:</strong> {{ productoSeleccionado.codigo }}</p>
                <p><strong>Nombre:</strong> {{ productoSeleccionado.nombre }}</p>
                <p><strong>Categoría:</strong> {{ productoSeleccionado.categoria_nombre }}</p>
                <p><strong>Marca:</strong> {{ productoSeleccionado.marca_nombre }}</p>
              </div>
              <div class="col-md-6">
                <p><strong>Precio Compra:</strong> ${{ Number(productoSeleccionado.precio_compra).toFixed(2) }}</p>
                <p><strong>Precio Venta:</strong> ${{ Number(productoSeleccionado.precio_venta).toFixed(2) }}</p>
                <p><strong>Fecha Eliminación:</strong> {{ formatFecha(productoSeleccionado.deleted_at) }}</p>
                <p><strong>Eliminado Por:</strong> {{ productoSeleccionado.deleted_by_username || 'Desconocido' }}</p>
              </div>
            </div>
            <div v-if="productoSeleccionado.descripcion" class="mt-3">
              <p><strong>Descripción:</strong></p>
              <p class="text-muted">{{ productoSeleccionado.descripcion }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" @click="restaurarProducto(productoSeleccionado.id)">
              ♻️ Restaurar Producto
            </button>
            <button type="button" class="btn btn-secondary" @click="cerrarDetalles">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProductosEliminados',
  data() {
    return {
      productos: [],
      loading: true,
      mostrarDetalles: false,
      productoSeleccionado: null
    }
  },
  async created() {
    await this.cargarProductosEliminados()
  },
  methods: {
    async cargarProductosEliminados() {
      try {
        this.loading = true
        const response = await api.getProductosEliminados()

        // Los datos pueden venir en .data o .data.results (DRF pagination)
        this.productos = response.data.results || response.data || []

        console.log('Productos eliminados:', this.productos)
      } catch (error) {
        console.error('Error al cargar productos eliminados:', error)
        console.error('Detalles del error:', error.response?.data)
        alert('Error al cargar los productos eliminados. Abre la consola (F12) para ver detalles.')
      } finally {
        this.loading = false
      }
    },
    async restaurarProducto(id) {
      if (confirm('¿Estás seguro de restaurar este producto?\n\nEl producto volverá a estar activo y visible en el listado principal.')) {
        try {
          const response = await api.restaurarProducto(id)

          // Mostrar mensaje de éxito
          alert(response.data.message || 'Producto restaurado correctamente')

          // Recargar la lista
          await this.cargarProductosEliminados()

          // Cerrar modal si está abierto
          if (this.mostrarDetalles) {
            this.cerrarDetalles()
          }
        } catch (error) {
          console.error('Error al restaurar producto:', error)
          alert(error.response?.data?.error || 'Error al restaurar el producto')
        }
      }
    },
    verDetalles(producto) {
      this.productoSeleccionado = producto
      this.mostrarDetalles = true
    },
    cerrarDetalles() {
      this.mostrarDetalles = false
      this.productoSeleccionado = null
    },
    formatFecha(fecha) {
      if (!fecha) return 'N/A'
      const date = new Date(fecha)
      return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.table tbody tr {
  transition: background-color 0.2s;
}

.table tbody tr:hover {
  background-color: #f8d7da !important;
}

.modal {
  display: block;
}

.btn-close-white {
  filter: brightness(0) invert(1);
}
</style>
