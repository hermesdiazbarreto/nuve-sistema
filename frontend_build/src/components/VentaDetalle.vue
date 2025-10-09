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
        <v-card-text class="pa-0">
          <!-- Vista Desktop: Tabla -->
          <v-table v-if="$vuetify.display.mdAndUp" hover>
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
                <td><span class="nombre-producto">{{ detalle.producto_info }}</span></td>
                <td>{{ detalle.cantidad }}</td>
                <td>{{ formatearPrecio(detalle.precio_unitario) }}</td>
                <td>{{ formatearPrecio(detalle.subtotal) }}</td>
              </tr>
            </tbody>
          </v-table>

          <!-- Vista Móvil: Cards -->
          <div v-else class="pa-2">
            <v-card
              v-for="detalle in venta.detalles"
              :key="detalle.id"
              class="mb-2"
              variant="outlined"
            >
              <v-card-text class="pa-3">
                <div class="nombre-producto text-body-2 font-weight-bold mb-2">
                  {{ detalle.producto_info }}
                </div>
                <v-divider class="my-2"></v-divider>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Cantidad:</span>
                  <span class="text-body-2 font-weight-medium">{{ detalle.cantidad }}</span>
                </div>
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-caption">Precio Unit.:</span>
                  <span class="text-body-2">{{ formatearPrecio(detalle.precio_unitario) }}</span>
                </div>
                <div class="d-flex justify-space-between">
                  <span class="text-caption font-weight-bold">Subtotal:</span>
                  <span class="text-body-1 font-weight-bold text-primary">{{ formatearPrecio(detalle.subtotal) }}</span>
                </div>
              </v-card-text>
            </v-card>
          </div>
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
                <strong>{{ formatearPrecio(venta.subtotal) }}</strong>
              </div>
              <div class="d-flex justify-space-between mb-2 text-error">
                <span>Descuento:</span>
                <strong>-{{ formatearPrecio(venta.descuento) }}</strong>
              </div>
              <div class="d-flex justify-space-between mb-2">
                <span>Impuesto:</span>
                <strong>{{ formatearPrecio(venta.impuesto) }}</strong>
              </div>
              <v-divider class="my-2"></v-divider>
              <div class="d-flex justify-space-between text-h5 mb-3">
                <span><strong>TOTAL:</strong></span>
                <strong class="text-primary">{{ formatearPrecio(venta.total) }}</strong>
              </div>

              <!-- Información de Pagos (si hay abono o pendiente) -->
              <div v-if="venta.estado === 'ABONO' || venta.saldo_pendiente > 0">
                <v-divider class="my-3"></v-divider>
                <div class="d-flex justify-space-between mb-2">
                  <span class="text-success">
                    <v-icon size="small" color="success">mdi-cash-check</v-icon>
                    Monto Abonado:
                  </span>
                  <strong class="text-success">{{ formatearPrecio(venta.monto_abonado || 0) }}</strong>
                </div>
                <div class="d-flex justify-space-between mb-2">
                  <span :class="venta.saldo_pendiente > 0 ? 'text-warning' : 'text-grey'">
                    <v-icon size="small" :color="venta.saldo_pendiente > 0 ? 'warning' : 'grey'">
                      mdi-cash-clock
                    </v-icon>
                    Saldo Pendiente:
                  </span>
                  <strong :class="venta.saldo_pendiente > 0 ? 'text-warning text-h6' : 'text-grey'">
                    {{ formatearPrecio(venta.saldo_pendiente || 0) }}
                  </strong>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Historial de Pagos (si existen) -->
      <v-card v-if="venta.pagos && venta.pagos.length > 0" elevation="3" class="mb-4">
        <v-card-title class="bg-success">
          <span class="text-white">
            <v-icon left color="white">mdi-cash-multiple</v-icon>
            Historial de Pagos
          </span>
        </v-card-title>
        <v-card-text class="pa-0">
          <!-- Vista Desktop: Tabla -->
          <v-table v-if="$vuetify.display.mdAndUp" hover>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Monto</th>
                <th>Tipo de Pago</th>
                <th>Usuario</th>
                <th>Observaciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pago in venta.pagos" :key="pago.id">
                <td>{{ formatFecha(pago.fecha_pago) }}</td>
                <td class="text-success font-weight-bold">{{ formatearPrecio(pago.monto) }}</td>
                <td>
                  <v-chip size="small" variant="outlined">{{ pago.tipo_pago }}</v-chip>
                </td>
                <td>{{ pago.usuario_nombre }}</td>
                <td>{{ pago.observaciones || '-' }}</td>
              </tr>
            </tbody>
          </v-table>

          <!-- Vista Móvil: Cards -->
          <div v-else class="pa-2">
            <v-card
              v-for="pago in venta.pagos"
              :key="pago.id"
              class="mb-2"
              variant="outlined"
            >
              <v-card-text class="pa-3">
                <div class="d-flex justify-space-between align-center mb-2">
                  <div class="text-caption text-medium-emphasis">
                    {{ formatFecha(pago.fecha_pago) }}
                  </div>
                  <v-chip size="small" variant="outlined">{{ pago.tipo_pago }}</v-chip>
                </div>
                <v-divider class="my-2"></v-divider>
                <div class="d-flex justify-space-between mb-2">
                  <span class="text-body-2">Monto:</span>
                  <span class="text-h6 font-weight-bold text-success">{{ formatearPrecio(pago.monto) }}</span>
                </div>
                <div class="text-caption mb-1">
                  <strong>Usuario:</strong> {{ pago.usuario_nombre }}
                </div>
                <div v-if="pago.observaciones" class="text-caption">
                  <strong>Observaciones:</strong> {{ pago.observaciones }}
                </div>
              </v-card-text>
            </v-card>
          </div>

          <!-- Resumen de pagos -->
          <v-alert type="info" variant="tonal" class="mt-4">
            <div class="d-flex justify-space-between">
              <span><strong>Total de Pagos Registrados:</strong></span>
              <span><strong>{{ venta.pagos.length }}</strong></span>
            </div>
            <div class="d-flex justify-space-between mt-2">
              <span><strong>Monto Total Abonado:</strong></span>
              <span class="text-success"><strong>{{ formatearPrecio(venta.monto_abonado || 0) }}</strong></span>
            </div>
          </v-alert>
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
import formatoPrecio from '../mixins/formatoPrecio'

export default {
  name: 'VentaDetalle',
  mixins: [formatoPrecio],
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
        'ABONO': 'info',
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
