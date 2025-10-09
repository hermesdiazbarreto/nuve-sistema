<template>
  <div>
    <!-- Header -->
    <v-row align="center" class="mb-6">
      <v-col cols="12" md="6">
        <h1 class="text-h4 font-weight-bold">
          <v-icon large color="success" class="mr-2">mdi-cash-multiple</v-icon>
          Ventas
        </h1>
      </v-col>
      <v-col cols="12" md="6" class="text-md-right">
        <v-btn color="primary" :to="'/ventas/nueva'">
          <v-icon left>mdi-plus</v-icon>
          Nueva Venta
        </v-btn>
      </v-col>
    </v-row>

    <!-- Filtros Card -->
    <v-card elevation="3" class="mb-4">
      <v-card-title class="bg-primary">
        <v-icon left color="white">mdi-filter</v-icon>
        <span class="text-white">Filtros</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <v-select
              v-model="filtro.estado"
              :items="['Todos', 'PAGADO', 'PENDIENTE', 'CANCELADO']"
              label="Estado"
              variant="outlined"
              density="compact"
              @update:model-value="aplicarFiltros"
            ></v-select>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filtro.fecha_desde"
              type="date"
              label="Fecha Desde"
              variant="outlined"
              density="compact"
              @change="aplicarFiltros"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-text-field
              v-model="filtro.fecha_hasta"
              type="date"
              label="Fecha Hasta"
              variant="outlined"
              density="compact"
              @change="aplicarFiltros"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <v-btn color="grey" variant="outlined" block @click="limpiarFiltros">
              <v-icon left>mdi-refresh</v-icon>
              Limpiar Filtros
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Progress bar -->
    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Stats Cards -->
    <v-row v-if="!loading" class="mb-4">
      <v-col cols="12" sm="6">
        <v-card color="success" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Total Ventas</div>
                <div class="text-h4 font-weight-bold">S/ {{ formatPrecio(totalVentas) }}</div>
              </div>
              <v-icon size="48">mdi-currency-usd</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6">
        <v-card color="info" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Cantidad de Ventas</div>
                <div class="text-h4 font-weight-bold">{{ ventasFiltradas.length }}</div>
              </div>
              <v-icon size="48">mdi-counter</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Data Table -->
    <v-card v-if="!loading" elevation="3">
      <v-card-title class="d-flex align-center pa-4">
        <v-icon class="mr-2">mdi-table</v-icon>
        Listado de Ventas
      </v-card-title>
      <v-divider></v-divider>

      <v-data-table
        :headers="headers"
        :items="ventasFiltradas"
        :items-per-page="10"
        items-per-page-text="Ventas por página"
        no-data-text="No hay ventas registradas"
        class="elevation-0"
      >
        <!-- N° Venta -->
        <template #item.numero_venta="{ item }">
          <span class="font-weight-bold">{{ item.numero_venta }}</span>
        </template>

        <!-- Tipo Movimiento -->
        <template #item.tipo_movimiento="{ item }">
          <v-chip
            :color="item.tipo_movimiento === 'INGRESO' ? 'success' : 'error'"
            size="small"
            variant="flat"
          >
            <v-icon left size="small">
              {{ item.tipo_movimiento === 'INGRESO' ? 'mdi-cash-plus' : 'mdi-cash-minus' }}
            </v-icon>
            {{ item.tipo_movimiento === 'INGRESO' ? 'Ingreso' : 'Egreso' }}
          </v-chip>
        </template>

        <!-- Subtotal -->
        <template #item.subtotal="{ item }">
          <span>S/ {{ formatPrecio(item.subtotal) }}</span>
        </template>

        <!-- Descuento -->
        <template #item.descuento="{ item }">
          <span>S/ {{ formatPrecio(item.descuento) }}</span>
        </template>

        <!-- Total -->
        <template #item.total="{ item }">
          <span class="font-weight-bold">S/ {{ formatPrecio(item.total) }}</span>
        </template>

        <!-- Estado -->
        <template #item.estado="{ item }">
          <v-chip :color="getChipColor(item.estado)" size="small" variant="flat">
            {{ item.estado }}
          </v-chip>
        </template>

        <!-- Fecha -->
        <template #item.fecha_venta="{ item }">
          <span class="text-caption">{{ formatFecha(item.fecha_venta) }}</span>
        </template>

        <!-- Acciones -->
        <template #item.actions="{ item }">
          <v-btn
            icon
            size="small"
            color="info"
            variant="text"
            :to="`/ventas/${item.id}`"
            title="Ver detalles"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            color="warning"
            variant="text"
            :disabled="item.estado === 'CANCELADO'"
            @click="cancelarVenta(item)"
            title="Cancelar venta"
          >
            <v-icon>mdi-cancel</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            color="error"
            variant="text"
            @click="eliminarVenta(item.id)"
            title="Eliminar"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Modal para Cancelar Venta -->
    <v-dialog v-model="mostrarModalCancelar" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 warning white--text">
          <v-icon left color="white">mdi-alert</v-icon>
          Cancelar Venta
        </v-card-title>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">¿Estás seguro de cancelar esta venta?</p>

          <v-alert v-if="ventaSeleccionada" type="info" variant="tonal" class="mb-4">
            <div><strong>N° Venta:</strong> {{ ventaSeleccionada.numero_venta }}</div>
            <div><strong>Cliente:</strong> {{ ventaSeleccionada.cliente_nombre }}</div>
            <div><strong>Total:</strong> S/ {{ formatPrecio(ventaSeleccionada.total) }}</div>
            <div>
              <strong>Tipo:</strong>
              <v-chip
                :color="ventaSeleccionada.tipo_movimiento === 'INGRESO' ? 'success' : 'error'"
                size="x-small"
                class="ml-2"
              >
                {{ ventaSeleccionada.tipo_movimiento === 'INGRESO' ? 'Ingreso' : 'Egreso' }}
              </v-chip>
            </div>
          </v-alert>

          <v-alert type="success" variant="tonal">
            <v-alert-title>
              <v-icon left>mdi-check-circle</v-icon>
              Stock automático
            </v-alert-title>
            Si esta es una venta de INGRESO, el stock se restaurará automáticamente y se crearán movimientos de inventario de reversión.
          </v-alert>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarModalCancelar">
            No, mantener venta
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="warning" @click="confirmarCancelarVenta">
            Sí, cancelar venta
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Modal para Eliminar Venta -->
    <v-dialog v-model="mostrarModalEliminar" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 error white--text">
          <v-icon left color="white">mdi-delete</v-icon>
          Eliminar Venta
        </v-card-title>
        <v-card-text class="pa-6">
          <p class="text-h6 mb-4">¿Estás seguro de eliminar esta venta?</p>

          <v-alert type="error" variant="tonal" class="mb-4">
            <v-alert-title>
              <v-icon left>mdi-alert</v-icon>
              ADVERTENCIA
            </v-alert-title>
            Esta acción NO se puede deshacer y eliminará:
            <ul class="mt-2">
              <li>La venta completa</li>
              <li>Los detalles de productos</li>
              <li>Los movimientos de inventario relacionados</li>
            </ul>
          </v-alert>

          <v-alert type="success" variant="tonal">
            <v-alert-title>
              <v-icon left>mdi-check-circle</v-icon>
              Stock automático
            </v-alert-title>
            Si es una venta de INGRESO, el stock se restaurará automáticamente antes de eliminar.
          </v-alert>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarModalEliminar">
            No, cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="confirmarEliminarVenta">
            Sí, eliminar permanentemente
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar de Éxito -->
    <v-snackbar v-model="mostrarModalExito" color="success" timeout="3000" top>
      {{ mensajeExito }}
      <template #actions>
        <v-btn variant="text" @click="mostrarModalExito = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Snackbar de Error -->
    <v-snackbar v-model="mostrarModalError" color="error" timeout="5000" top>
      {{ mensajeError }}
      <template #actions>
        <v-btn variant="text" @click="mostrarModalError = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
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
        estado: 'Todos',
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
      mensajeError: '',
      headers: [
        { title: 'N° Venta', key: 'numero_venta', sortable: true },
        { title: 'Tipo', key: 'tipo_movimiento', sortable: true },
        { title: 'Cliente', key: 'cliente_nombre', sortable: true },
        { title: 'Vendedor', key: 'vendedor_nombre', sortable: true },
        { title: 'Fecha', key: 'fecha_venta', sortable: true },
        { title: 'Subtotal', key: 'subtotal', sortable: true },
        { title: 'Descuento', key: 'descuento', sortable: true },
        { title: 'Total', key: 'total', sortable: true },
        { title: 'Tipo Pago', key: 'tipo_pago', sortable: true },
        { title: 'Estado', key: 'estado', sortable: true },
        { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
      ],
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
        this.mensajeError = 'Error al cargar ventas'
        this.mostrarModalError = true
      } finally {
        this.loading = false
      }
    },
    aplicarFiltros() {
      let filtradas = [...this.ventas]

      if (this.filtro.estado && this.filtro.estado !== 'Todos') {
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
        estado: 'Todos',
        fecha_desde: '',
        fecha_hasta: ''
      }
      this.ventasFiltradas = this.ventas
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
      return new Date(fecha).toLocaleString('es-ES')
    },
    formatPrecio(precio) {
      const numero = Number(precio)
      const esEntero = numero % 1 === 0

      // Formatear con punto como separador de miles
      const partes = numero.toFixed(esEntero ? 0 : 2).split('.')
      partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')

      return partes.join(',')
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
    }
  }
}
</script>

<style scoped>
/* Animaciones suaves para las filas */
.v-data-table >>> tbody tr {
  transition: background-color 0.2s;
}

.v-data-table >>> tbody tr:hover {
  background-color: rgba(25, 118, 210, 0.05);
}
</style>
