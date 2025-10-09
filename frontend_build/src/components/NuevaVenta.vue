<template>
  <v-container fluid class="mt-4">
    <h2>Nueva Venta</h2>

    <v-row class="mt-4">
      <!-- Columna Izquierda: Selector de Productos (solo para INGRESO) -->
      <v-col cols="12" md="7" v-if="venta.tipo_movimiento === 'INGRESO'">
        <v-card elevation="3">
          <v-card-title class="bg-primary">
            <span class="text-white">Seleccionar Productos</span>
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="busqueda"
              variant="outlined"
              density="comfortable"
              placeholder="Buscar producto, código o variante..."
              prepend-inner-icon="mdi-magnify"
              @input="filtrarVariantes"
              class="mb-3"
            ></v-text-field>

            <div style="max-height: 500px; overflow-y: auto;">
              <v-table density="compact" hover>
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Talla</th>
                    <th>Color</th>
                    <th>Precio</th>
                    <th>Stock</th>
                    <th>Acción</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="variante in variantesFiltradas" :key="variante.id">
                    <td>{{ variante.producto_nombre }}</td>
                    <td>{{ variante.talla_nombre }}</td>
                    <td>{{ variante.color_nombre }}</td>
                    <td>${{ Number(variante.precio_venta).toFixed(2) }}</td>
                    <td>
                      <v-chip
                        :color="variante.stock_actual > 0 ? 'success' : 'error'"
                        size="small"
                        variant="flat"
                      >
                        {{ variante.stock_actual }}
                      </v-chip>
                    </td>
                    <td>
                      <v-btn
                        @click="agregarAlCarrito(variante)"
                        :disabled="variante.stock_actual === 0"
                        color="primary"
                        size="small"
                      >
                        <v-icon left>mdi-plus</v-icon> Agregar
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
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
          <v-card-text>
            <!-- Selector de Tipo de Movimiento -->
            <v-select
              v-model="venta.tipo_movimiento"
              :items="[
                { title: 'Ingreso (Venta)', value: 'INGRESO' },
                { title: 'Egreso (Gasto)', value: 'EGRESO' }
              ]"
              label="Tipo de Movimiento *"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            ></v-select>

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
              <strong class="text-error">${{ Number(venta.monto_egreso || 0).toFixed(2) }}</strong>
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
          <v-card-text>
            <!-- Selector de Tipo de Movimiento -->
            <v-select
              v-model="venta.tipo_movimiento"
              :items="[
                { title: 'Ingreso (Venta)', value: 'INGRESO' },
                { title: 'Egreso (Gasto)', value: 'EGRESO' }
              ]"
              label="Tipo de Movimiento *"
              variant="outlined"
              density="comfortable"
              class="mb-3"
            ></v-select>

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
              class="mb-3"
            ></v-select>

            <!-- Items del Carrito -->
            <div class="mb-3">
              <h6>Productos Seleccionados:</h6>
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
                  class="mb-2 pa-2"
                >
                  <div class="d-flex justify-space-between align-center">
                    <div class="flex-grow-1">
                      <strong>{{ item.nombre }}</strong><br>
                      <small class="text-medium-emphasis">
                        {{ item.talla }} - {{ item.color }}
                      </small><br>
                      <small>${{ Number(item.precio).toFixed(2) }} x {{ item.cantidad }}</small>
                    </div>
                    <div class="d-flex align-center">
                      <v-btn
                        @click="modificarCantidad(index, -1)"
                        icon="mdi-minus"
                        size="small"
                        variant="outlined"
                      ></v-btn>
                      <v-text-field
                        v-model.number="item.cantidad"
                        type="number"
                        variant="outlined"
                        density="compact"
                        hide-details
                        class="mx-1"
                        style="width: 60px;"
                        min="1"
                        :max="item.stock_max"
                        @change="validarCantidad(index)"
                      ></v-text-field>
                      <v-btn
                        @click="modificarCantidad(index, 1)"
                        icon="mdi-plus"
                        size="small"
                        variant="outlined"
                      ></v-btn>
                      <v-btn
                        @click="eliminarDelCarrito(index)"
                        icon="mdi-delete"
                        size="small"
                        color="error"
                        class="ms-2"
                      ></v-btn>
                    </div>
                  </div>
                  <div class="text-right mt-1">
                    <strong>Subtotal: ${{ (item.precio * item.cantidad).toFixed(2) }}</strong>
                  </div>
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
              <strong>${{ subtotal.toFixed(2) }}</strong>
            </div>
            <div class="mb-2 d-flex justify-space-between text-error">
              <span>Descuento:</span>
              <strong>-${{ Number(venta.descuento).toFixed(2) }}</strong>
            </div>
            <div class="mb-2 d-flex justify-space-between">
              <span>Impuesto ({{ venta.impuesto_porcentaje }}%):</span>
              <strong>${{ impuesto.toFixed(2) }}</strong>
            </div>
            <div class="mb-3 d-flex justify-space-between text-h5">
              <span><strong>TOTAL:</strong></span>
              <strong class="text-success">${{ total.toFixed(2) }}</strong>
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
                <span>${{ Number(venta.monto_abonado || 0).toFixed(2) }}</span>
              </div>
              <div class="d-flex justify-space-between align-center">
                <span><strong>Saldo Pendiente:</strong></span>
                <span class="text-error">
                  ${{ (total - Number(venta.monto_abonado || 0)).toFixed(2) }}
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
  </v-container>
</template>

<script>
import api from '../services/api'

export default {
  name: 'NuevaVenta',
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
      snackbarColor: 'success'
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
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarDatos() {
      try {
        const [variantesRes, productosRes, clientesRes] = await Promise.all([
          api.getProductoVariantes(),
          api.getProductos(),
          api.getClientes()
        ])

        const variantes = variantesRes.data.results || variantesRes.data || []
        const productos = productosRes.data.results || productosRes.data || []
        const clientes = clientesRes.data.results || clientesRes.data || []

        this.variantes = variantes.filter(v => v.activo && v.stock_actual > 0)
        this.productos = productos
        this.clientes = clientes.filter(c => c.activo)

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
            monto_abonado: this.venta.es_abono ? Number(this.venta.monto_abonado).toFixed(2) : this.total.toFixed(2),
            tipo_pago: this.venta.tipo_pago,
            observaciones: this.venta.observaciones || '',
            detalles: this.carrito.map(item => ({
              producto_variante: item.variante_id,
              cantidad: item.cantidad,
              precio_unitario: item.precio.toFixed(2),
              subtotal: (item.precio * item.cantidad).toFixed(2)
            }))
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
    }
  }
}
</script>
