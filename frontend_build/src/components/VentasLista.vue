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
                <div class="btn-group btn-group-sm" role="group">
                  <router-link :to="`/ventas/${venta.id}`" class="btn btn-info" title="Ver detalles">
                    👁️
                  </router-link>
                  <button
                    @click="cancelarVenta(venta)"
                    class="btn btn-warning"
                    title="Cancelar venta"
                    :disabled="venta.estado === 'CANCELADO'"
                  >
                    ❌
                  </button>
                  <button @click="eliminarVenta(venta.id)" class="btn btn-danger" title="Eliminar">
                    🗑️
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="ventasFiltradas.length === 0" class="alert alert-info">
        No hay ventas registradas.
      </div>
    </div>

    <!-- Modal de confirmación para cancelar venta -->
    <div v-if="mostrarModalCancelar" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-warning text-dark">
            <h5 class="modal-title">⚠️ Cancelar Venta</h5>
            <button type="button" class="close" @click="cerrarModalCancelar" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p class="mb-3"><strong>¿Estás seguro de cancelar esta venta?</strong></p>
            <div class="alert alert-info" v-if="ventaSeleccionada">
              <p class="mb-1"><strong>N° Venta:</strong> {{ ventaSeleccionada.numero_venta }}</p>
              <p class="mb-1"><strong>Cliente:</strong> {{ ventaSeleccionada.cliente_nombre }}</p>
              <p class="mb-1"><strong>Total:</strong> ${{ Number(ventaSeleccionada.total).toFixed(2) }}</p>
              <p class="mb-0"><strong>Tipo:</strong>
                <span class="badge" :class="ventaSeleccionada.tipo_movimiento === 'INGRESO' ? 'bg-success' : 'bg-danger'">
                  {{ ventaSeleccionada.tipo_movimiento === 'INGRESO' ? '💰 Ingreso' : '💸 Egreso' }}
                </span>
              </p>
            </div>
            <div class="alert alert-success">
              <strong>✅ Stock automático:</strong> Si esta es una venta de INGRESO, el stock se restaurará automáticamente y se crearán movimientos de inventario de reversión.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalCancelar">No, mantener venta</button>
            <button type="button" class="btn btn-warning" @click="confirmarCancelarVenta">Sí, cancelar venta</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación para eliminar venta -->
    <div v-if="mostrarModalEliminar" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">🗑️ Eliminar Venta</h5>
            <button type="button" class="close" @click="cerrarModalEliminar" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p class="mb-3"><strong>¿Estás seguro de eliminar esta venta?</strong></p>
            <div class="alert alert-danger">
              <strong>⚠️ ADVERTENCIA:</strong> Esta acción NO se puede deshacer y eliminará:
              <ul class="mb-0 mt-2">
                <li>La venta completa</li>
                <li>Los detalles de productos</li>
                <li>Los movimientos de inventario relacionados</li>
              </ul>
            </div>
            <div class="alert alert-success">
              <strong>✅ Stock automático:</strong> Si es una venta de INGRESO, el stock se restaurará automáticamente antes de eliminar.
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalEliminar">No, cancelar</button>
            <button type="button" class="btn btn-danger" @click="confirmarEliminarVenta">Sí, eliminar permanentemente</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de éxito -->
    <div v-if="mostrarModalExito" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">✅ {{ mensajeExito }}</h5>
          </div>
          <div class="modal-body text-center py-4">
            <div style="font-size: 4rem;">✅</div>
            <p class="mt-3 mb-0">Operación completada exitosamente</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" @click="cerrarModalExito">Aceptar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de error -->
    <div v-if="mostrarModalError" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">❌ Error</h5>
            <button type="button" class="close" @click="cerrarModalError" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="text-center py-3">
              <div style="font-size: 4rem;">❌</div>
              <p class="mt-3 mb-0">{{ mensajeError }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalError">Cerrar</button>
          </div>
        </div>
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
      },
      mostrarModalCancelar: false,
      mostrarModalEliminar: false,
      mostrarModalExito: false,
      mostrarModalError: false,
      ventaSeleccionada: null,
      ventaIdEliminar: null,
      mensajeExito: '',
      mensajeError: ''
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
    },
    cancelarVenta(venta) {
      if (venta.estado === 'CANCELADO') {
        this.mensajeError = 'Esta venta ya está cancelada'
        this.mostrarModalError = true
        return
      }
      this.ventaSeleccionada = venta
      this.mostrarModalCancelar = true
    },
    cerrarModalCancelar() {
      this.mostrarModalCancelar = false
      this.ventaSeleccionada = null
    },
    async confirmarCancelarVenta() {
      try {
        await api.updateVenta(this.ventaSeleccionada.id, {
          ...this.ventaSeleccionada,
          estado: 'CANCELADO'
        })
        this.cerrarModalCancelar()
        this.mensajeExito = 'Venta cancelada correctamente'
        this.mostrarModalExito = true
        await this.cargarVentas()
      } catch (error) {
        console.error('Error al cancelar venta:', error)
        this.cerrarModalCancelar()
        this.mensajeError = error.response?.data?.detail || error.message || 'Error al cancelar la venta'
        this.mostrarModalError = true
      }
    },
    eliminarVenta(ventaId) {
      this.ventaIdEliminar = ventaId
      this.mostrarModalEliminar = true
    },
    cerrarModalEliminar() {
      this.mostrarModalEliminar = false
      this.ventaIdEliminar = null
    },
    async confirmarEliminarVenta() {
      try {
        await api.deleteVenta(this.ventaIdEliminar)
        this.cerrarModalEliminar()
        this.mensajeExito = 'Venta eliminada correctamente'
        this.mostrarModalExito = true
        await this.cargarVentas()
      } catch (error) {
        console.error('Error al eliminar venta:', error)
        this.cerrarModalEliminar()
        this.mensajeError = error.response?.data?.detail || error.message || 'Error al eliminar la venta'
        this.mostrarModalError = true
      }
    },
    cerrarModalExito() {
      this.mostrarModalExito = false
      this.mensajeExito = ''
    },
    cerrarModalError() {
      this.mostrarModalError = false
      this.mensajeError = ''
    }
  }
}
</script>
