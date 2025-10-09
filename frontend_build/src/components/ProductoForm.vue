<template>
  <div>
    <!-- Header -->
    <v-row align="center" class="mb-6">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold">
          <v-icon large color="primary" class="mr-2">
            {{ esEdicion ? 'mdi-pencil' : 'mdi-plus-circle' }}
          </v-icon>
          {{ esEdicion ? 'Editar' : 'Nuevo' }} Producto
        </h1>
      </v-col>
    </v-row>

    <!-- Formulario Principal -->
    <v-card elevation="3" class="mb-4">
      <v-card-title class="bg-primary">
        <v-icon left color="white">mdi-form-select</v-icon>
        <span class="text-white">Información del Producto</span>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-6">
        <v-form @submit.prevent="guardarProducto">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.codigo"
                label="Código *"
                variant="outlined"
                density="comfortable"
                required
                :rules="[v => !!v || 'Código es requerido']"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.nombre"
                label="Nombre *"
                variant="outlined"
                density="comfortable"
                required
                :rules="[v => !!v || 'Nombre es requerido']"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-textarea
                v-model="form.descripcion"
                label="Descripción"
                variant="outlined"
                density="comfortable"
                rows="2"
              ></v-textarea>
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="form.categoria"
                :items="categorias"
                item-title="nombre"
                item-value="id"
                label="Categoría *"
                variant="outlined"
                density="comfortable"
                required
                :rules="[v => !!v || 'Categoría es requerida']"
              ></v-select>
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="form.marca"
                :items="marcas"
                item-title="nombre"
                item-value="id"
                label="Marca *"
                variant="outlined"
                density="comfortable"
                required
                :rules="[v => !!v || 'Marca es requerida']"
              ></v-select>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="form.precio_compra"
                label="Precio de Compra *"
                variant="outlined"
                density="comfortable"
                type="number"
                step="0.01"
                prefix="S/"
                required
                :rules="[v => !!v || 'Precio de compra es requerido']"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model.number="form.precio_venta"
                label="Precio de Venta *"
                variant="outlined"
                density="comfortable"
                type="number"
                step="0.01"
                prefix="S/"
                required
                :rules="[v => !!v || 'Precio de venta es requerido']"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-checkbox
                v-model="form.activo"
                label="Producto Activo"
                color="primary"
              ></v-checkbox>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <div class="d-flex gap-2">
            <v-btn type="submit" color="primary" size="large">
              <v-icon left>mdi-content-save</v-icon>
              Guardar Producto
            </v-btn>
            <v-btn :to="'/productos'" color="grey" variant="outlined" size="large">
              <v-icon left>mdi-cancel</v-icon>
              Cancelar
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Sección de Variantes (solo en modo edición) -->
    <v-card v-if="esEdicion" elevation="3">
      <v-card-title class="bg-secondary d-flex justify-space-between align-items-center">
        <span class="text-white">
          <v-icon left color="white">mdi-package-variant</v-icon>
          Variantes y Stock
        </span>
        <v-btn color="success" size="small" @click="mostrarModalVariante = true">
          <v-icon left>mdi-plus</v-icon>
          Agregar Variante
        </v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-0">
        <v-progress-linear v-if="cargandoVariantes" indeterminate color="primary"></v-progress-linear>

        <v-alert v-else-if="variantes.length === 0" type="info" variant="tonal" class="ma-4">
          Este producto no tiene variantes. Agrega tallas y colores con su stock.
        </v-alert>

        <v-table v-else density="comfortable">
          <thead>
            <tr>
              <th>Código</th>
              <th>Talla</th>
              <th>Color</th>
              <th>Stock Actual</th>
              <th>Stock Mínimo</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="variante in variantes" :key="variante.id">
              <td><span class="text-caption">{{ variante.codigo_variante }}</span></td>
              <td>{{ variante.talla_nombre }}</td>
              <td>
                <v-chip
                  size="small"
                  :style="{ backgroundColor: getColorHex(variante.color), color: '#fff' }"
                >
                  {{ variante.color_nombre }}
                </v-chip>
              </td>
              <td>
                <v-chip
                  size="small"
                  :color="getStockColor(variante)"
                  variant="flat"
                >
                  {{ variante.stock_actual }}
                </v-chip>
              </td>
              <td>{{ variante.stock_minimo }}</td>
              <td>
                <v-chip
                  :color="variante.activo ? 'success' : 'grey'"
                  size="small"
                  variant="flat"
                >
                  {{ variante.activo ? 'Activo' : 'Inactivo' }}
                </v-chip>
              </td>
              <td>
                <v-btn
                  icon
                  size="small"
                  color="warning"
                  variant="text"
                  @click="editarVariante(variante)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  size="small"
                  color="error"
                  variant="text"
                  @click="eliminarVariante(variante.id)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>

    <!-- Modal para agregar/editar variante -->
    <v-dialog v-model="mostrarModalVariante" max-width="600px">
      <v-card>
        <v-card-title class="text-h5 primary white--text">
          <v-icon left color="white">mdi-package-variant</v-icon>
          {{ varianteEditando ? 'Editar' : 'Nueva' }} Variante
        </v-card-title>
        <v-card-text class="pa-6">
          <v-form @submit.prevent="guardarVariante">
            <v-select
              v-model="formVariante.talla"
              :items="tallas"
              item-title="nombre"
              item-value="id"
              label="Talla *"
              variant="outlined"
              density="comfortable"
              required
              :disabled="!!varianteEditando"
            ></v-select>

            <v-select
              v-model="formVariante.color"
              :items="colores"
              item-title="nombre"
              item-value="id"
              label="Color *"
              variant="outlined"
              density="comfortable"
              required
              :disabled="!!varianteEditando"
              class="mt-4"
            ></v-select>

            <v-text-field
              v-model.number="formVariante.stock_actual"
              label="Stock Actual *"
              variant="outlined"
              density="comfortable"
              type="number"
              min="0"
              required
              class="mt-4"
            ></v-text-field>

            <v-text-field
              v-model.number="formVariante.stock_minimo"
              label="Stock Mínimo *"
              variant="outlined"
              density="comfortable"
              type="number"
              min="0"
              required
              class="mt-4"
            ></v-text-field>

            <v-checkbox
              v-model="formVariante.activo"
              label="Activo"
              color="primary"
              class="mt-4"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarModalVariante">
            Cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="guardarVariante">
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para notificaciones -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000" top>
      {{ snackbarText }}
      <template #actions>
        <v-btn variant="text" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>

    <!-- Dialog de confirmación para eliminar -->
    <v-dialog v-model="dialogEliminar" max-width="500px">
      <v-card>
        <v-card-title class="text-h5 error white--text">
          <v-icon left color="white">mdi-delete</v-icon>
          Confirmar Eliminación
        </v-card-title>
        <v-card-text class="pa-6">
          <p class="text-h6">¿Estás seguro de eliminar esta variante?</p>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="dialogEliminar = false">
            No, cancelar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="confirmarEliminarVariante">
            Sí, eliminar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProductoForm',
  data() {
    return {
      form: {
        codigo: '',
        nombre: '',
        descripcion: '',
        categoria: '',
        marca: '',
        precio_compra: 0,
        precio_venta: 0,
        activo: true
      },
      categorias: [],
      marcas: [],
      tallas: [],
      colores: [],
      variantes: [],
      esEdicion: false,
      productoId: null,
      cargandoVariantes: false,
      mostrarModalVariante: false,
      varianteEditando: null,
      formVariante: {
        producto: null,
        talla: '',
        color: '',
        stock_actual: 0,
        stock_minimo: 5,
        activo: true
      },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogEliminar: false,
      varianteIdEliminar: null
    }
  },
  async created() {
    await this.cargarDatos()

    if (this.$route.params.id) {
      this.esEdicion = true
      this.productoId = this.$route.params.id
      await this.cargarProducto()
      await this.cargarVariantes()
    }
  },
  methods: {
    async cargarDatos() {
      try {
        const [catRes, marcaRes, tallasRes, coloresRes] = await Promise.all([
          api.getCategorias(),
          api.getMarcas(),
          api.getTallas(),
          api.getColores()
        ])
        const categorias = catRes.data.results || catRes.data || []
        const marcas = marcaRes.data.results || marcaRes.data || []
        const tallas = tallasRes.data.results || tallasRes.data || []
        const colores = coloresRes.data.results || coloresRes.data || []

        this.categorias = categorias.filter(c => c.activo)
        this.marcas = marcas.filter(m => m.activo)
        this.tallas = tallas
        this.colores = colores
      } catch (error) {
        console.error('Error al cargar datos:', error)
        console.error('Detalles:', error.response?.data)
      }
    },
    async cargarProducto() {
      try {
        const response = await api.getProducto(this.productoId)
        this.form = { ...response.data }
      } catch (error) {
        console.error('Error al cargar producto:', error)
        this.showSnackbar('Error al cargar el producto', 'error')
        this.$router.push('/productos')
      }
    },
    async guardarProducto() {
      try {
        if (this.esEdicion) {
          await api.updateProducto(this.productoId, this.form)
          this.showSnackbar('Producto actualizado correctamente', 'success')
        } else {
          await api.createProducto(this.form)
          this.showSnackbar('Producto creado correctamente', 'success')
        }
        setTimeout(() => {
          this.$router.push('/productos')
        }, 1000)
      } catch (error) {
        console.error('Error al guardar producto:', error)
        this.showSnackbar('Error al guardar el producto', 'error')
      }
    },
    async cargarVariantes() {
      try {
        this.cargandoVariantes = true
        const response = await api.getProductoVariantes()
        const todasVariantes = response.data.results || response.data || []
        this.variantes = todasVariantes.filter(v => v.producto === parseInt(this.productoId))
      } catch (error) {
        console.error('Error al cargar variantes:', error)
      } finally {
        this.cargandoVariantes = false
      }
    },
    editarVariante(variante) {
      this.varianteEditando = variante
      this.formVariante = {
        producto: variante.producto,
        talla: variante.talla,
        color: variante.color,
        stock_actual: variante.stock_actual,
        stock_minimo: variante.stock_minimo,
        activo: variante.activo
      }
      this.mostrarModalVariante = true
    },
    async guardarVariante() {
      try {
        // Generar código de variante
        const talla = this.tallas.find(t => t.id === this.formVariante.talla)
        const color = this.colores.find(c => c.id === this.formVariante.color)
        const codigo_variante = `${this.form.codigo}-${talla.nombre}-${color.nombre.substring(0, 3).toUpperCase()}`

        const data = {
          ...this.formVariante,
          producto: parseInt(this.productoId),
          codigo_variante: this.varianteEditando ? this.varianteEditando.codigo_variante : codigo_variante
        }

        if (this.varianteEditando) {
          await api.updateProductoVariante(this.varianteEditando.id, data)
          this.showSnackbar('Variante actualizada correctamente', 'success')
        } else {
          await api.createProductoVariante(data)
          this.showSnackbar('Variante creada correctamente', 'success')
        }
        await this.cargarVariantes()
        this.cerrarModalVariante()
      } catch (error) {
        console.error('Error al guardar variante:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al guardar la variante. Verifica que la combinación talla/color no exista.', 'error')
      }
    },
    eliminarVariante(id) {
      this.varianteIdEliminar = id
      this.dialogEliminar = true
    },
    async confirmarEliminarVariante() {
      try {
        await api.deleteProductoVariante(this.varianteIdEliminar)
        this.showSnackbar('Variante eliminada correctamente', 'success')
        await this.cargarVariantes()
        this.dialogEliminar = false
        this.varianteIdEliminar = null
      } catch (error) {
        console.error('Error al eliminar variante:', error)
        this.showSnackbar('Error al eliminar la variante', 'error')
      }
    },
    cerrarModalVariante() {
      this.mostrarModalVariante = false
      this.varianteEditando = null
      this.formVariante = {
        producto: null,
        talla: '',
        color: '',
        stock_actual: 0,
        stock_minimo: 5,
        activo: true
      }
    },
    getStockColor(variante) {
      if (variante.stock_actual === 0) return 'error'
      if (variante.stock_actual <= variante.stock_minimo) return 'warning'
      return 'success'
    },
    getColorHex(colorId) {
      const color = this.colores.find(c => c.id === colorId)
      return color ? color.codigo_hex : '#999999'
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
.gap-2 {
  gap: 8px;
}
</style>
