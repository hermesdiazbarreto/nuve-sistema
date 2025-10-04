<template>
  <div class="container-fluid mt-4">
    <h2>💳 Nueva Venta</h2>

    <div class="row mt-4">
      <!-- Columna Izquierda: Selector de Productos -->
      <div class="col-md-7">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Seleccionar Productos</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <input
                v-model="busqueda"
                type="text"
                class="form-control"
                placeholder="Buscar producto, código o variante..."
                @input="filtrarVariantes"
              >
            </div>

            <div style="max-height: 500px; overflow-y: auto;">
              <div class="table-responsive">
                <table class="table table-sm table-hover">
                  <thead class="table-dark sticky-top">
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
                        <span :class="variante.stock_actual > 0 ? 'badge bg-success' : 'badge bg-danger'">
                          {{ variante.stock_actual }}
                        </span>
                      </td>
                      <td>
                        <button
                          @click="agregarAlCarrito(variante)"
                          :disabled="variante.stock_actual === 0"
                          class="btn btn-sm btn-primary"
                        >
                          ➕ Agregar
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Columna Derecha: Carrito y Resumen -->
      <div class="col-md-5">
        <div class="card">
          <div class="card-header bg-success text-white">
            <h5 class="mb-0">🛒 Carrito de Compra</h5>
          </div>
          <div class="card-body">
            <!-- Selector de Tipo de Movimiento -->
            <div class="mb-3">
              <label class="form-label">Tipo de Movimiento *</label>
              <select v-model="venta.tipo_movimiento" class="form-select">
                <option value="INGRESO">💰 Ingreso (Venta)</option>
                <option value="EGRESO">💸 Egreso (Gasto)</option>
              </select>
            </div>

            <!-- Selector de Cliente -->
            <div class="mb-3">
              <label class="form-label">Cliente (Opcional)</label>
              <select v-model="venta.cliente_id" class="form-select">
                <option value="">Cliente General</option>
                <option v-for="cliente in clientes" :key="cliente.id" :value="cliente.id">
                  {{ cliente.nombre_completo }} - {{ cliente.numero_documento }}
                </option>
              </select>
            </div>

            <!-- Items del Carrito -->
            <div class="mb-3">
              <h6>Productos Seleccionados:</h6>
              <div v-if="carrito.length === 0" class="alert alert-info">
                Carrito vacío
              </div>
              <div v-else>
                <div v-for="(item, index) in carrito" :key="index" class="border p-2 mb-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-grow-1">
                      <strong>{{ item.nombre }}</strong><br>
                      <small class="text-muted">
                        {{ item.talla }} - {{ item.color }}
                      </small><br>
                      <small>${{ Number(item.precio).toFixed(2) }} x {{ item.cantidad }}</small>
                    </div>
                    <div class="d-flex align-items-center">
                      <button @click="modificarCantidad(index, -1)" class="btn btn-sm btn-outline-secondary">-</button>
                      <input
                        v-model.number="item.cantidad"
                        type="number"
                        class="form-control form-control-sm mx-1"
                        style="width: 60px;"
                        min="1"
                        :max="item.stock_max"
                        @change="validarCantidad(index)"
                      >
                      <button @click="modificarCantidad(index, 1)" class="btn btn-sm btn-outline-secondary">+</button>
                      <button @click="eliminarDelCarrito(index)" class="btn btn-sm btn-danger ms-2">🗑️</button>
                    </div>
                  </div>
                  <div class="text-end mt-1">
                    <strong>Subtotal: ${{ (item.precio * item.cantidad).toFixed(2) }}</strong>
                  </div>
                </div>
              </div>
            </div>

            <!-- Resumen de la Venta -->
            <div class="border-top pt-3">
              <div class="mb-2">
                <label class="form-label">Descuento ($)</label>
                <input v-model.number="venta.descuento" type="number" step="0.01" class="form-control" min="0" :max="subtotal">
              </div>

              <div class="mb-2">
                <label class="form-label">Impuesto (%) </label>
                <input v-model.number="venta.impuesto_porcentaje" type="number" step="0.01" class="form-control" min="0" max="100">
              </div>

              <div class="mb-2">
                <label class="form-label">Tipo de Pago *</label>
                <select v-model="venta.tipo_pago" class="form-select" required>
                  <option value="">Seleccione...</option>
                  <option value="EFECTIVO">Efectivo</option>
                  <option value="TARJETA">Tarjeta</option>
                  <option value="TRANSFERENCIA">Transferencia</option>
                  <option value="MIXTO">Mixto</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Observaciones</label>
                <textarea v-model="venta.observaciones" class="form-control" rows="2"></textarea>
              </div>

              <hr>

              <div class="mb-2 d-flex justify-content-between">
                <span>Subtotal:</span>
                <strong>${{ subtotal.toFixed(2) }}</strong>
              </div>
              <div class="mb-2 d-flex justify-content-between text-danger">
                <span>Descuento:</span>
                <strong>-${{ Number(venta.descuento).toFixed(2) }}</strong>
              </div>
              <div class="mb-2 d-flex justify-content-between">
                <span>Impuesto ({{ venta.impuesto_porcentaje }}%):</span>
                <strong>${{ impuesto.toFixed(2) }}</strong>
              </div>
              <div class="mb-3 d-flex justify-content-between fs-4">
                <span><strong>TOTAL:</strong></span>
                <strong class="text-success">${{ total.toFixed(2) }}</strong>
              </div>

              <div class="d-grid gap-2">
                <button @click="procesarVenta" class="btn btn-success btn-lg" :disabled="!puedeVender">
                  💰 Procesar Venta
                </button>
                <router-link to="/ventas" class="btn btn-secondary">
                  ❌ Cancelar
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
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
        vendedor: 1 // TODO: Obtener del usuario autenticado
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
    }
  },
  async created() {
    await this.cargarDatos()
  },
  methods: {
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
        alert('Error al cargar datos necesarios')
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
          alert('No hay suficiente stock')
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
        alert('No hay suficiente stock')
      }
    },
    validarCantidad(index) {
      const item = this.carrito[index]
      if (item.cantidad > item.stock_max) {
        item.cantidad = item.stock_max
        alert('Cantidad ajustada al stock disponible')
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
        alert('Complete todos los campos requeridos')
        return
      }

      if (confirm('¿Confirmar la venta?')) {
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
            estado: 'PAGADO',
            observaciones: this.venta.observaciones || '',
            detalles: this.carrito.map(item => ({
              producto_variante: item.variante_id,
              cantidad: item.cantidad,
              precio_unitario: item.precio.toFixed(2),
              subtotal: (item.precio * item.cantidad).toFixed(2)
            }))
          }

          console.log('Datos de venta a enviar:', ventaData)
          await api.createVenta(ventaData)
          alert('Venta registrada correctamente!')
          this.$router.push('/ventas')
        } catch (error) {
          console.error('Error al procesar venta:', error)
          console.error('Respuesta del servidor:', error.response?.data)
          alert('Error al procesar la venta: ' + JSON.stringify(error.response?.data || error.message))
        }
      }
    }
  }
}
</script>

<style scoped>
.sticky-top {
  position: sticky;
  top: 0;
  z-index: 10;
}
</style>
