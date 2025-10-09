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
                label="Código (Generado automáticamente)"
                variant="outlined"
                density="comfortable"
                readonly
                hint="Se genera automáticamente al guardar según la categoría"
                persistent-hint
                placeholder="Se generará automáticamente"
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
              >
                <template v-slot:append>
                  <v-btn
                    icon="mdi-plus"
                    size="small"
                    color="primary"
                    variant="text"
                    @click="mostrarDialogCategoria = true"
                    title="Agregar nueva categoría"
                  ></v-btn>
                </template>
              </v-select>
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
              >
                <template v-slot:append>
                  <v-btn
                    icon="mdi-plus"
                    size="small"
                    color="primary"
                    variant="text"
                    @click="mostrarDialogMarca = true"
                    title="Agregar nueva marca"
                  ></v-btn>
                </template>
              </v-select>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="precioCompraFormateado"
                label="Precio de Compra *"
                variant="outlined"
                density="comfortable"
                required
                :rules="[v => !!v || 'Precio de compra es requerido']"
                hint="Use punto como separador de miles: 90.000 = noventa mil"
                persistent-hint
                @blur="actualizarPrecioCompra"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="precioVentaFormateado"
                label="Precio de Venta *"
                variant="outlined"
                density="comfortable"
                required
                :rules="[v => !!v || 'Precio de venta es requerido']"
                hint="Use punto como separador de miles: 90.000 = noventa mil"
                persistent-hint
                @blur="actualizarPrecioVenta"
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
                <v-tooltip text="Editar variante">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      icon
                      size="small"
                      color="warning"
                      variant="text"
                      @click="editarVariante(variante)"
                    >
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
                <v-tooltip text="Clonar variante">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      icon
                      size="small"
                      color="info"
                      variant="text"
                      @click="clonarVariante(variante)"
                    >
                      <v-icon>mdi-content-copy</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
                <v-tooltip text="Eliminar variante">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      icon
                      size="small"
                      color="error"
                      variant="text"
                      @click="eliminarVariante(variante.id)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
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
          <v-icon left color="white">
            {{ varianteEditando ? 'mdi-pencil' : formVariante.stock_actual === 0 && (formVariante.talla || formVariante.color) ? 'mdi-content-copy' : 'mdi-plus' }}
          </v-icon>
          {{ varianteEditando ? 'Editar Variante' : formVariante.stock_actual === 0 && (formVariante.talla || formVariante.color) ? 'Clonar Variante' : 'Nueva Variante' }}
        </v-card-title>
        <v-card-text class="pa-6">
          <v-alert
            v-if="!varianteEditando && formVariante.stock_actual === 0 && (formVariante.talla || formVariante.color)"
            type="info"
            variant="tonal"
            density="compact"
            class="mb-4"
          >
            <div class="d-flex align-center">
              <v-icon>mdi-information</v-icon>
              <span class="ml-2">Clonando variante. Cambia la <strong>talla</strong> o el <strong>color</strong> para crear una nueva variante con las mismas características.</span>
            </div>
          </v-alert>

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
            >
              <template v-slot:append v-if="!varianteEditando">
                <v-btn
                  icon="mdi-plus"
                  size="small"
                  color="primary"
                  variant="text"
                  @click="mostrarDialogTalla = true"
                  title="Agregar nueva talla"
                ></v-btn>
              </template>
            </v-select>

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
            >
              <template v-slot:append v-if="!varianteEditando">
                <v-btn
                  icon="mdi-plus"
                  size="small"
                  color="primary"
                  variant="text"
                  @click="mostrarDialogColor = true"
                  title="Agregar nuevo color"
                ></v-btn>
              </template>
            </v-select>

            <v-text-field
              v-model.number="formVariante.stock_actual"
              label="Stock Actual *"
              variant="outlined"
              density="comfortable"
              type="number"
              min="0"
              required
              class="mt-4"
              :hint="!varianteEditando && formVariante.stock_actual === 0 && (formVariante.talla || formVariante.color) ? 'El stock inicia en 0 al clonar. Ingresa la cantidad inicial.' : ''"
              persistent-hint
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

    <!-- Dialog para agregar Categoría -->
    <v-dialog v-model="mostrarDialogCategoria" max-width="500px">
      <v-card>
        <v-card-title class="bg-primary text-white">
          <v-icon left color="white">mdi-shape-plus</v-icon>
          Nueva Categoría
        </v-card-title>
        <v-card-text class="pa-6">
          <v-text-field
            v-model="nuevaCategoria.nombre"
            label="Nombre de la Categoría *"
            variant="outlined"
            density="comfortable"
            autofocus
          ></v-text-field>
          <v-textarea
            v-model="nuevaCategoria.descripcion"
            label="Descripción"
            variant="outlined"
            density="comfortable"
            rows="2"
          ></v-textarea>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarDialogCategoria">Cancelar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="guardarCategoria">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog para agregar Marca -->
    <v-dialog v-model="mostrarDialogMarca" max-width="500px">
      <v-card>
        <v-card-title class="bg-primary text-white">
          <v-icon left color="white">mdi-tag-plus</v-icon>
          Nueva Marca
        </v-card-title>
        <v-card-text class="pa-6">
          <v-text-field
            v-model="nuevaMarca.nombre"
            label="Nombre de la Marca *"
            variant="outlined"
            density="comfortable"
            autofocus
          ></v-text-field>
          <v-textarea
            v-model="nuevaMarca.descripcion"
            label="Descripción"
            variant="outlined"
            density="comfortable"
            rows="2"
          ></v-textarea>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarDialogMarca">Cancelar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="guardarMarca">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog para agregar Talla -->
    <v-dialog v-model="mostrarDialogTalla" max-width="500px">
      <v-card>
        <v-card-title class="bg-primary text-white">
          <v-icon left color="white">mdi-resize</v-icon>
          Nueva Talla
        </v-card-title>
        <v-card-text class="pa-6">
          <v-text-field
            v-model="nuevaTalla.nombre"
            label="Nombre de la Talla *"
            variant="outlined"
            density="comfortable"
            autofocus
            hint="Ej: XS, S, M, L, XL, 36, 38, 40, etc."
            persistent-hint
          ></v-text-field>
          <v-text-field
            v-model.number="nuevaTalla.orden"
            label="Orden"
            variant="outlined"
            density="comfortable"
            type="number"
            class="mt-4"
            hint="Orden de visualización (menor número = primero)"
            persistent-hint
          ></v-text-field>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarDialogTalla">Cancelar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="guardarTalla">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog para agregar Color -->
    <v-dialog v-model="mostrarDialogColor" max-width="500px">
      <v-card>
        <v-card-title class="bg-primary text-white">
          <v-icon left color="white">mdi-palette-plus</v-icon>
          Nuevo Color
        </v-card-title>
        <v-card-text class="pa-6">
          <v-text-field
            v-model="nuevoColor.nombre"
            label="Nombre del Color *"
            variant="outlined"
            density="comfortable"
            autofocus
          ></v-text-field>
          <v-text-field
            v-model="nuevoColor.codigo_hex"
            label="Código Hexadecimal"
            variant="outlined"
            density="comfortable"
            class="mt-4"
            placeholder="#FF0000"
            hint="Ej: #FF0000 para rojo"
            persistent-hint
          >
            <template v-slot:prepend-inner v-if="nuevoColor.codigo_hex">
              <div
                :style="{
                  backgroundColor: nuevoColor.codigo_hex,
                  width: '24px',
                  height: '24px',
                  borderRadius: '4px',
                  border: '1px solid #ccc'
                }"
              ></div>
            </template>
          </v-text-field>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-btn color="grey" variant="text" @click="cerrarDialogColor">Cancelar</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="guardarColor">Guardar</v-btn>
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
      precioCompraFormateado: '',
      precioVentaFormateado: '',
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
      varianteIdEliminar: null,
      // Diálogos para agregar datos
      mostrarDialogCategoria: false,
      mostrarDialogMarca: false,
      mostrarDialogTalla: false,
      mostrarDialogColor: false,
      nuevaCategoria: {
        nombre: '',
        descripcion: '',
        activo: true
      },
      nuevaMarca: {
        nombre: '',
        descripcion: '',
        activo: true
      },
      nuevaTalla: {
        nombre: '',
        orden: 0
      },
      nuevoColor: {
        nombre: '',
        codigo_hex: ''
      }
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
        // Inicializar campos formateados con punto como separador de miles
        this.precioCompraFormateado = this.formatearParaInput(this.form.precio_compra)
        this.precioVentaFormateado = this.formatearParaInput(this.form.precio_venta)
      } catch (error) {
        console.error('Error al cargar producto:', error)
        this.showSnackbar('Error al cargar el producto', 'error')
        this.$router.push('/productos')
      }
    },
    formatearParaInput(precio) {
      if (!precio) return ''
      const numero = Number(precio)
      const esEntero = numero % 1 === 0

      // Formatear con punto como separador de miles
      const partes = numero.toFixed(esEntero ? 0 : 2).split('.')
      partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.')

      return partes.join(',')
    },
    actualizarPrecioCompra() {
      // Parsear el valor ingresado (puede tener puntos como separadores de miles)
      const valorLimpio = this.precioCompraFormateado.replace(/\./g, '').replace(/,/g, '.')
      const numero = parseFloat(valorLimpio)
      if (!isNaN(numero)) {
        this.form.precio_compra = numero
      }
    },
    actualizarPrecioVenta() {
      // Parsear el valor ingresado (puede tener puntos como separadores de miles)
      const valorLimpio = this.precioVentaFormateado.replace(/\./g, '').replace(/,/g, '.')
      const numero = parseFloat(valorLimpio)
      if (!isNaN(numero)) {
        this.form.precio_venta = numero
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
    clonarVariante(variante) {
      // No establecemos varianteEditando para que sea una nueva variante
      this.varianteEditando = null
      this.formVariante = {
        producto: parseInt(this.productoId),
        talla: variante.talla, // Mantiene la misma talla por defecto
        color: variante.color, // Mantiene el mismo color por defecto
        stock_actual: 0, // Stock inicial en 0 para la nueva variante
        stock_minimo: variante.stock_minimo, // Copia el stock mínimo
        activo: true // Nueva variante activa por defecto
      }
      this.mostrarModalVariante = true
      this.showSnackbar('Clonando variante. Cambia la talla o color para crear una nueva variante.', 'info')
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
    },
    // Métodos para Categoría
    async guardarCategoria() {
      if (!this.nuevaCategoria.nombre) {
        this.showSnackbar('El nombre es requerido', 'warning')
        return
      }
      try {
        const response = await api.createCategoria(this.nuevaCategoria)
        this.categorias.push(response.data)
        this.form.categoria = response.data.id
        this.showSnackbar('Categoría creada correctamente', 'success')
        this.cerrarDialogCategoria()
      } catch (error) {
        console.error('Error al crear categoría:', error)
        this.showSnackbar('Error al crear la categoría', 'error')
      }
    },
    cerrarDialogCategoria() {
      this.mostrarDialogCategoria = false
      this.nuevaCategoria = { nombre: '', descripcion: '', activo: true }
    },
    // Métodos para Marca
    async guardarMarca() {
      if (!this.nuevaMarca.nombre) {
        this.showSnackbar('El nombre es requerido', 'warning')
        return
      }
      try {
        const response = await api.createMarca(this.nuevaMarca)
        this.marcas.push(response.data)
        this.form.marca = response.data.id
        this.showSnackbar('Marca creada correctamente', 'success')
        this.cerrarDialogMarca()
      } catch (error) {
        console.error('Error al crear marca:', error)
        this.showSnackbar('Error al crear la marca', 'error')
      }
    },
    cerrarDialogMarca() {
      this.mostrarDialogMarca = false
      this.nuevaMarca = { nombre: '', descripcion: '', activo: true }
    },
    // Métodos para Talla
    async guardarTalla() {
      if (!this.nuevaTalla.nombre) {
        this.showSnackbar('El nombre es requerido', 'warning')
        return
      }
      try {
        const response = await api.createTalla(this.nuevaTalla)
        this.tallas.push(response.data)
        this.formVariante.talla = response.data.id
        this.showSnackbar('Talla creada correctamente', 'success')
        this.cerrarDialogTalla()
      } catch (error) {
        console.error('Error al crear talla:', error)
        this.showSnackbar('Error al crear la talla', 'error')
      }
    },
    cerrarDialogTalla() {
      this.mostrarDialogTalla = false
      this.nuevaTalla = { nombre: '', orden: 0 }
    },
    // Métodos para Color
    async guardarColor() {
      if (!this.nuevoColor.nombre) {
        this.showSnackbar('El nombre es requerido', 'warning')
        return
      }
      try {
        const response = await api.createColor(this.nuevoColor)
        this.colores.push(response.data)
        this.formVariante.color = response.data.id
        this.showSnackbar('Color creado correctamente', 'success')
        this.cerrarDialogColor()
      } catch (error) {
        console.error('Error al crear color:', error)
        this.showSnackbar('Error al crear el color', 'error')
      }
    },
    cerrarDialogColor() {
      this.mostrarDialogColor = false
      this.nuevoColor = { nombre: '', codigo_hex: '' }
    }
  }
}
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
