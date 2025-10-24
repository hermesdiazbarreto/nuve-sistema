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
              :items="['Todos', 'PAGADO', 'ABONO', 'PENDIENTE', 'CANCELADO']"
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
      <v-col cols="12" sm="6" md="4">
        <v-card color="success" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Total Ventas (Ingresos)</div>
                <div class="text-h4 font-weight-bold">{{ formatearPrecio(totalIngresos) }}</div>
              </div>
              <v-icon size="48">mdi-cash-plus</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card color="error" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Total Egresos</div>
                <div class="text-h4 font-weight-bold">{{ formatearPrecio(totalEgresos) }}</div>
              </div>
              <v-icon size="48">mdi-cash-minus</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card color="info" dark elevation="3">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <div class="text-subtitle-2">Cantidad de Ventas</div>
                <div class="text-h4 font-weight-bold">{{ cantidadVentas }}</div>
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

      <!-- Vista Desktop: Tabla completa -->
      <v-data-table
        v-if="$vuetify.display.mdAndUp"
        :headers="headers"
        :items="ventasParaMostrar"
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
          <span>{{ formatearPrecio(item.subtotal) }}</span>
        </template>

        <!-- Descuento -->
        <template #item.descuento="{ item }">
          <span>{{ formatearPrecio(item.descuento) }}</span>
        </template>

        <!-- Total -->
        <template #item.total="{ item }">
          <span class="font-weight-bold">{{ formatearPrecio(item.total) }}</span>
        </template>

        <!-- Monto Abonado -->
        <template #item.monto_abonado="{ item }">
          <span class="font-weight-medium text-success">{{ formatearPrecio(item.monto_abonado || 0) }}</span>
        </template>

        <!-- Saldo Pendiente -->
        <template #item.saldo_pendiente="{ item }">
          <span
            :class="item.saldo_pendiente > 0 ? 'font-weight-medium text-warning' : 'text-grey'"
          >
            {{ formatearPrecio(item.saldo_pendiente || 0) }}
          </span>
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
            v-if="item.estado === 'ABONO' || (item.estado === 'PENDIENTE' && item.saldo_pendiente > 0)"
            icon
            size="small"
            color="success"
            variant="text"
            @click="abrirModalPago(item)"
            title="Registrar pago"
          >
            <v-icon>mdi-cash-plus</v-icon>
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

      <!-- Vista Móvil/Tablet: Cards -->
      <v-card-text v-else class="pa-2">
        <v-card
          v-for="venta in ventasParaMostrar"
          :key="venta.id"
          class="mb-3"
          elevation="2"
        >
          <v-card-text class="pa-3">
            <!-- Header con número y tipo -->
            <div class="d-flex justify-space-between align-center mb-2">
              <div>
                <div class="text-subtitle-2 font-weight-bold">{{ venta.numero_venta }}</div>
                <div class="text-caption text-medium-emphasis">{{ formatFecha(venta.fecha_venta) }}</div>
              </div>
              <v-chip
                :color="venta.tipo_movimiento === 'INGRESO' ? 'success' : 'error'"
                size="small"
                variant="flat"
              >
                <v-icon left size="x-small">
                  {{ venta.tipo_movimiento === 'INGRESO' ? 'mdi-cash-plus' : 'mdi-cash-minus' }}
                </v-icon>
                {{ venta.tipo_movimiento === 'INGRESO' ? 'Ingreso' : 'Egreso' }}
              </v-chip>
            </div>

            <v-divider class="my-2"></v-divider>

            <!-- Información principal -->
            <div class="mb-2">
              <div class="d-flex justify-space-between mb-1">
                <span class="text-caption">Cliente:</span>
                <span class="text-caption font-weight-medium">{{ venta.cliente_nombre }}</span>
              </div>
              <div class="d-flex justify-space-between mb-1">
                <span class="text-caption">Total:</span>
                <span class="text-body-2 font-weight-bold text-primary">{{ formatearPrecio(venta.total) }}</span>
              </div>
              <div v-if="venta.monto_abonado > 0" class="d-flex justify-space-between mb-1">
                <span class="text-caption">Abonado:</span>
                <span class="text-caption font-weight-medium text-success">{{ formatearPrecio(venta.monto_abonado) }}</span>
              </div>
              <div v-if="venta.saldo_pendiente > 0" class="d-flex justify-space-between mb-1">
                <span class="text-caption">Pendiente:</span>
                <span class="text-caption font-weight-bold text-warning">{{ formatearPrecio(venta.saldo_pendiente) }}</span>
              </div>
            </div>

            <!-- Estado y acciones -->
            <div class="d-flex justify-space-between align-center">
              <v-chip :color="getChipColor(venta.estado)" size="small" variant="flat">
                {{ venta.estado }}
              </v-chip>
              <div class="d-flex ga-1">
                <v-btn
                  icon
                  size="small"
                  color="info"
                  variant="text"
                  :to="`/ventas/${venta.id}`"
                  title="Ver detalles"
                >
                  <v-icon size="small">mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  v-if="venta.estado === 'ABONO' || (venta.estado === 'PENDIENTE' && venta.saldo_pendiente > 0)"
                  icon
                  size="small"
                  color="success"
                  variant="text"
                  @click="abrirModalPago(venta)"
                  title="Registrar pago"
                >
                  <v-icon size="small">mdi-cash-plus</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  color="warning"
                  variant="text"
                  :disabled="venta.estado === 'CANCELADO'"
                  @click="cancelarVenta(venta)"
                  title="Cancelar"
                >
                  <v-icon size="small">mdi-cancel</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  color="error"
                  variant="text"
                  @click="eliminarVenta(venta.id)"
                  title="Eliminar"
                >
                  <v-icon size="small">mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <!-- Paginación manual para móvil (opcional) -->
        <div v-if="ventasParaMostrar.length === 0" class="text-center pa-4 text-medium-emphasis">
          No hay ventas registradas
        </div>
      </v-card-text>
    </v-card>

    <!-- Modal para Registrar Pago -->
    <v-dialog v-model="mostrarModalPago" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 success white--text">
          <v-icon left color="white">mdi-cash-plus</v-icon>
          Registrar Pago
        </v-card-title>
        <v-card-text class="pa-6">
          <v-alert v-if="ventaParaPago" type="info" variant="tonal" class="mb-4">
            <div><strong>N° Venta:</strong> {{ ventaParaPago.numero_venta }}</div>
            <div><strong>Cliente:</strong> {{ ventaParaPago.cliente_nombre }}</div>
            <div><strong>Total:</strong> {{ formatearPrecio(ventaParaPago.total) }}</div>
            <div class="mt-2">
              <strong>Monto Abonado:</strong>
              <span class="text-success ml-2">{{ formatearPrecio(ventaParaPago.monto_abonado || 0) }}</span>
            </div>
            <div class="mt-1">
              <strong>Saldo Pendiente:</strong>
              <span class="text-warning ml-2 font-weight-bold">
                {{ formatearPrecio(ventaParaPago.saldo_pendiente || 0) }}
              </span>
            </div>
          </v-alert>

          <v-form ref="formPago">
            <v-text-field
              v-model.number="nuevoPago.monto"
              type="number"
              step="0.01"
              label="Monto a Pagar *"
              variant="outlined"
              prefix="S/"
              :max="ventaParaPago ? ventaParaPago.saldo_pendiente : 0"
              :rules="[
                v => !!v || 'El monto es requerido',
                v => v > 0 || 'El monto debe ser mayor a 0',
                v => v <= (ventaParaPago ? ventaParaPago.saldo_pendiente : 0) || 'El monto no puede exceder el saldo pendiente'
              ]"
              class="mb-3"
            ></v-text-field>

            <v-select
              v-model="nuevoPago.tipo_pago"
              :items="['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'MIXTO']"
              label="Tipo de Pago *"
              variant="outlined"
              :rules="[v => !!v || 'Seleccione un tipo de pago']"
              class="mb-3"
            ></v-select>

            <v-textarea
              v-model="nuevoPago.observaciones"
              label="Observaciones (opcional)"
              variant="outlined"
              rows="3"
              placeholder="Ingrese cualquier nota sobre este pago..."
            ></v-textarea>

            <v-alert
              v-if="nuevoPago.monto > 0 && ventaParaPago"
              type="success"
              variant="tonal"
              class="mt-3"
            >
              <div class="d-flex justify-space-between">
                <span><strong>Nuevo Saldo Pendiente:</strong></span>
                <span class="font-weight-bold">
                  {{ formatearPrecio((ventaParaPago.saldo_pendiente || 0) - nuevoPago.monto) }}
                </span>
              </div>
              <div v-if="(ventaParaPago.saldo_pendiente - nuevoPago.monto) <= 0" class="mt-2">
                <v-icon color="success" size="small">mdi-check-circle</v-icon>
                <span class="ml-1">¡La venta quedará totalmente pagada!</span>
              </div>
            </v-alert>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarModalPago">
            Cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="success" @click="confirmarRegistrarPago">
            <v-icon left>mdi-check</v-icon>
            Registrar Pago
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
            <div><strong>Total:</strong> {{ formatearPrecio(ventaSeleccionada.total) }}</div>
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
import formatoPrecio from '../mixins/formatoPrecio'

