<template>
  <v-container class="mt-4">
    <h2>Movimientos de Inventario</h2>

    <v-card elevation="3" class="mb-4">
      <v-card-title class="bg-primary">
        <span class="text-white">Filtros</span>
      </v-card-title>
      <v-card-text>
        <v-row align="end">
          <v-col cols="12" md="3">
            <v-select
              v-model="filtro.tipo"
              @change="aplicarFiltros"
              :items="[
                { title: 'Todos', value: '' },
                { title: 'Entrada', value: 'ENTRADA' },
                { title: 'Salida', value: 'SALIDA' },
                { title: 'Ajuste', value: 'AJUSTE' },
                { title: 'Devolución', value: 'DEVOLUCION' }
              ]"
              label="Tipo de Movimiento"
              variant="outlined"
              density="comfortable"
            ></v-select>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="filtro.fecha_desde"
              type="date"
              label="Fecha Desde"
              variant="outlined"
              density="comfortable"
              @change="aplicarFiltros"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-text-field
              v-model="filtro.fecha_hasta"
              type="date"
              label="Fecha Hasta"
              variant="outlined"
              density="comfortable"
              @change="aplicarFiltros"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="3">
            <v-btn @click="limpiarFiltros" color="secondary" block>
              <v-icon left>mdi-refresh</v-icon> Limpiar Filtros
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <div v-if="loading" class="text-center mt-4">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else class="mt-4">
      <v-table density="compact" hover>
        <thead>
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
              <v-chip
                :color="getBadgeClass(mov.tipo_movimiento)"
                size="small"
                variant="flat"
              >
                {{ mov.tipo_movimiento }}
              </v-chip>
            </td>
            <td><span class="nombre-producto">{{ mov.producto_info }}</span></td>
            <td :class="getCantidadClass(mov.tipo_movimiento)">
              {{ getTipoMovimiento(mov.tipo_movimiento) }}{{ mov.cantidad }}
            </td>
            <td>{{ mov.stock_anterior }}</td>
            <td>{{ mov.stock_nuevo }}</td>
            <td>{{ mov.motivo }}</td>
            <td>{{ mov.usuario_nombre }}</td>
          </tr>
        </tbody>
      </v-table>

      <v-alert v-if="movimientosFiltrados.length === 0" type="info" variant="tonal" class="mt-3">
        No hay movimientos de inventario.
      </v-alert>
    </div>
  </v-container>
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
        'ENTRADA': 'success',
        'SALIDA': 'error',
        'AJUSTE': 'warning',
        'DEVOLUCION': 'info'
      }
      return classes[tipo] || 'secondary'
    },
    getCantidadClass(tipo) {
      return tipo === 'ENTRADA' || tipo === 'DEVOLUCION' ? 'text-success font-weight-bold' : 'text-error font-weight-bold'
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
