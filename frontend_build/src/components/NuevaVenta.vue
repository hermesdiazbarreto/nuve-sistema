<template>
  <v-container fluid class="mt-4">
    <h2 class="mb-4">Nueva Venta</h2>

    <!-- Selector de Tipo de Movimiento (arriba de todo) -->
    <v-card elevation="2" class="mb-4">
      <v-card-text class="pa-4">
        <v-select
          v-model="venta.tipo_movimiento"
          :items="[
            { title: 'Ingreso (Venta)', value: 'INGRESO' },
            { title: 'Egreso (Gasto)', value: 'EGRESO' }
          ]"
          label="Tipo de Movimiento *"
          variant="outlined"
          density="comfortable"
          prepend-inner-icon="mdi-swap-horizontal"
        ></v-select>
      </v-card-text>
    </v-card>

    <v-row>
      <!-- Columna Izquierda: Selector de Productos (solo para INGRESO) -->
      <v-col cols="12" md="7" v-if="venta.tipo_movimiento === 'INGRESO'">
        <v-card elevation="3">
          <v-card-title class="bg-primary">
            <span class="text-white">Seleccionar Productos</span>
          </v-card-title>
          <v-card-text class="pt-4">
            <v-text-field
              v-model="busqueda"
              variant="outlined"
              density="comfortable"
              placeholder="Buscar producto, código o variante..."
              prepend-inner-icon="mdi-magnify"
              @input="filtrarVariantes"
              class="mb-4"
            ></v-text-field>

            <!-- Vista Desktop: Tabla -->
            <div v-if="$vuetify.display.mdAndUp" style="max-height: 500px; overflow-y: auto;">
              <v-table density="compact" hover fixed-header>
                <thead>
                  <tr>
                    <th class="text-left">Código</th>
                    <th class="text-left">Producto</th>
                    <th class="text-left">Talla</th>
                    <th class="text-left">Color</th>
                    <th class="text-left">Marca</th>
                    <th class="text-right">Precio</th>
                    <th class="text-center">Stock</th>
                    <th class="text-center">Acción</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="variante in variantesFiltradas" :key="variante.id">
                    <td class="text-left">
                      <span class="text-caption font-weight-bold">{{ variante.codigo_variante }}</span>
                    </td>
                    <td class="text-left">
                      <div class="nombre-producto">{{ variante.producto_nombre }}</div>
                      <div class="text-caption text-medium-emphasis">{{ variante.categoria_nombre }}</div>
                    </td>
                    <td class="text-left">{{ variante.talla_nombre }}</td>
                    <td class="text-left">
                      <v-chip size="x-small" :color="variante.color_hex" variant="flat">
                        {{ variante.color_nombre }}
                      </v-chip>
                    </td>
                    <td class="text-left">{{ variante.marca_nombre }}</td>
                    <td class="text-right font-weight-bold">{{ formatearPrecio(variante.precio_venta) }}</td>
                    <td class="text-center">
                      <v-chip
                        :color="variante.stock_actual > 10 ? 'success' : variante.stock_actual > 0 ? 'warning' : 'error'"
                        size="small"
                        variant="flat"
                      >
                        {{ variante.stock_actual }}
                      </v-chip>
                    </td>
                    <td class="text-center">
                      <v-btn
                        @click="agregarAlCarrito(variante)"
                        :disabled="variante.stock_actual === 0"
                        color="primary"
                        size="small"
                        variant="flat"
                      >
                        <v-icon size="small">mdi-plus</v-icon>
                        Agregar
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </div>

            <!-- Vista Móvil: Cards -->
            <div v-else style="max-height: 500px; overflow-y: auto;">
              <v-card
                v-for="variante in variantesFiltradas"
                :key="variante.id"
                class="mb-3"
                elevation="2"
              >
                <v-card-text class="pa-3">
                  <div class="d-flex justify-space-between align-center mb-2">
                    <div class="flex-grow-1">
                      <div class="nombre-producto text-body-2 font-weight-bold">
                        {{ variante.producto_nombre }}
                      </div>
                      <div class="text-caption text-medium-emphasis">
                        {{ variante.codigo_variante }}
                      </div>
                    </div>
                    <v-chip
                      :color="variante.stock_actual > 10 ? 'success' : variante.stock_actual > 0 ? 'warning' : 'error'"
                      size="small"
                      variant="flat"
                    >
                      Stock: {{ variante.stock_actual }}
                    </v-chip>
                  </div>

                  <v-divider class="my-2"></v-divider>

                  <div class="d-flex justify-space-between align-center mb-2">
                    <div class="text-caption">
                      <v-icon size="x-small">mdi-resize</v-icon> {{ variante.talla_nombre }}
                      <v-chip size="x-small" :color="variante.color_hex" variant="flat" class="ml-2">
                        {{ variante.color_nombre }}
                      </v-chip>
                    </div>
                    <div class="text-caption">{{ variante.marca_nombre }}</div>
                  </div>

                  <div class="d-flex justify-space-between align-center">
                    <div class="text-h6 font-weight-bold text-primary">
                      {{ formatearPrecio(variante.precio_venta) }}
                    </div>
                    <v-btn
                      @click="agregarAlCarrito(variante)"
                      :disabled="variante.stock_actual === 0"
                      color="primary"
                      size="small"
                      variant="flat"
                    >
                      <v-icon size="small">mdi-plus</v-icon>
                      Agregar
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Formulario para EGRESO -->
      <v-col cols="12" v-if="venta.tipo_movimiento === 'EGRESO'">
        <v-card elevation="3">
          <v-card-title class="bg-error">
            <span class="text-white">Registrar Egreso (Gasto)</span>
          </v-card-title>
          <v-card-text class="pt-4">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model.number="venta.monto_egreso"
                  type="number"
                  step="0.01"
                  label="Monto del Egreso *"
                  variant="outlined"
                  density="comfortable"
                  min="0.01"
                  required
                  placeholder="0.00"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-select
                  v-model="venta.tipo_pago"
                  :items="[
                    { title: 'Seleccione...', value: '' },
                    { title: 'Efectivo', value: 'EFECTIVO' },
                    { title: 'Tarjeta', value: 'TARJETA' },
                    { title: 'Transferencia', value: 'TRANSFERENCIA' }
                  ]"
                  label="Tipo de Pago *"
                  variant="outlined"
                  density="comfortable"
                  required
                ></v-select>
              </v-col>
            </v-row>

            <v-textarea
              v-model="venta.observaciones"
              label="Descripción del Egreso *"
              variant="outlined"
              rows="3"
              required
              placeholder="Ej: Pago de servicios, compra de suministros, etc."
            ></v-textarea>

            <v-divider class="my-4"></v-divider>

            <div class="d-flex justify-space-between mb-3 text-h5">
              <span><strong>TOTAL A EGRESAR:</strong></span>
              <strong class="text-error">{{ formatearPrecio(venta.monto_egreso || 0) }}</strong>
            </div>

            <div class="d-flex flex-column ga-2">
              <v-btn
                @click="procesarEgreso"
                color="error"
                size="large"
                :disabled="!puedeRegistrarEgreso"
                block
              >
                <v-icon left>mdi-cash-multiple</v-icon> Registrar Egreso
              </v-btn>
              <v-btn
                :to="'/ventas'"
                color="secondary"
                variant="outlined"
                block
              >
                <v-icon left>mdi-cancel</v-icon> Cancelar
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Columna Derecha: Carrito y Resumen (solo para INGRESO) -->
      <v-col cols="12" md="5" v-if="venta.tipo_movimiento === 'INGRESO'">
        <v-card elevation="3">
          <v-card-title class="bg-success">
            <span class="text-white">Carrito de Compra</span>
          </v-card-title>
          <v-card-text class="pt-4">
            <!-- Selector de Cliente -->
            <v-select
              v-model="venta.cliente_id"
              :items="[
                { title: 'Cliente General', value: '' },
                ...clientes.map(c => ({
                  title: `${c.nombre_completo} - ${c.numero_documento}`,
                  value: c.id
                }))
              ]"
              label="Cliente (Opcional)"
              variant="outlined"
              density="comfortable"
              prepend-inner-icon="mdi-account"
              class="mb-4"
            ></v-select>

            <!-- Items del Carrito -->
            <div class="mb-4">
              <h6 class="mb-3 text-subtitle-1 font-weight-bold">
                <v-icon size="small" class="mr-1">mdi-cart</v-icon>
                Productos Seleccionados:
              </h6>
              <v-alert
                v-if="carrito.length === 0"
                type="info"
                variant="tonal"
              >
                Carrito vacío
              </v-alert>
              <div v-else>
                <v-card
                  v-for="(item, index) in carrito"
                  :key="index"
                  variant="outlined"
                  class="mb-3"
                >
                  <v-card-text class="pa-3">
                    <div class="d-flex flex-column">
                      <!-- Información del producto -->
                      <div class="mb-2">
                        <div class="font-weight-bold text-body-1 nombre-producto">{{ item.nombre }}</div>
                        <div class="text-caption text-medium-emphasis">
                          <v-icon size="x-small">mdi-resize</v-icon> {{ item.talla }}
                          <v-icon size="x-small" class="ml-2">mdi-palette</v-icon> {{ item.color }}
                          <span v-if="item.marca" class="ml-2">
                            <v-icon size="x-small">mdi-tag</v-icon> {{ item.marca }}
                          </span>
                        </div>
                        <div class="text-caption mt-1">
                          Precio unitario: <strong>{{ formatearPrecio(item.precio) }}</strong>
                        </div>
                      </div>

                      <!-- Controles de cantidad -->
                      <div class="d-flex justify-space-between align-center">
                        <div class="d-flex align-center ga-1">
                          <v-btn
                            @click="modificarCantidad(index, -1)"
                            icon="mdi-minus"
                            size="x-small"
                            variant="tonal"
                            color="primary"
                          ></v-btn>
                          <v-text-field
                            v-model.number="item.cantidad"
                            type="number"
                            variant="outlined"
                            density="compact"
                            hide-details
                            class="text-center"
                            style="width: 70px;"
                            min="1"
                            :max="item.stock_max"
                            @change="validarCantidad(index)"
                          ></v-text-field>
                          <v-btn
                            @click="modificarCantidad(index, 1)"
                            icon="mdi-plus"
                            size="x-small"
                            variant="tonal"
                            color="primary"
                          ></v-btn>
                          <v-chip size="small" color="info" variant="tonal" class="ml-2">
                            Max: {{ item.stock_max }}
                          </v-chip>
                        </div>
                        <v-btn
                          @click="eliminarDelCarrito(index)"
                          icon="mdi-delete"
                          size="small"
                          color="error"
                          variant="tonal"
                        ></v-btn>
                      </div>

                      <!-- Subtotal -->
                      <v-divider class="my-2"></v-divider>
                      <div class="d-flex justify-space-between align-center">
                        <span class="text-body-2">Subtotal:</span>
                        <span class="text-h6 font-weight-bold text-success">
                          {{ formatearPrecio(item.precio * item.cantidad) }}
                        </span>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </div>

            <!-- Resumen de la Venta -->
            <v-divider class="mb-3"></v-divider>

            <v-text-field
              v-model.number="venta.descuento"
              type="number"
              step="0.01"
              label="Descuento ($)"
              variant="outlined"
              density="comfortable"
              min="0"
              :max="subtotal"
              class="mb-2"
            ></v-text-field>

            <v-text-field
              v-model.number="venta.impuesto_porcentaje"
              type="number"
              step="0.01"
              label="Impuesto (%)"
              variant="outlined"
              density="comfortable"
              min="0"
              max="100"
              class="mb-2"
            ></v-text-field>

            <v-select
              v-model="venta.tipo_pago"
              :items="[
                { title: 'Seleccione...', value: '' },
                { title: 'Efectivo', value: 'EFECTIVO' },
                { title: 'Tarjeta', value: 'TARJETA' },
                { title: 'Transferencia', value: 'TRANSFERENCIA' },
                { title: 'Mixto', value: 'MIXTO' }
              ]"
              label="Tipo de Pago *"
              variant="outlined"
              density="comfortable"
              required
              class="mb-2"
            ></v-select>

            <v-textarea
              v-model="venta.observaciones"
              label="Observaciones"
              variant="outlined"
              rows="2"
              class="mb-3"
            ></v-textarea>

            <v-divider class="mb-3"></v-divider>

            <div class="mb-2 d-flex justify-space-between">
              <span>Subtotal:</span>
              <strong>{{ formatearPrecio(subtotal) }}</strong>
            </div>
            <div class="mb-2 d-flex justify-space-between text-error">
              <span>Descuento:</span>
              <strong>-{{ formatearPrecio(venta.descuento) }}</strong>
            </div>
            <div class="mb-2 d-flex justify-space-between">
              <span>Impuesto ({{ venta.impuesto_porcentaje }}%):</span>
              <strong>{{ formatearPrecio(impuesto) }}</strong>
            </div>
            <div class="mb-3 d-flex justify-space-between text-h5">
              <span><strong>TOTAL:</strong></span>
              <strong class="text-success">{{ formatearPrecio(total) }}</strong>
            </div>

            <!-- Opción de Abono -->
            <v-divider class="mb-3"></v-divider>

            <v-checkbox
              v-model="venta.es_abono"
              label="¿Es un abono? (Pago parcial)"
              color="warning"
              hide-details
              class="mb-2"
            ></v-checkbox>

            <v-text-field
              v-if="venta.es_abono"
              v-model.number="venta.monto_abonado"
              type="number"
              step="0.01"
              label="Monto a Abonar *"
              variant="outlined"
              density="comfortable"
              min="0.01"
              :max="total"
              required
              class="mb-2"
              :rules="[
                v => !!v || 'El monto es requerido',
                v => v > 0 || 'El monto debe ser mayor a 0',
                v => v <= total || 'El monto no puede exceder el total'
              ]"
            >
              <template v-slot:prepend-inner>
                $
              </template>
            </v-text-field>

            <v-alert
              v-if="venta.es_abono && venta.monto_abonado > 0"
              type="warning"
              variant="tonal"
              density="compact"
              class="mb-3"
            >
              <div class="d-flex justify-space-between align-center">
                <span><strong>Abono:</strong></span>
                <span>{{ formatearPrecio(venta.monto_abonado || 0) }}</span>
              </div>
              <div class="d-flex justify-space-between align-center">
                <span><strong>Saldo Pendiente:</strong></span>
                <span class="text-error">
                  {{ formatearPrecio(total - Number(venta.monto_abonado || 0)) }}
                </span>
              </div>
            </v-alert>

            <div class="d-flex flex-column ga-2">
              <v-btn
                @click="procesarVenta"
                color="success"
                size="large"
                :disabled="!puedeVender"
                block
              >
                <v-icon left>mdi-cash-multiple</v-icon> Procesar Venta
              </v-btn>
              <v-btn
                :to="'/ventas'"
                color="secondary"
                variant="outlined"
                block
              >
                <v-icon left>mdi-cancel</v-icon> Cancelar
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

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
  </v-container>