export default {
  name: 'VentasLista',
  mixins: [formatoPrecio],
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
      mostrarModalPago: false,
      mostrarModalExito: false,
      mostrarModalError: false,
      ventaSeleccionada: null,
      ventaIdEliminar: null,
      ventaParaPago: null,
      mensajeExito: '',
      mensajeError: '',
      nuevoPago: {
        monto: 0,
        tipo_pago: '',
        observaciones: ''
      },
      headers: [
        { title: 'N° Venta', key: 'numero_venta', sortable: true },
        { title: 'Tipo', key: 'tipo_movimiento', sortable: true },
        { title: 'Cliente', key: 'cliente_nombre', sortable: true },
        { title: 'Vendedor', key: 'vendedor_nombre', sortable: true },
        { title: 'Fecha', key: 'fecha_venta', sortable: true },
        { title: 'Subtotal', key: 'subtotal', sortable: true },
        { title: 'Descuento', key: 'descuento', sortable: true },
        { title: 'Total', key: 'total', sortable: true },
        { title: 'Abonado', key: 'monto_abonado', sortable: true },
        { title: 'Pendiente', key: 'saldo_pendiente', sortable: true },
        { title: 'Tipo Pago', key: 'tipo_pago', sortable: true },
        { title: 'Estado', key: 'estado', sortable: true },
        { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
      ],
    }
  },
  computed: {
    // Solo mostrar ventas de tipo INGRESO en la tabla
    ventasParaMostrar() {
      return this.ventasFiltradas.filter(v => v.tipo_movimiento === 'INGRESO')
    },
    totalIngresos() {
      return this.ventasFiltradas
        .filter(v => v.tipo_movimiento === 'INGRESO')
        .reduce((sum, v) => sum + Number(v.total), 0)
    },
    totalEgresos() {
      return this.ventasFiltradas
        .filter(v => v.tipo_movimiento === 'EGRESO')
        .reduce((sum, v) => sum + Number(v.total), 0)
    },
    cantidadVentas() {
      return this.ventasParaMostrar.length
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
        'ABONO': 'info',
        'PENDIENTE': 'warning',
        'CANCELADO': 'error'
      }
      return colors[estado] || 'grey'
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
    abrirModalPago(venta) {
      this.ventaParaPago = venta
      this.nuevoPago = {
        monto: venta.saldo_pendiente || 0,
        tipo_pago: '',
        observaciones: ''
      }
      this.mostrarModalPago = true
    },
    cerrarModalPago() {
      this.mostrarModalPago = false
      this.ventaParaPago = null
      this.nuevoPago = {
        monto: 0,
        tipo_pago: '',
        observaciones: ''
      }
      if (this.$refs.formPago) {
        this.$refs.formPago.reset()
      }
    },
    async confirmarRegistrarPago() {
      // Validate form
      const { valid } = await this.$refs.formPago.validate()
      if (!valid) {
        return
      }

      try {
        const response = await api.registrarPagoVenta(this.ventaParaPago.id, {
          monto: this.nuevoPago.monto,
          tipo_pago: this.nuevoPago.tipo_pago,
          observaciones: this.nuevoPago.observaciones
        })

        this.cerrarModalPago()

        // Check if sale is now fully paid
        const ventaActualizada = response.data.venta
        if (ventaActualizada.estado === 'PAGADO') {
          this.mensajeExito = `Pago registrado correctamente. ¡La venta está totalmente pagada!`
        } else {
          this.mensajeExito = `Pago registrado correctamente. Saldo pendiente: ${this.formatearPrecio(ventaActualizada.saldo_pendiente)}`
        }

        this.mostrarModalExito = true
        await this.cargarVentas()
      } catch (error) {
        console.error('Error al registrar pago:', error)
        this.cerrarModalPago()
        this.mensajeError = error.response?.data?.error || error.response?.data?.detail || error.message || 'Error al registrar el pago'
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
