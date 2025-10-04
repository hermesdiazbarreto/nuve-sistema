<template>
  <div class="container-fluid mt-4">
    <h2 class="mb-4">Dashboard - Sistema de Almacén</h2>

    <!-- Tarjetas de estadísticas -->
    <div class="row mb-4">
      <!-- Total Productos -->
      <div class="col-md-3 mb-3">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="card-title">Total Productos</h6>
                <h2 class="mb-0">{{ estadisticas.totalProductos }}</h2>
              </div>
              <div class="fs-1">📦</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Total Clientes -->
      <div class="col-md-3 mb-3">
        <div class="card text-white bg-success">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="card-title">Total Clientes</h6>
                <h2 class="mb-0">{{ estadisticas.totalClientes }}</h2>
              </div>
              <div class="fs-1">👥</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Ventas Hoy -->
      <div class="col-md-3 mb-3">
        <div class="card text-white bg-info">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="card-title">Ventas Hoy</h6>
                <h2 class="mb-0">{{ estadisticas.ventasHoy }}</h2>
              </div>
              <div class="fs-1">💰</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Productos Stock Bajo -->
      <div class="col-md-3 mb-3">
        <div class="card text-white bg-warning">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="card-title">Stock Bajo</h6>
                <h2 class="mb-0">{{ estadisticas.productosStockBajo }}</h2>
              </div>
              <div class="fs-1">⚠️</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sección de dos columnas -->
    <div class="row">
      <!-- Productos con stock bajo -->
      <div class="col-md-6 mb-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">⚠️ Productos con Stock Bajo</h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center">
              <div class="spinner-border spinner-border-sm" role="status"></div>
            </div>
            <div v-else-if="productosStockBajo.length === 0" class="text-muted text-center py-3">
              No hay productos con stock bajo
            </div>
            <div v-else class="table-responsive">
              <table class="table table-sm table-hover">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Talla</th>
                    <th>Color</th>
                    <th>Stock</th>
                    <th>Mínimo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="variante in productosStockBajo" :key="variante.id">
                    <td>{{ variante.producto_nombre }}</td>
                    <td>{{ variante.talla_nombre }}</td>
                    <td>{{ variante.color_nombre }}</td>
                    <td><span class="badge bg-danger">{{ variante.stock_actual }}</span></td>
                    <td>{{ variante.stock_minimo }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Últimas ventas -->
      <div class="col-md-6 mb-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">📊 Últimas Ventas</h5>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center">
              <div class="spinner-border spinner-border-sm" role="status"></div>
            </div>
            <div v-else-if="ultimasVentas.length === 0" class="text-muted text-center py-3">
              No hay ventas registradas
            </div>
            <div v-else class="table-responsive">
              <table class="table table-sm table-hover">
                <thead>
                  <tr>
                    <th>N° Venta</th>
                    <th>Tipo</th>
                    <th>Cliente</th>
                    <th>Total</th>
                    <th>Estado</th>
                    <th>Fecha</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="venta in ultimasVentas" :key="venta.id">
                    <td><small>{{ venta.numero_venta }}</small></td>
                    <td>
                      <span class="badge" :class="venta.tipo_movimiento === 'INGRESO' ? 'bg-success' : 'bg-danger'">
                        {{ venta.tipo_movimiento === 'INGRESO' ? '💰' : '💸' }}
                      </span>
                    </td>
                    <td><small>{{ venta.cliente_nombre }}</small></td>
                    <td><small><strong>${{ Number(venta.total).toFixed(2) }}</strong></small></td>
                    <td>
                      <span class="badge" :class="getBadgeClass(venta.estado)">
                        <small>{{ venta.estado }}</small>
                      </span>
                    </td>
                    <td><small>{{ formatFecha(venta.fecha_venta) }}</small></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Accesos rápidos -->
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">🚀 Accesos Rápidos</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-3 mb-2">
                <router-link to="/ventas/nueva" class="btn btn-primary w-100">
                  💳 Nueva Venta
                </router-link>
              </div>
              <div class="col-md-3 mb-2">
                <router-link to="/productos/nuevo" class="btn btn-success w-100">
                  ➕ Nuevo Producto
                </router-link>
              </div>
              <div class="col-md-3 mb-2">
                <router-link to="/adicionar-cliente" class="btn btn-info w-100">
                  👤 Nuevo Cliente
                </router-link>
              </div>
              <div class="col-md-3 mb-2">
                <router-link to="/productos" class="btn btn-warning w-100">
                  📦 Ver Productos
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'Dashboard',
  data() {
    return {
      loading: true,
      estadisticas: {
        totalProductos: 0,
        totalClientes: 0,
        ventasHoy: 0,
        productosStockBajo: 0
      },
      productosStockBajo: [],
      ultimasVentas: []
    }
  },
  async created() {
    await this.cargarDatos()
  },
  methods: {
    async cargarDatos() {
      try {
        this.loading = true

        // Cargar productos
        const productosRes = await api.getProductos()
        const productos = productosRes.data.results || productosRes.data || []
        this.estadisticas.totalProductos = productos.length

        // Cargar clientes
        const clientesRes = await api.getClientes()
        const clientes = clientesRes.data.results || clientesRes.data || []
        this.estadisticas.totalClientes = clientes.length

        // Cargar ventas
        const ventasRes = await api.getVentas()
        const ventas = ventasRes.data.results || ventasRes.data || []
        this.ultimasVentas = ventas.slice(0, 5) // Últimas 5 ventas

        // Contar ventas de hoy
        const hoy = new Date().toISOString().split('T')[0]
        this.estadisticas.ventasHoy = ventas.filter(v =>
          v.fecha_venta && v.fecha_venta.startsWith(hoy)
        ).length

        // Cargar variantes con stock bajo
        const variantesRes = await api.getProductoVariantes()
        const variantes = variantesRes.data.results || variantesRes.data || []
        this.productosStockBajo = variantes.filter(v =>
          v.stock_actual <= v.stock_minimo && v.activo
        ).slice(0, 10) // Top 10 con stock bajo

        this.estadisticas.productosStockBajo = this.productosStockBajo.length

      } catch (error) {
        console.error('Error al cargar datos del dashboard:', error)
        console.error('Detalles:', error.response?.data)
      } finally {
        this.loading = false
      }
    },
    getBadgeClass(estado) {
      const classes = {
        'PAGADO': 'bg-success',
        'PENDIENTE': 'bg-warning',
        'CANCELADO': 'bg-danger'
      }
      return classes[estado] || 'bg-secondary'
    },
    formatFecha(fecha) {
      if (!fecha) return ''
      const date = new Date(fecha)
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.fs-1 {
  font-size: 2.5rem;
}

.table-responsive {
  max-height: 300px;
  overflow-y: auto;
}

.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
