<template>
  <v-container class="mt-4">
    <div v-if="loading" class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="venta">
      <div class="d-flex justify-space-between align-center mb-4">
        <h2>Detalle de Venta: {{ venta.numero_venta }}</h2>
        <v-btn :to="'/ventas'" color="secondary">
          <v-icon left>mdi-arrow-left</v-icon> Volver
        </v-btn>
      </div>

      <!-- Información General -->
      <v-card elevation="3" class="mb-4">
        <v-card-title class="bg-primary">
          <span class="text-white">Información General</span>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <p><strong>N° Venta:</strong> {{ venta.numero_venta }}</p>
              <p><strong>Cliente:</strong> {{ venta.cliente_nombre }}</p>
              <p><strong>Vendedor:</strong> {{ venta.vendedor_nombre }}</p>
            </v-col>
            <v-col cols="12" md="6">
              <p><strong>Fecha:</strong> {{ formatFecha(venta.fecha_venta) }}</p>
              <p><strong>Tipo de Pago:</strong> {{ venta.tipo_pago }}</p>
              <p>
                <strong>Estado:</strong>
                <v-chip
                  :color="getBadgeClass(venta.estado)"
                  size="small"
                  variant="flat"
                  class="ml-2"
                >
                  {{ venta.estado }}
                </v-chip>
              </p>
            </v-col>
          </v-row>
          <div v-if="venta.observaciones" class="mt-2">
            <p><strong>Observaciones:</strong> {{ venta.observaciones }}</p>
          </div>
        </v-card-text>
      </v-card>

      <!-- Detalle de Productos -->
      <v-card elevation="3" class="mb-4">
        <v-card-title class="bg-success">
          <span class="text-white">Productos</span>
        </v-card-title>
        <v-card-text>
          <v-table hover>
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Precio Unitario</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="detalle in venta.detalles" :key="detalle.id">
                <td>{{ detalle.producto_info }}</td>
                <td>{{ detalle.cantidad }}</td>
                <td>${{ Number(detalle.precio_unitario).toFixed(2) }}</td>
                <td>${{ Number(detalle.subtotal).toFixed(2) }}</td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>

      <!-- Resumen de Totales -->
      <v-card elevation="3" class="mb-4">
        <v-card-title class="bg-info">
          <span class="text-white">Resumen</span>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6" offset-md="6">
              <div class="d-flex justify-space-between mb-2">
                <span>Subtotal:</span>
                <strong>${{ Number(venta.subtotal).toFixed(2) }}</strong>
              </div>
              <div class="d-flex justify-space-between mb-2 text-error">
                <span>Descuento:</span>
                <strong>-${{ Number(venta.descuento).toFixed(2) }}</strong>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span>Impuesto:</span>
                <strong>${{ Number(venta.impuesto).toFixed(2) }}</strong>
              </div>
              <v-divider class="my-2"></v-divider>
              <div class="d-flex justify-space-between text-h5">
                <span><strong>TOTAL:</strong></span>
                <strong class="text-success">${{ Number(venta.total).toFixed(2) }}</strong>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

    <v-alert v-else type="error" variant="tonal">
      No se encontró la venta.
    </v-alert>
  </v-container>
</template>

<script>
import api from '../services/api'

export default {
  name: 'VentaDetalle',
  data() {
    return {
      venta: null,
      loading: true
    }
  },
  async created() {
    await this.cargarVenta()
  },
  methods: {
    async cargarVenta() {
      try {
        this.loading = true
        const id = this.$route.params.id
        const response = await api.getVenta(id)
        this.venta = response.data
      } catch (error) {
        console.error('Error:', error)
      } finally {
        this.loading = false
      }
    },
    getBadgeClass(estado) {
      const classes = {
        'PAGADO': 'success',
        'PENDIENTE': 'warning',
        'CANCELADO': 'error'
      }
      return classes[estado] || 'secondary'
    },
    formatFecha(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleString('es-ES')
    }
  }
}
</script>
