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

        <!-- Nombre -->
        <template #item.nombre="{ item }">
          <span class="nombre-producto">{{ item.nombre }}</span>
        </template>

        <!-- Categoría -->
        <template #item.categoria_nombre="{ item }">
          <v-chip color="primary" size="small" variant="flat">
            {{ item.categoria_nombre }}
          </v-chip>
        </template>

        <!-- Precio -->
        <template #item.precio_venta="{ item }">
          <span class="font-weight-medium">{{ formatearPrecio(item.precio_venta) }}</span>
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
            color="info"
            variant="text"
            :to="`/productos/${item.id}`"
            title="Ver detalle"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            color="warning"
            variant="text"
            :to="`/productos/editar/${item.id}`"
            title="Editar"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            color="error"
            variant="text"
            @click="eliminarProducto(item.id)"
            title="Eliminar"
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
          <span>Variantes de: <span class="nombre-producto">{{ productoSeleccionado?.nombre }}</span></span>
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

          <!-- Vista Desktop: Tabla -->
          <v-table v-else-if="$vuetify.display.mdAndUp" density="comfortable">
            <thead>
              <tr>
                <th>Código</th>
                <th>Talla</th>
                <th>Color</th>
                <th>Stock</th>
                <th>Mín</th>
                <th>Estado</th>
                <th class="text-center">Acciones</th>
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
                <td class="text-center">
                  <v-btn
                    icon
                    size="small"
                    color="info"
                    variant="text"
                    @click="abrirModalDuplicar(variante)"
                    title="Duplicar variante"
                  >
                    <v-icon>mdi-content-copy</v-icon>
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>

          <!-- Vista Móvil: Cards -->
          <div v-else>
            <v-card
              v-for="variante in variantesProducto"
              :key="variante.id"
              class="mb-2"
              elevation="2"
            >
              <v-card-text class="pa-3">
                <div class="d-flex justify-space-between align-center mb-2">
                  <div>
                    <div class="text-body-2 font-weight-bold">{{ variante.codigo_variante }}</div>
                    <div class="text-caption text-medium-emphasis">
                      {{ variante.talla_nombre }} / {{ variante.color_nombre }}
                    </div>
                  </div>
                  <v-chip
                    :color="variante.activo ? 'success' : 'grey'"
                    size="small"
                    variant="flat"
                  >
                    {{ variante.activo ? 'Activo' : 'Inactivo' }}
                  </v-chip>
                </div>

                <v-divider class="my-2"></v-divider>

                <div class="d-flex justify-space-around mb-2">
                  <div class="text-center">
                    <div class="text-caption text-medium-emphasis">Stock</div>
                    <v-chip
                      :color="variante.stock_actual <= variante.stock_minimo ? 'error' : 'success'"
                      size="small"
                      variant="flat"
                    >
                      {{ variante.stock_actual }}
                    </v-chip>
                  </div>
                  <div class="text-center">
                    <div class="text-caption text-medium-emphasis">Mínimo</div>
                    <div class="text-body-2 font-weight-medium">{{ variante.stock_minimo }}</div>
                  </div>
                </div>

                <div class="text-center">
                  <v-btn
                    size="small"
                    color="info"
                    variant="outlined"
                    @click="abrirModalDuplicar(variante)"
                  >
                    <v-icon left size="small">mdi-content-copy</v-icon>
                    Duplicar
                  </v-btn>
                </div>
              </v-card-text>
            </v-card>
          </div>
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

    <!-- Modal para Duplicar Variante -->
    <v-dialog v-model="mostrarModalDuplicar" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 info white--text">
          <v-icon left color="white">mdi-content-copy</v-icon>
          Duplicar Variante
        </v-card-title>
        <v-card-text class="pa-6">
          <v-alert v-if="varianteADuplicar" type="info" variant="tonal" class="mb-4">
            <div><strong>Variante Original:</strong></div>
            <div>Código: {{ varianteADuplicar.codigo_variante }}</div>
            <div>Talla: {{ varianteADuplicar.talla_nombre }} / Color: {{ varianteADuplicar.color_nombre }}</div>
            <div>Stock Actual: {{ varianteADuplicar.stock_actual }}</div>
          </v-alert>

          <v-form ref="formDuplicar">
            <v-select
              v-model="duplicarData.talla"
              :items="tallas"
              item-title="nombre"
              item-value="id"
              label="Talla *"
              variant="outlined"
              :rules="[v => !!v || 'Seleccione una talla']"
              class="mb-3"
            ></v-select>

            <v-select
              v-model="duplicarData.color"
              :items="colores"
              item-title="nombre"
              item-value="id"
              label="Color *"
              variant="outlined"
              :rules="[v => !!v || 'Seleccione un color']"
              class="mb-3"
            ></v-select>

            <v-text-field
              v-model.number="duplicarData.stock_actual"
              type="number"
              label="Stock Inicial *"
              variant="outlined"
              :rules="[v => v >= 0 || 'El stock debe ser mayor o igual a 0']"
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model.number="duplicarData.stock_minimo"
              type="number"
              label="Stock Mínimo *"
              variant="outlined"
              :rules="[v => v >= 0 || 'El stock mínimo debe ser mayor o igual a 0']"
            ></v-text-field>

            <v-alert type="success" variant="tonal" class="mt-4">
              Se creará una nueva variante con las características especificadas, manteniendo los demás datos del producto original.
            </v-alert>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarModalDuplicar">
            Cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="info" @click="confirmarDuplicarVariante">
            <v-icon left>mdi-check</v-icon>
            Duplicar Variante
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
import formatoPrecio from '../mixins/formatoPrecio'

