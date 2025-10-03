<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">
      <div class="spinner-border"></div>
    </div>

    <div v-else-if="venta">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>📄 Detalle de Venta: {{ venta.numero_venta }}</h2>
        <router-link to="/ventas" class="btn btn-secondary">
          ← Volver
        </router-link>
      </div>

      <!-- Información General -->
      <div class="card mb-4">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0">Información General</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <p><strong>N° Venta:</strong> {{ venta.numero_venta }}</p>
              <p><strong>Cliente:</strong> {{ venta.cliente_nombre }}</p>
              <p><strong>Vendedor:</strong> {{ venta.vendedor_nombre }}</p>
            </div>
            <div class="col-md-6">
              <p><strong>Fecha:</strong> {{ formatFecha(venta.fecha_venta) }}</p>
              <p><strong>Tipo de Pago:</strong> {{ venta.tipo_pago }}</p>
              <p>
                <strong>Estado:</strong>
                <span class="badge" :class="getBadgeClass(venta.estado)">
                  {{ venta.estado }}
                </span>
              </p>
            </div>
          </div>
          <div v-if="venta.observaciones" class="mt-2">
            <p><strong>Observaciones:</strong> {{ venta.observaciones }}</p>
          </div>
        </div>
      </div>

      <!-- Detalle de Productos -->
      <div class="card mb-4">
        <div class="card-header bg-success text-white">
          <h5 class="mb-0">Productos</h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-striped">
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
            </table>
          </div>
        </div>
      </div>

      <!-- Resumen de Totales -->
      <div class="card mb-4">
        <div class="card-header bg-info text-white">
          <h5 class="mb-0">Resumen</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6 offset-md-6">
              <div class="d-flex justify-content-between mb-2">
                <span>Subtotal:</span>
                <strong>${{ Number(venta.subtotal).toFixed(2) }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2 text-danger">
                <span>Descuento:</span>
                <strong>-${{ Number(venta.descuento).toFixed(2) }}</strong>
              </div>
              <div class="d-flex justify-content-between mb-2">
                <span>Impuesto:</span>
                <strong>${{ Number(venta.impuesto).toFixed(2) }}</strong>
              </div>
              <hr>
              <div class="d-flex justify-content-between fs-4">
                <span><strong>TOTAL:</strong></span>
                <strong class="text-success">${{ Number(venta.total).toFixed(2) }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-danger">
      No se encontró la venta.
    </div>
  </div>
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
        alert('Error al cargar la venta')
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
      return new Date(fecha).toLocaleString('es-ES')
    }
  }
}
</script>
