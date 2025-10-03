<template>
  <div class="container mt-4">
    <h2>📋 Movimientos de Inventario</h2>

    <div class="card mb-4">
      <div class="card-header bg-primary text-white">
        <h6 class="mb-0">🔍 Filtros</h6>
      </div>
      <div class="card-body">
        <div class="row align-items-end g-3">
          <div class="col-md-3">
            <label class="form-label fw-bold">Tipo de Movimiento</label>
            <select v-model="filtro.tipo" @change="aplicarFiltros" class="form-select">
              <option value="">Todos</option>
              <option value="ENTRADA">Entrada</option>
              <option value="SALIDA">Salida</option>
              <option value="AJUSTE">Ajuste</option>
              <option value="DEVOLUCION">Devolución</option>
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
            <button @click="limpiarFiltros" class="btn btn-secondary w-100">
              🔄 Limpiar Filtros
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border"></div>
    </div>

    <div v-else class="mt-4">
      <div class="table-responsive">
        <table class="table table-striped table-hover table-sm">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Fecha</th>
              <th>Tipo</th>
              <th>Producto</th>
              <th>Cantidad</th>
              <th>Stock Anterior</th>
              <th>Stock Nuevo</th>
              <th>Motivo</th>
              <th>Usuario</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mov in movimientosFiltrados" :key="mov.id">
              <td>{{ mov.id }}</td>
              <td>{{ formatFecha(mov.fecha_movimiento) }}</td>
              <td>
                <span class="badge" :class="getBadgeClass(mov.tipo_movimiento)">
                  {{ mov.tipo_movimiento }}
                </span>
              </td>
              <td>{{ mov.producto_info }}</td>
              <td :class="getCantidadClass(mov.tipo_movimiento)">
                {{ getTipoMovimiento(mov.tipo_movimiento) }}{{ mov.cantidad }}
              </td>
              <td>{{ mov.stock_anterior }}</td>
              <td>{{ mov.stock_nuevo }}</td>
              <td>{{ mov.motivo }}</td>
              <td>{{ mov.usuario_nombre }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="movimientosFiltrados.length === 0" class="alert alert-info">
        No hay movimientos de inventario.
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'MovimientosLista',
  data() {
    return {
      movimientos: [],
      movimientosFiltrados: [],
      loading: true,
      filtro: {
        tipo: '',
        fecha_desde: '',
        fecha_hasta: ''
      }
    }
  },
  async created() {
    await this.cargarMovimientos()
  },
  methods: {
    async cargarMovimientos() {
      try {
        this.loading = true
        const response = await api.getMovimientos()
        const movimientos = response.data.results || response.data || []
        this.movimientos = movimientos
        this.movimientosFiltrados = this.movimientos
      } catch (error) {
        console.error('Error:', error)
        alert('Error al cargar movimientos')
      } finally {
        this.loading = false
      }
    },
    aplicarFiltros() {
      let filtrados = [...this.movimientos]

      if (this.filtro.tipo) {
        filtrados = filtrados.filter(m => m.tipo_movimiento === this.filtro.tipo)
      }

      if (this.filtro.fecha_desde) {
        filtrados = filtrados.filter(m =>
          new Date(m.fecha_movimiento) >= new Date(this.filtro.fecha_desde)
        )
      }

      if (this.filtro.fecha_hasta) {
        const fechaHasta = new Date(this.filtro.fecha_hasta)
        fechaHasta.setHours(23, 59, 59)
        filtrados = filtrados.filter(m =>
          new Date(m.fecha_movimiento) <= fechaHasta
        )
      }

      this.movimientosFiltrados = filtrados
    },
    limpiarFiltros() {
      this.filtro = {
        tipo: '',
        fecha_desde: '',
        fecha_hasta: ''
      }
      this.movimientosFiltrados = this.movimientos
    },
    getBadgeClass(tipo) {
      const classes = {
        'ENTRADA': 'bg-success',
        'SALIDA': 'bg-danger',
        'AJUSTE': 'bg-warning',
        'DEVOLUCION': 'bg-info'
      }
      return classes[tipo] || 'bg-secondary'
    },
    getCantidadClass(tipo) {
      return tipo === 'ENTRADA' || tipo === 'DEVOLUCION' ? 'text-success fw-bold' : 'text-danger fw-bold'
    },
    getTipoMovimiento(tipo) {
      return tipo === 'ENTRADA' || tipo === 'DEVOLUCION' ? '+' : '-'
    },
    formatFecha(fecha) {
      if (!fecha) return ''
      return new Date(fecha).toLocaleString('es-ES')
    }
  }
}
</script>
