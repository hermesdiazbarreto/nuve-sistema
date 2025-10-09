<template>
  <div>
    <!-- Header -->
    <v-row align="center" class="mb-6">
      <v-col cols="12" md="6">
        <h1 class="text-h4 font-weight-bold">
          <v-icon large color="primary" class="mr-2">mdi-package-variant</v-icon>
          Productos
        </h1>
      </v-col>
      <v-col cols="12" md="6" class="text-md-right">
        <v-btn
          color="error"
          variant="outlined"
          class="mr-2"
          :to="'/productos/eliminados'"
        >
          <v-icon left>mdi-delete</v-icon>
          Ver Eliminados
        </v-btn>
        <v-btn
          color="primary"
          :to="'/productos/nuevo'"
        >
          <v-icon left>mdi-plus</v-icon>
          Nuevo Producto
        </v-btn>
      </v-col>
    </v-row>

    <!-- Data Table Card -->
    <v-card elevation="3">
      <v-card-title class="d-flex align-center pa-4">
        <v-icon class="mr-2">mdi-table</v-icon>
        Listado de Productos

        <v-spacer></v-spacer>

        <v-text-field
          v-model="search"
          append-inner-icon="mdi-magnify"
          label="Buscar producto..."
          single-line
          hide-details
          variant="outlined"
          density="compact"
          style="max-width: 300px"
        ></v-text-field>
      </v-card-title>

      <v-divider></v-divider>

      <v-data-table
        :headers="headers"
        :items="productos"
        :search="search"
        :loading="loading"
        loading-text="Cargando productos..."
        no-data-text="No hay productos registrados"
        items-per-page-text="Productos por página"
        class="elevation-0"
      >
        <!-- Código -->
        <template #item.codigo="{ item }">
          <span class="font-weight-bold">{{ item.codigo }}</span>
        </template>

        <!-- Categoría -->
        <template #item.categoria_nombre="{ item }">
          <v-chip color="primary" size="small" variant="flat">
            {{ item.categoria_nombre }}
          </v-chip>
        </template>

        <!-- Precio -->
        <template #item.precio_venta="{ item }">
          <span class="font-weight-medium">S/ {{ formatPrecio(item.precio_venta) }}</span>
        </template>

        <!-- Variantes -->
        <template #item.total_variantes="{ item }">
          <v-btn
            size="small"
            color="info"
            variant="outlined"
            @click="verVariantes(item)"
          >
            <v-icon left size="small">mdi-magnify</v-icon>
            {{ item.total_variantes || 0 }}
          </v-btn>
        </template>

        <!-- Stock -->
        <template #item.stock_total="{ item }">
          <v-chip
            :color="getStockColor(item.stock_total)"
            size="small"
            variant="flat"
          >
            {{ item.stock_total || 0 }}
          </v-chip>
        </template>

        <!-- Estado -->
        <template #item.activo="{ item }">
          <v-chip
            :color="item.activo ? 'success' : 'grey'"
            size="small"
            variant="flat"
          >
            <v-icon left size="small">
              {{ item.activo ? 'mdi-check-circle' : 'mdi-close-circle' }}
            </v-icon>
            {{ item.activo ? 'Activo' : 'Inactivo' }}
          </v-chip>
        </template>

        <!-- Acciones -->
        <template #item.actions="{ item }">
          <v-btn
            icon
            size="small"
            color="warning"
            variant="text"
            :to="`/productos/editar/${item.id}`"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            color="error"
            variant="text"
            @click="eliminarProducto(item.id)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Modal de Variantes -->
    <v-dialog v-model="mostrarVariantes" max-width="900px">
      <v-card>
        <v-card-title class="text-h5 primary white--text">
          <v-icon left color="white">mdi-format-list-bulleted</v-icon>
          Variantes de: {{ productoSeleccionado?.nombre }}
        </v-card-title>

        <v-card-text class="pa-4">
          <v-btn
            color="primary"
            size="small"
            class="mb-4"
            :to="`/productos/editar/${productoSeleccionado?.id}`"
            @click="cerrarVariantes"
          >
            <v-icon left>mdi-plus</v-icon>
            Agregar Variante
          </v-btn>

          <v-progress-linear
            v-if="cargandoVariantes"
            indeterminate
            color="primary"
          ></v-progress-linear>

          <v-alert
            v-else-if="variantesProducto.length === 0"
            type="info"
            variant="tonal"
          >
            Este producto no tiene variantes.
          </v-alert>

          <v-table v-else density="comfortable">
            <thead>
              <tr>
                <th>Código</th>
                <th>Talla</th>
                <th>Color</th>
                <th>Stock</th>
                <th>Mín</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="variante in variantesProducto" :key="variante.id">
                <td>{{ variante.codigo_variante }}</td>
                <td>{{ variante.talla_nombre }}</td>
                <td>{{ variante.color_nombre }}</td>
                <td>
                  <v-chip
                    :color="variante.stock_actual <= variante.stock_minimo ? 'error' : 'success'"
                    size="small"
                  >
                    {{ variante.stock_actual }}
                  </v-chip>
                </td>
                <td>{{ variante.stock_minimo }}</td>
                <td>
                  <v-chip
                    :color="variante.activo ? 'success' : 'grey'"
                    size="small"
                  >
                    {{ variante.activo ? 'Activo' : 'Inactivo' }}
                  </v-chip>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="cerrarVariantes">
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para notificaciones -->
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="3000"
      top
    >
      {{ snackbarText }}
      <template #actions>
        <v-btn
          variant="text"
          @click="snackbar = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProductosLista',
  data() {
    return {
      productos: [],
      loading: true,
      search: '',
      mostrarVariantes: false,
      productoSeleccionado: null,
      variantesProducto: [],
      cargandoVariantes: false,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      headers: [
        { title: 'Código', key: 'codigo', sortable: true },
        { title: 'Nombre', key: 'nombre', sortable: true },
        { title: 'Categoría', key: 'categoria_nombre', sortable: true },
        { title: 'Marca', key: 'marca_nombre', sortable: true },
        { title: 'Precio Venta', key: 'precio_venta', sortable: true },
        { title: 'Variantes', key: 'total_variantes', sortable: false },
        { title: 'Stock Total', key: 'stock_total', sortable: true },
        { title: 'Estado', key: 'activo', sortable: true },
        { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
      ],
    }
  },
  async created() {
    await this.cargarProductos()
  },
  methods: {
    async cargarProductos() {
      try {
        this.loading = true
        const [productosRes, variantesRes] = await Promise.all([
          api.getProductos(),
          api.getProductoVariantes()
        ])

        const productos = productosRes.data.results || productosRes.data || []
        const variantes = variantesRes.data.results || variantesRes.data || []

        this.productos = productos.map(producto => {
          const variantesProducto = variantes.filter(v => v.producto === producto.id)
          const stockTotal = variantesProducto.reduce((sum, v) => sum + (v.stock_actual || 0), 0)
          return {
            ...producto,
            total_variantes: variantesProducto.length,
            stock_total: stockTotal
          }
        })
      } catch (error) {
        console.error('Error al cargar productos:', error)
        this.showSnackbar('Error al cargar los productos', 'error')
      } finally {
        this.loading = false
      }
    },
    async verVariantes(producto) {
      this.productoSeleccionado = producto
      this.mostrarVariantes = true
      this.cargandoVariantes = true

      try {
        const response = await api.getProductoVariantes()
        const variantes = response.data.results || response.data || []
        this.variantesProducto = variantes.filter(v => v.producto === producto.id)
      } catch (error) {
        console.error('Error al cargar variantes:', error)
        this.showSnackbar('Error al cargar las variantes', 'error')
      } finally {
        this.cargandoVariantes = false
      }
    },
    cerrarVariantes() {
      this.mostrarVariantes = false
      this.productoSeleccionado = null
      this.variantesProducto = []
    },
    async eliminarProducto(id) {
      if (confirm('¿Estás seguro de eliminar este producto?\n\nNOTA: El producto no se borrará permanentemente, solo se marcará como eliminado.\nPodrás restaurarlo desde "Ver Eliminados".')) {
        try {
          const response = await api.deleteProducto(id)
          await this.cargarProductos()
          this.showSnackbar(response.data.message || 'Producto eliminado correctamente', 'success')
        } catch (error) {
          console.error('Error al eliminar producto:', error)
          this.showSnackbar(error.response?.data?.error || 'Error al eliminar el producto', 'error')
        }
      }
    },
    getStockColor(stock) {
      if (stock === 0) return 'error'
      if (stock < 10) return 'warning'
      return 'success'
    },
    formatPrecio(precio) {
      const numero = Number(precio)
      const esEntero = numero % 1 === 0

      // Formatear con punto como separador de miles
      const partes = numero.toFixed(esEntero ? 0 : 2).split('.')
      partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')

      return partes.join(',')
    },
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
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
