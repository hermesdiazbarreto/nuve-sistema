<template>
  <div>
    <!-- Header -->
    <v-row align="center" class="mb-6">
      <v-col cols="12" md="6">
        <h1 class="text-h4 font-weight-bold">
          <v-icon large color="error" class="mr-2">mdi-delete-variant</v-icon>
          Productos Eliminados
        </h1>
      </v-col>
      <v-col cols="12" md="6" class="text-md-right">
        <v-btn
          color="primary"
          variant="outlined"
          :to="'/productos'"
        >
          <v-icon left>mdi-arrow-left</v-icon>
          Volver a Productos
        </v-btn>
      </v-col>
    </v-row>

    <!-- Info Alert -->
    <v-alert
      v-if="productos.length > 0"
      type="warning"
      variant="tonal"
      class="mb-4"
    >
      <v-alert-title class="font-weight-bold">
        <v-icon left>mdi-information</v-icon>
        Información
      </v-alert-title>
      Estos productos han sido eliminados pero aún se conservan en la base de datos.
      Puedes restaurarlos cuando quieras.
    </v-alert>

    <!-- Empty State -->
    <v-card v-if="!loading && productos.length === 0" elevation="3" class="text-center pa-8">
      <v-icon size="80" color="success" class="mb-4">mdi-check-circle</v-icon>
      <h2 class="text-h5 mb-2">¡No hay productos eliminados!</h2>
      <p class="text-body-1 text-medium-emphasis">
        Todos los productos están activos.
      </p>
      <v-btn color="primary" :to="'/productos'" class="mt-4">
        Ver Productos Activos
      </v-btn>
    </v-card>

    <!-- Data Table Card -->
    <v-card v-else elevation="3">
      <v-card-title class="d-flex align-center pa-4">
        <v-icon class="mr-2">mdi-delete-restore</v-icon>
        Productos Eliminados ({{ productos.length }})

        <v-spacer></v-spacer>

        <v-text-field
          v-model="search"
          append-inner-icon="mdi-magnify"
          label="Buscar..."
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
        loading-text="Cargando productos eliminados..."
        no-data-text="No hay productos eliminados"
        items-per-page-text="Productos por página"
        class="elevation-0"
      >
        <!-- Código -->
        <template #item.codigo="{ item }">
          <span class="font-weight-bold">{{ item.codigo }}</span>
        </template>

        <!-- Categoría -->
        <template #item.categoria_nombre="{ item }">
          <v-chip color="grey" size="small" variant="flat">
            {{ item.categoria_nombre }}
          </v-chip>
        </template>

        <!-- Precio -->
        <template #item.precio_venta="{ item }">
          <span class="font-weight-medium">S/ {{ formatPrecio(item.precio_venta) }}</span>
        </template>

        <!-- Fecha Eliminación -->
        <template #item.deleted_at="{ item }">
          <span>{{ formatFecha(item.deleted_at) }}</span>
        </template>

        <!-- Usuario -->
        <template #item.deleted_by_username="{ item }">
          <v-chip color="error" size="small" variant="flat">
            <v-icon left size="small">mdi-account</v-icon>
            {{ item.deleted_by_username || 'Desconocido' }}
          </v-chip>
        </template>

        <!-- Acciones -->
        <template #item.actions="{ item }">
          <v-btn
            size="small"
            color="success"
            variant="tonal"
            class="mr-2"
            @click="restaurarProducto(item.id)"
          >
            <v-icon left size="small">mdi-restore</v-icon>
            Restaurar
          </v-btn>
          <v-btn
            icon
            size="small"
            color="info"
            variant="text"
            @click="verDetalles(item)"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Modal de Detalles -->
    <v-dialog v-model="mostrarDetalles" max-width="700px">
      <v-card v-if="productoSeleccionado">
        <v-card-title class="text-h5 error white--text">
          <v-icon left color="white">mdi-file-document-outline</v-icon>
          Detalles del Producto Eliminado
        </v-card-title>

        <v-card-text class="pa-6">
          <v-row>
            <v-col cols="12" md="6">
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Código</span>
                <p class="text-h6 font-weight-medium">{{ productoSeleccionado.codigo }}</p>
              </div>
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Nombre</span>
                <p class="text-h6 font-weight-medium">{{ productoSeleccionado.nombre }}</p>
              </div>
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Categoría</span>
                <p class="text-body-1">{{ productoSeleccionado.categoria_nombre }}</p>
              </div>
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Marca</span>
                <p class="text-body-1">{{ productoSeleccionado.marca_nombre }}</p>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Precio Compra</span>
                <p class="text-h6 success--text">S/ {{ formatPrecio(productoSeleccionado.precio_compra) }}</p>
              </div>
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Precio Venta</span>
                <p class="text-h6 primary--text">S/ {{ formatPrecio(productoSeleccionado.precio_venta) }}</p>
              </div>
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Fecha de Eliminación</span>
                <p class="text-body-1">{{ formatFecha(productoSeleccionado.deleted_at) }}</p>
              </div>
              <div class="mb-4">
                <span class="text-caption text-medium-emphasis">Eliminado Por</span>
                <p class="text-body-1">{{ productoSeleccionado.deleted_by_username || 'Desconocido' }}</p>
              </div>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div v-if="productoSeleccionado.descripcion">
            <span class="text-caption text-medium-emphasis">Descripción</span>
            <p class="text-body-1 mt-2">{{ productoSeleccionado.descripcion }}</p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions class="pa-4">
          <v-btn
            color="success"
            @click="restaurarProducto(productoSeleccionado.id)"
          >
            <v-icon left>mdi-restore</v-icon>
            Restaurar Producto
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="cerrarDetalles">
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="3000"
      top
    >
      {{ snackbarText }}
      <template #actions>
        <v-btn variant="text" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProductosEliminados',
  data() {
    return {
      productos: [],
      loading: true,
      search: '',
      mostrarDetalles: false,
      productoSeleccionado: null,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      headers: [
        { title: 'Código', key: 'codigo', sortable: true },
        { title: 'Nombre', key: 'nombre', sortable: true },
        { title: 'Categoría', key: 'categoria_nombre', sortable: true },
        { title: 'Marca', key: 'marca_nombre', sortable: true },
        { title: 'Precio Venta', key: 'precio_venta', sortable: true },
        { title: 'Fecha Eliminación', key: 'deleted_at', sortable: true },
        { title: 'Eliminado Por', key: 'deleted_by_username', sortable: true },
        { title: 'Acciones', key: 'actions', sortable: false, align: 'center' },
      ],
    }
  },
  async created() {
    await this.cargarProductosEliminados()
  },
  methods: {
    async cargarProductosEliminados() {
      try {
        this.loading = true
        const response = await api.getProductosEliminados()
        this.productos = response.data.results || response.data || []
      } catch (error) {
        console.error('Error al cargar productos eliminados:', error)
        this.showSnackbar('Error al cargar los productos eliminados', 'error')
      } finally {
        this.loading = false
      }
    },
    async restaurarProducto(id) {
      if (confirm('¿Estás seguro de restaurar este producto?\n\nEl producto volverá a estar activo y visible en el listado principal.')) {
        try {
          const response = await api.restaurarProducto(id)
          await this.cargarProductosEliminados()
          this.showSnackbar(response.data.message || 'Producto restaurado correctamente', 'success')

          if (this.mostrarDetalles) {
            this.cerrarDetalles()
          }
        } catch (error) {
          console.error('Error al restaurar producto:', error)
          this.showSnackbar(error.response?.data?.error || 'Error al restaurar el producto', 'error')
        }
      }
    },
    verDetalles(producto) {
      this.productoSeleccionado = producto
      this.mostrarDetalles = true
    },
    cerrarDetalles() {
      this.mostrarDetalles = false
      this.productoSeleccionado = null
    },
    formatFecha(fecha) {
      if (!fecha) return 'N/A'
      const date = new Date(fecha)
      return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    formatPrecio(precio) {
      const numero = Number(precio)
      return numero.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
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
/* Filas de productos eliminados con fondo rojo claro */
.v-data-table >>> tbody tr {
  background-color: rgba(255, 82, 82, 0.05);
  transition: background-color 0.2s;
}

.v-data-table >>> tbody tr:hover {
  background-color: rgba(255, 82, 82, 0.1);
}
</style>