</template>

<script>
import api from '../services/api'
import formatoPrecio from '../mixins/formatoPrecio'

export default {
  name: 'NuevaVenta',
  mixins: [formatoPrecio],
  data() {
    return {
      busqueda: '',
      variantes: [],
      variantesFiltradas: [],
      productos: [],
      clientes: [],
      carrito: [],
      venta: {
        tipo_movimiento: 'INGRESO', // Por defecto es Ingreso
        cliente_id: '',
        descuento: 0,
        impuesto_porcentaje: 0,
        tipo_pago: '',
        observaciones: '',
        monto_egreso: 0,
        es_abono: false,
        monto_abonado: 0,
        vendedor: 1 // TODO: Obtener del usuario autenticado
      },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      // Diálogos para agregar datos
      mostrarDialogCategoria: false,
      mostrarDialogMarca: false,
      mostrarDialogTalla: false,
      mostrarDialogColor: false,
      categorias: [],
      marcas: [],
      tallas: [],
      colores: [],
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
  computed: {
    subtotal() {
      return this.carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0)
    },
    impuesto() {
      return (this.subtotal - this.venta.descuento) * (this.venta.impuesto_porcentaje / 100)
    },
    total() {
      return this.subtotal - this.venta.descuento + this.impuesto
    },
    puedeVender() {
      return this.venta.tipo_pago && this.carrito.length > 0
    },
    puedeRegistrarEgreso() {
      return this.venta.tipo_pago && this.venta.monto_egreso > 0 && this.venta.observaciones
    }
  },
  async created() {
    await this.cargarDatos()
    // Escuchar eventos globales del navbar
    this.$root.$on('open-dialog-categoria', () => {
      this.mostrarDialogCategoria = true
    })
    this.$root.$on('open-dialog-marca', () => {
      this.mostrarDialogMarca = true
    })
    this.$root.$on('open-dialog-talla', () => {
      this.mostrarDialogTalla = true
    })
    this.$root.$on('open-dialog-color', () => {
      this.mostrarDialogColor = true
    })
  },
  beforeUnmount() {
    // Limpiar event listeners
    this.$root.$off('open-dialog-categoria')
    this.$root.$off('open-dialog-marca')
    this.$root.$off('open-dialog-talla')
    this.$root.$off('open-dialog-color')
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarDatos() {
      try {
        const [variantesRes, productosRes, clientesRes, categoriasRes, marcasRes, tallasRes, coloresRes] = await Promise.all([
          api.getProductoVariantes(),
          api.getProductos(),
          api.getClientes(),
          api.getCategorias(),
          api.getMarcas(),
          api.getTallas(),
          api.getColores()
        ])

        const variantes = variantesRes.data.results || variantesRes.data || []
        const productos = productosRes.data.results || productosRes.data || []
        const clientes = clientesRes.data.results || clientesRes.data || []
        const categorias = categoriasRes.data.results || categoriasRes.data || []
        const marcas = marcasRes.data.results || marcasRes.data || []
        const tallas = tallasRes.data.results || tallasRes.data || []
        const colores = coloresRes.data.results || coloresRes.data || []

        this.variantes = variantes.filter(v => v.activo && v.stock_actual > 0)
        this.productos = productos
        this.clientes = clientes.filter(c => c.activo)
        this.categorias = categorias.filter(c => c.activo)
        this.marcas = marcas.filter(m => m.activo)
        this.tallas = tallas
        this.colores = colores

        // Enriquecer variantes con precio de venta
        this.variantes = this.variantes.map(v => {
          const producto = this.productos.find(p => p.id === v.producto)
          return {
            ...v,
            precio_venta: producto ? producto.precio_venta : 0
          }
        })

        this.variantesFiltradas = this.variantes
      } catch (error) {
        console.error('Error al cargar datos:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al cargar datos necesarios', 'error')
      }
    },
    filtrarVariantes() {
      const termino = this.busqueda.toLowerCase()
      this.variantesFiltradas = this.variantes.filter(v =>
        v.producto_nombre.toLowerCase().includes(termino) ||
        v.codigo_variante.toLowerCase().includes(termino) ||
        v.talla_nombre.toLowerCase().includes(termino) ||
        v.color_nombre.toLowerCase().includes(termino)
      )
    },
    agregarAlCarrito(variante) {
      const existe = this.carrito.find(item => item.variante_id === variante.id)

      if (existe) {
        if (existe.cantidad < variante.stock_actual) {
          existe.cantidad++
        } else {
          this.showSnackbar('No hay suficiente stock', 'warning')
        }
      } else {
        this.carrito.push({
          variante_id: variante.id,
          nombre: variante.producto_nombre,
          talla: variante.talla_nombre,
          color: variante.color_nombre,
          marca: variante.marca_nombre,
          categoria: variante.categoria_nombre,
          precio: Number(variante.precio_venta),
          cantidad: 1,
          stock_max: variante.stock_actual
        })
      }
    },
    modificarCantidad(index, cambio) {
      const item = this.carrito[index]
      const nuevaCantidad = item.cantidad + cambio

      if (nuevaCantidad <= 0) {
        this.eliminarDelCarrito(index)
      } else if (nuevaCantidad <= item.stock_max) {
        item.cantidad = nuevaCantidad
      } else {
        this.showSnackbar('No hay suficiente stock', 'warning')
      }
    },
    validarCantidad(index) {
      const item = this.carrito[index]
      if (item.cantidad > item.stock_max) {
        item.cantidad = item.stock_max
        this.showSnackbar('Cantidad ajustada al stock disponible', 'warning')
      }
      if (item.cantidad < 1) {
        item.cantidad = 1
      }
    },
    eliminarDelCarrito(index) {
      this.carrito.splice(index, 1)
    },
    async procesarVenta() {
      if (!this.puedeVender) {
        this.showSnackbar('Complete todos los campos requeridos', 'warning')
        return
      }

      // Validar monto de abono si está activado
      if (this.venta.es_abono) {
        if (!this.venta.monto_abonado || this.venta.monto_abonado <= 0) {
          this.showSnackbar('Ingrese el monto del abono', 'warning')
          return
        }
        if (this.venta.monto_abonado > this.total) {
          this.showSnackbar('El monto del abono no puede ser mayor al total', 'warning')
          return
        }
      }

      const mensaje = this.venta.es_abono
        ? `¿Confirmar venta con abono de $${Number(this.venta.monto_abonado).toFixed(2)}?`
        : '¿Confirmar la venta?'

      if (confirm(mensaje)) {
        try {
          const ventaData = {
            tipo_movimiento: this.venta.tipo_movimiento,
            cliente: this.venta.cliente_id || null,
            vendedor: this.venta.vendedor,
            subtotal: this.subtotal.toFixed(2),
            descuento: Number(this.venta.descuento).toFixed(2),
            impuesto: this.impuesto.toFixed(2),
            total: this.total.toFixed(2),
            tipo_pago: this.venta.tipo_pago,
            observaciones: this.venta.observaciones || '',
            detalles: this.carrito.map(item => ({
              producto_variante: item.variante_id,
              cantidad: item.cantidad,
              precio_unitario: item.precio.toFixed(2),
              subtotal: (item.precio * item.cantidad).toFixed(2)
            }))
          }

          // Si es abono: enviar el monto que el usuario ingresó y marcar como ABONO
          // Si NO es abono: enviar el total completo y marcar como PAGADO
          if (this.venta.es_abono) {
            ventaData.monto_abonado = Number(this.venta.monto_abonado).toFixed(2)
            ventaData.estado = 'ABONO'
          } else {
            ventaData.monto_abonado = this.total.toFixed(2)
            ventaData.estado = 'PAGADO'
          }

          console.log('Datos de venta a enviar:', ventaData)
          const response = await api.createVenta(ventaData)

          const mensaje = this.venta.es_abono
            ? `Venta registrada con abono de $${Number(this.venta.monto_abonado).toFixed(2)}. Saldo pendiente: $${(this.total - Number(this.venta.monto_abonado)).toFixed(2)}`
            : 'Venta registrada correctamente!'

          this.showSnackbar(mensaje, 'success')

          // Esperar 2 segundos antes de redirigir para que el usuario vea el mensaje
          setTimeout(() => {
            this.$router.push('/ventas')
          }, 2000)
        } catch (error) {
          console.error('Error al procesar venta:', error)
          console.error('Respuesta del servidor:', error.response?.data)
          this.showSnackbar('Error al procesar la venta: ' + JSON.stringify(error.response?.data || error.message), 'error')
        }
      }
    },
    async procesarEgreso() {
      if (!this.puedeRegistrarEgreso) {
        this.showSnackbar('Complete todos los campos requeridos', 'warning')
        return
      }

      if (confirm('¿Confirmar el registro de este egreso?')) {
        try {
          const egresoData = {
            tipo_movimiento: 'EGRESO',
            cliente: null,
            vendedor: this.venta.vendedor,
            subtotal: Number(this.venta.monto_egreso).toFixed(2),
            descuento: 0,
            impuesto: 0,
            total: Number(this.venta.monto_egreso).toFixed(2),
            tipo_pago: this.venta.tipo_pago,
            estado: 'PAGADO',
            observaciones: this.venta.observaciones,
            detalles: [] // Los egresos no tienen detalles de productos
          }

          console.log('Datos de egreso a enviar:', egresoData)
          await api.createVenta(egresoData)
          this.showSnackbar('Egreso registrado correctamente!', 'success')
          this.$router.push('/ventas')
        } catch (error) {
          console.error('Error al procesar egreso:', error)
          console.error('Respuesta del servidor:', error.response?.data)
          this.showSnackbar('Error al procesar el egreso: ' + JSON.stringify(error.response?.data || error.message), 'error')
        }
      }
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
