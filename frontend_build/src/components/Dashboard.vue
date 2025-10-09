<template>
  <div>
    <!-- Header -->
    <v-row align="center" class="mb-6">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold">
          <v-icon large color="primary" class="mr-2">mdi-view-dashboard</v-icon>
          Dashboard - Sistema de Almacén
        </h1>
      </v-col>
    </v-row>

    <!-- Tarjetas de estadísticas -->
    <v-row class="mb-6">
      <!-- Total Productos -->
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Total Productos</div>
                <div class="text-h4 font-weight-bold">{{ estadisticas.totalProductos }}</div>
              </div>
              <v-icon size="64" class="opacity-75">mdi-package-variant</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Total Clientes -->
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Total Clientes</div>
                <div class="text-h4 font-weight-bold">{{ estadisticas.totalClientes }}</div>
              </div>
              <v-icon size="64" class="opacity-75">mdi-account-group</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Ventas Hoy -->
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Ventas Hoy</div>
                <div class="text-h4 font-weight-bold">{{ estadisticas.ventasHoy }}</div>
              </div>
              <v-icon size="64" class="opacity-75">mdi-cash-multiple</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Productos Stock Bajo -->
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Stock Bajo</div>
                <div class="text-h4 font-weight-bold">{{ estadisticas.productosStockBajo }}</div>
              </div>
              <v-icon size="64" class="opacity-75">mdi-alert</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Sección de dos columnas -->
    <v-row>
      <!-- Productos con stock bajo -->
      <v-col cols="12" md="6">
        <v-card elevation="3">
          <v-card-title class="bg-warning">
            <v-icon left color="white">mdi-alert-circle</v-icon>
            <span class="text-white">Productos con Stock Bajo</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-0">
            <v-progress-linear v-if="loading" indeterminate color="warning"></v-progress-linear>

            <v-alert v-else-if="productosStockBajo.length === 0" type="success" variant="tonal" class="ma-4">
              No hay productos con stock bajo
            </v-alert>

            <v-table v-else density="compact" class="stock-bajo-table">
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
                  <td>
                    <v-chip color="error" size="small" variant="flat">
                      {{ variante.stock_actual }}
                    </v-chip>
                  </td>
                  <td>{{ variante.stock_minimo }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Últimas ventas -->
      <v-col cols="12" md="6">
        <v-card elevation="3">
          <v-card-title class="bg-primary">
            <v-icon left color="white">mdi-chart-line</v-icon>
            <span class="text-white">Últimas Ventas</span>
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text class="pa-0">
            <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

            <v-alert v-else-if="ultimasVentas.length === 0" type="info" variant="tonal" class="ma-4">
              No hay ventas registradas
            </v-alert>

            <v-table v-else density="compact">
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
                  <td><span class="text-caption">{{ venta.numero_venta }}</span></td>
                  <td>
                    <v-chip
                      :color="venta.tipo_movimiento === 'INGRESO' ? 'success' : 'error'"
                      size="x-small"
                      variant="flat"
                    >
                      <v-icon left size="x-small">
                        {{ venta.tipo_movimiento === 'INGRESO' ? 'mdi-cash-plus' : 'mdi-cash-minus' }}
                      </v-icon>
                    </v-chip>
                  </td>
                  <td><span class="text-caption">{{ venta.cliente_nombre }}</span></td>
                  <td><span class="text-caption font-weight-bold">S/ {{ formatPrecio(venta.total) }}</span></td>
                  <td>
                    <v-chip :color="getChipColor(venta.estado)" size="x-small" variant="flat">
                      {{ venta.estado }}
                    </v-chip>
                  </td>
                  <td><span class="text-caption">{{ formatFecha(venta.fecha_venta) }}</span></td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Accesos rápidos -->
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-title>
            <v-icon left>mdi-rocket-launch</v-icon>
            Accesos Rápidos
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn color="primary" block size="large" :to="'/ventas/nueva'">
                  <v-icon left>mdi-point-of-sale</v-icon>
                  Nueva Venta
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn color="success" block size="large" :to="'/productos/nuevo'">
                  <v-icon left>mdi-plus-circle</v-icon>
                  Nuevo Producto
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn color="info" block size="large" :to="'/adicionar-cliente'">
                  <v-icon left>mdi-account-plus</v-icon>
                  Nuevo Cliente
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn color="warning" block size="large" :to="'/productos'">
                  <v-icon left>mdi-package-variant</v-icon>
                  Ver Productos
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
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
    getChipColor(estado) {
      const colors = {
        'PAGADO': 'success',
        'PENDIENTE': 'warning',
        'CANCELADO': 'error'
      }
      return colors[estado] || 'grey'
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
    },
    formatPrecio(precio) {
      const numero = Number(precio)
      return numero.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }
  }
}
</script>

<style scoped>
.stock-bajo-table {
  max-height: 400px;
  overflow-y: auto;
}

.opacity-75 {
  opacity: 0.75;
}
</style>