export default {
  name: 'ProductosLista',
  mixins: [formatoPrecio],
  data() {
    return {
      productos: [],
      loading: true,
      search: '',
      mostrarVariantes: false,
      productoSeleccionado: null,
      variantesProducto: [],
      cargandoVariantes: false,
      mostrarModalDuplicar: false,
      varianteADuplicar: null,
      tallas: [],
      colores: [],
      duplicarData: {
        talla: null,
        color: null,
        stock_actual: 0,
        stock_minimo: 0
      },
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
    await this.cargarTallasYColores()
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
        // Filtrar por producto directamente en el API
        const response = await api.getProductoVariantes(producto.id)
        this.variantesProducto = response.data.results || response.data || []
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
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarTallasYColores() {
      try {
        const [tallasRes, coloresRes] = await Promise.all([
          api.getTallas(),
          api.getColores()
        ])
        this.tallas = tallasRes.data.results || tallasRes.data || []
        this.colores = coloresRes.data.results || coloresRes.data || []
      } catch (error) {
        console.error('Error al cargar tallas y colores:', error)
      }
    },
    abrirModalDuplicar(variante) {
      this.varianteADuplicar = variante
      this.duplicarData = {
        talla: variante.talla,
        color: variante.color,
        stock_actual: 0,
        stock_minimo: variante.stock_minimo
      }
      this.mostrarModalDuplicar = true
    },
    cerrarModalDuplicar() {
      this.mostrarModalDuplicar = false
      this.varianteADuplicar = null
      this.duplicarData = {
        talla: null,
        color: null,
        stock_actual: 0,
        stock_minimo: 0
      }
      if (this.$refs.formDuplicar) {
        this.$refs.formDuplicar.reset()
      }
    },
    async confirmarDuplicarVariante() {
      // Validate form
      const { valid } = await this.$refs.formDuplicar.validate()
      if (!valid) {
        return
      }

      try {
        await api.duplicarProductoVariante(this.varianteADuplicar.id, {
          talla: this.duplicarData.talla,
          color: this.duplicarData.color,
          stock_actual: this.duplicarData.stock_actual,
          stock_minimo: this.duplicarData.stock_minimo
        })

        this.showSnackbar('Variante duplicada correctamente', 'success')
        this.cerrarModalDuplicar()

        // Recargar variantes del producto actual
        if (this.productoSeleccionado) {
          await this.verVariantes(this.productoSeleccionado)
        }

        // Recargar productos para actualizar contadores
        await this.cargarProductos()
      } catch (error) {
        console.error('Error al duplicar variante:', error)
        this.showSnackbar(
          error.response?.data?.error || 'Error al duplicar la variante',
          'error'
        )
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
