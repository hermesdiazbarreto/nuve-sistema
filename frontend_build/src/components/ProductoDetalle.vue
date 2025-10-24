<template>
  <div>
    <!-- Header -->
    <v-row align="center" class="mb-4">
      <v-col cols="12">
        <v-btn icon @click="$router.back()" class="mr-3">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <span class="text-h4 font-weight-bold">
          {{ producto.nombre }}
        </span>
      </v-col>
    </v-row>

    <!-- Loading -->
    <v-progress-linear v-if="loading" indeterminate color="primary"></v-progress-linear>

    <!-- Pestañas -->
    <v-card v-if="!loading" elevation="3">
      <v-tabs v-model="tab" bg-color="primary">
        <v-tab value="info">
          <v-icon left>mdi-information</v-icon>
          Información
        </v-tab>
        <v-tab value="variantes">
          <v-icon left>mdi-shape</v-icon>
          Variantes ({{ variantes.length }})
        </v-tab>
        <v-tab value="historial">
          <v-icon left>mdi-history</v-icon>
          Historial de Ventas
        </v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <!-- Pestaña: Información General -->
        <v-window-item value="info">
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Código</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ producto.codigo }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Categoría</v-list-item-title>
                    <v-list-item-subtitle>{{ producto.categoria_nombre }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Marca</v-list-item-title>
                    <v-list-item-subtitle>{{ producto.marca_nombre }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
              <v-col cols="12" md="6">
                <v-list>
                  <v-list-item>
                    <v-list-item-title>Precio Compra</v-list-item-title>
                    <v-list-item-subtitle class="text-h6">{{ formatearPrecio(producto.precio_compra) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Precio Venta</v-list-item-title>
                    <v-list-item-subtitle class="text-h6 text-success">{{ formatearPrecio(producto.precio_venta) }}</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Estado</v-list-item-title>
                    <v-list-item-subtitle>
                      <v-chip :color="producto.activo ? 'success' : 'error'" size="small">
                        {{ producto.activo ? 'Activo' : 'Inactivo' }}
                      </v-chip>
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-window-item>

        <!-- Pestaña: Variantes -->
        <v-window-item value="variantes">
          <v-card-text>
            <v-data-table
              :headers="headersVariantes"
              :items="variantes"
              :items-per-page="10"
              items-per-page-text="Variantes por página"
              no-data-text="No hay variantes para este producto"
            >
              <template #item.talla_nombre="{ item }">
                <v-chip size="small">{{ item.talla_nombre }}</v-chip>
              </template>
              <template #item.color_nombre="{ item }">
                <v-chip size="small" :style="{ backgroundColor: item.color_hex, color: 'white' }">
                  {{ item.color_nombre }}
                </v-chip>
              </template>
              <template #item.stock_actual="{ item }">
                <v-chip :color="item.stock_actual <= item.stock_minimo ? 'error' : 'success'" size="small">
                  {{ item.stock_actual }}
                </v-chip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-window-item>

        <!-- Pestaña: Historial de Ventas -->
        <v-window-item value="historial">
          <v-card-text>
            <v-progress-linear v-if="loadingHistorial" indeterminate color="primary"></v-progress-linear>

            <div v-else-if="historialVentas.length === 0" class="text-center pa-8">
              <v-icon size="64" color="grey-lighten-1">mdi-cart-off</v-icon>
              <p class="text-h6 mt-4 text-grey">No hay ventas registradas para este producto</p>
            </div>

            <div v-else>
              <!-- Resumen -->
              <v-row class="mb-4">
                <v-col cols="12" sm="6" md="3">
                  <v-card color="info" dark>
                    <v-card-text class="text-center">
                      <div class="text-subtitle-2">Total Vendido</div>
                      <div class="text-h5 font-weight-bold">{{ totalUnidadesVendidas }} unidades</div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="3">
                  <v-card color="success" dark>
                    <v-card-text class="text-center">
                      <div class="text-subtitle-2">Ingresos Totales</div>
                      <div class="text-h5 font-weight-bold">{{ formatearPrecio(totalIngresos) }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>

              <!-- Tabla de historial -->
              <v-data-table
                :headers="headersHistorial"
                :items="historialVentas"
                :items-per-page="10"
                items-per-page-text="Ventas por página"
                class="elevation-1"
              >
                <template #item.fecha_venta="{ item }">
                  <span class="text-caption">{{ formatFecha(item.fecha_venta) }}</span>
                </template>
                <template #item.numero_venta="{ item }">
                  <v-btn
                    variant="text"
                    color="primary"
                    size="small"
                    :to="`/ventas/${item.venta_id}`"
                  >
                    {{ item.numero_venta }}
                  </v-btn>
                </template>
                <template #item.variante="{ item }">
                  <v-chip size="x-small" class="mr-1">{{ item.talla }}</v-chip>
                  <v-chip size="x-small" :style="{ backgroundColor: item.color_hex, color: 'white' }">
                    {{ item.color }}
                  </v-chip>
                </template>
                <template #item.precio_unitario="{ item }">
                  {{ formatearPrecio(item.precio_unitario) }}
                </template>
                <template #item.subtotal="{ item }">
                  <span class="font-weight-bold">{{ formatearPrecio(item.subtotal) }}</span>
                </template>
                <template #item.estado="{ item }">
                  <v-chip :color="getChipColor(item.estado)" size="x-small">
                    {{ item.estado }}
                  </v-chip>
                </template>
              </v-data-table>
            </div>
          </v-card-text>
        </v-window-item>
      </v-window>
    </v-card>
  </div>
</template>

<script>
import api from '../services/api'
import formatoPrecio from '../mixins/formatoPrecio'

export default {
  name: 'ProductoDetalle',
  mixins: [formatoPrecio],
  data() {
    return {
      loading: true,
      loadingHistorial: false,
      tab: 'info',
      producto: {},
      variantes: [],
      historialVentas: [],
      headersVariantes: [
        { title: 'Código', key: 'codigo_variante' },
        { title: 'Talla', key: 'talla_nombre' },
        { title: 'Color', key: 'color_nombre' },
        { title: 'Stock', key: 'stock_actual' },
        { title: 'Stock Mínimo', key: 'stock_minimo' },
      ],
      headersHistorial: [
        { title: 'Fecha', key: 'fecha_venta' },
        { title: 'N° Venta', key: 'numero_venta' },
        { title: 'Variante', key: 'variante' },
        { title: 'Cliente', key: 'cliente' },
        { title: 'Cantidad', key: 'cantidad' },
        { title: 'Precio Unit.', key: 'precio_unitario' },
        { title: 'Subtotal', key: 'subtotal' },
        { title: 'Estado', key: 'estado' },
      ]
    }
  },
  computed: {
    totalUnidadesVendidas() {
      return this.historialVentas.reduce((total, item) => total + item.cantidad, 0)
    },
    totalIngresos() {
      return this.historialVentas.reduce((total, item) => total + item.subtotal, 0)
    }
  },
  watch: {
    tab(newTab) {
      if (newTab === 'historial' && this.historialVentas.length === 0) {
        this.cargarHistorialVentas()
      }
    }
  },
  async created() {
    await this.cargarProducto()
  },
  methods: {
    async cargarProducto() {
      try {
        this.loading = true
        const productoId = this.$route.params.id

        // Cargar producto
        const productoRes = await api.getProducto(productoId)
        this.producto = productoRes.data

        // Cargar variantes del producto
        const variantesRes = await api.getProductoVariantes(productoId)
        this.variantes = variantesRes.data.results || variantesRes.data || []

      } catch (error) {
        console.error('Error al cargar producto:', error)
      } finally {
        this.loading = false
      }
    },
    async cargarHistorialVentas() {
      try {
        this.loadingHistorial = true

        // Obtener todas las ventas
        const ventasRes = await api.getVentas()
        const ventas = ventasRes.data.results || ventasRes.data || []

        // Obtener todos los detalles de ventas
        const detallesRes = await api.getDetalleVentas()
        const detalles = detallesRes.data.results || detallesRes.data || []

        // Filtrar detalles que pertenecen a variantes de este producto
        const variantesIds = this.variantes.map(v => v.id)
        const detallesFiltrados = detalles.filter(d => variantesIds.includes(d.producto_variante))

        // Enriquecer con información de la venta y variante
        this.historialVentas = detallesFiltrados.map(detalle => {
          const venta = ventas.find(v => v.id === detalle.venta)
          const variante = this.variantes.find(v => v.id === detalle.producto_variante)

          return {
            ...detalle,
            venta_id: venta?.id,
            numero_venta: venta?.numero_venta || 'N/A',
            fecha_venta: venta?.fecha_venta,
            cliente: venta?.cliente_nombre || 'Cliente General',
            estado: venta?.estado || 'N/A',
            talla: variante?.talla_nombre || '',
            color: variante?.color_nombre || '',
            color_hex: variante?.color_hex || '#999'
          }
        }).sort((a, b) => new Date(b.fecha_venta) - new Date(a.fecha_venta)) // Más recientes primero

      } catch (error) {
        console.error('Error al cargar historial de ventas:', error)
      } finally {
        this.loadingHistorial = false
      }
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
      const date = new Date(fecha)
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.v-chip {
  font-weight: 500;
}
</style>
