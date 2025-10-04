<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>💰 Ventas</h2>
      <router-link to="/ventas/nueva" class="btn btn-primary">
        ➕ Nueva Venta
      </router-link>
    </div>

    <div class="card mb-4">
      <div class="card-header bg-primary text-white">
        <h6 class="mb-0">🔍 Filtros</h6>
      </div>
      <div class="card-body">
        <div class="row align-items-end g-3">
          <div class="col-md-3">
            <label class="form-label fw-bold">Estado</label>
            <select v-model="filtro.estado" @change="aplicarFiltros" class="form-select">
              <option value="">Todos</option>
              <option value="PAGADO">Pagado</option>
              <option value="PENDIENTE">Pendiente</option>
              <option value="CANCELADO">Cancelado</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label fw-bold">Fecha Desde</label>
            <input v-model="filtro.fecha_desde" type="date" class="form-control" @change="aplicarFiltros">
          </div>
          <div class="col-md-3">
            <label class="form-label fw-bold">Fecha Hasta</label>
            <input v-model="filtro.fecha_hasta" type="date" class="form-control" @change="aplicarFiltros">
          </div>
          <div class="col-md-3">
            <button @click="limpiarFiltros" class="btn btn-secondary w-100">🔄 Limpiar Filtros</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border"></div>
    </div>

    <div v-else>
      <div class="row mb-3">
        <div class="col-md-3">
          <div class="card bg-success text-white">
            <div class="card-body">
              <h6>Total Ventas</h6>
              <h4>${{ totalVentas.toFixed(2) }}</h4>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-info text-white">
            <div class="card-body">
              <h6>Cantidad</h6>
              <h4>{{ ventasFiltradas.length }}</h4>
            </div>
          </div>
        </div>
      </div>

      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>N° Venta</th>
              <th>Tipo</th>
              <th>Cliente</th>
              <th>Vendedor</th>
              <th>Fecha</th>
              <th>Subtotal</th>
              <th>Descuento</th>
              <th>Total</th>
              <th>Tipo Pago</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="venta in ventasFiltradas" :key="venta.id">
              <td><strong>{{ venta.numero_venta }}</strong></td>
              <td>
                <span class="badge" :class="venta.tipo_movimiento === 'INGRESO' ? 'bg-success' : 'bg-danger'">
                  {{ venta.tipo_movimiento === 'INGRESO' ? '💰 Ingreso' : '💸 Egreso' }}
                </span>
              </td>
              <td>{{ venta.cliente_nombre }}</td>
              <td>{{ venta.vendedor_nombre }}</td>
              <td>{{ formatFecha(venta.fecha_venta) }}</td>
              <td>${{ Number(venta.subtotal).toFixed(2) }}</td>
              <td>${{ Number(venta.descuento).toFixed(2) }}</td>
              <td><strong>${{ Number(venta.total).toFixed(2) }}</strong></td>
              <td>{{ venta.tipo_pago }}</td>
              <td>
                <span class="badge" :class="getBadgeClass(venta.estado)">
                  {{ venta.estado }}
                </span>
              </td>
              <td>
                <router-link :to="`/ventas/${venta.id}`" class="btn btn-sm btn-info">
                  👁️ Ver
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="ventasFiltradas.length === 0" class="alert alert-info">
        No hay ventas registradas.
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'VentasLista',
  data() {
    return {
      ventas: [],
      ventasFiltradas: [],
      loading: true,
      filtro: {
        estado: '',
        fecha_desde: '',
        fecha_hasta: ''
      }
    }
  },
  computed: {
    totalVentas() {
      return this.ventasFiltradas.reduce((sum, v) => sum + Number(v.total), 0)
    }
  },
  async created() {
    await this.cargarVentas()
  },
  methods: {
    async cargarVentas() {
      try {
        this.loading = true
        const response = await api.getVentas()
        const ventas = response.data.results || response.data || []
        this.ventas = ventas
        this.ventasFiltradas = this.ventas
      } catch (error) {
        console.error('Error:', error)
        alert('Error al cargar ventas')
      } finally {
        this.loading = false
      }
    },
    aplicarFiltros() {
      let filtradas = [...this.ventas]

      if (this.filtro.estado) {
        filtradas = filtradas.filter(v => v.estado === this.filtro.estado)
      }

      if (this.filtro.fecha_desde) {
        filtradas = filtradas.filter(v =>
          new Date(v.fecha_venta) >= new Date(this.filtro.fecha_desde)
        )
      }

      if (this.filtro.fecha_hasta) {
        const fechaHasta = new Date(this.filtro.fecha_hasta)
        fechaHasta.setHours(23, 59, 59)
        filtradas = filtradas.filter(v =>
          new Date(v.fecha_venta) <= fechaHasta
        )
      }

      this.ventasFiltradas = filtradas
    },
    limpiarFiltros() {
      this.filtro = {
        estado: '',
        fecha_desde: '',
        fecha_hasta: ''
      }
      this.ventasFiltradas = this.ventas
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
