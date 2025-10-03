<template>
  <div class="container mt-4">
    <h2>{{ esEdicion ? 'Editar' : 'Nuevo' }} Producto</h2>

    <div class="card mt-4">
      <div class="card-body">
        <form @submit.prevent="guardarProducto">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Código *</label>
              <input v-model="form.codigo" type="text" class="form-control" required>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Nombre *</label>
              <input v-model="form.nombre" type="text" class="form-control" required>
            </div>

            <div class="col-md-12 mb-3">
              <label class="form-label">Descripción</label>
              <textarea v-model="form.descripcion" class="form-control" rows="2"></textarea>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Categoría *</label>
              <select v-model="form.categoria" class="form-select" required>
                <option value="">Seleccione...</option>
                <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                  {{ cat.nombre }}
                </option>
              </select>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Marca *</label>
              <select v-model="form.marca" class="form-select" required>
                <option value="">Seleccione...</option>
                <option v-for="marca in marcas" :key="marca.id" :value="marca.id">
                  {{ marca.nombre }}
                </option>
              </select>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Precio de Compra *</label>
              <input v-model.number="form.precio_compra" type="number" step="0.01" class="form-control" required>
            </div>

            <div class="col-md-6 mb-3">
              <label class="form-label">Precio de Venta *</label>
              <input v-model.number="form.precio_venta" type="number" step="0.01" class="form-control" required>
            </div>

            <div class="col-md-12 mb-3 form-check">
              <input v-model="form.activo" type="checkbox" class="form-check-input" id="activo">
              <label class="form-check-label" for="activo">Producto Activo</label>
            </div>
          </div>

          <div class="mt-3">
            <button type="submit" class="btn btn-primary me-2">
              💾 Guardar Producto
            </button>
            <router-link to="/productos" class="btn btn-secondary">
              ❌ Cancelar
            </router-link>
          </div>
        </form>
      </div>
    </div>

    <!-- Sección de Variantes (solo en modo edición) -->
    <div v-if="esEdicion" class="card mt-4">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">📦 Variantes y Stock</h5>
        <button @click="mostrarModalVariante = true" class="btn btn-sm btn-success">
          ➕ Agregar Variante
        </button>
      </div>
      <div class="card-body">
        <div v-if="cargandoVariantes" class="text-center">
          <div class="spinner-border spinner-border-sm"></div>
        </div>
        <div v-else-if="variantes.length === 0" class="alert alert-info">
          Este producto no tiene variantes. Agrega tallas y colores con su stock.
        </div>
        <div v-else class="table-responsive">
          <table class="table table-sm table-hover">
            <thead class="table-light">
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
                <td><small>{{ variante.codigo_variante }}</small></td>
                <td>{{ variante.talla_nombre }}</td>
                <td>
                  <span class="badge" :style="{ backgroundColor: getColorHex(variante.color) }">
                    {{ variante.color_nombre }}
                  </span>
                </td>
                <td>
                  <span :class="getStockClass(variante)">
                    {{ variante.stock_actual }}
                  </span>
                </td>
                <td>{{ variante.stock_minimo }}</td>
                <td>
                  <span class="badge" :class="variante.activo ? 'bg-success' : 'bg-secondary'">
                    {{ variante.activo ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td>
                  <button @click="editarVariante(variante)" class="btn btn-sm btn-warning me-1">
                    ✏️
                  </button>
                  <button @click="eliminarVariante(variante.id)" class="btn btn-sm btn-danger">
                    🗑️
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal para agregar/editar variante -->
    <div v-if="mostrarModalVariante" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ varianteEditando ? 'Editar' : 'Nueva' }} Variante</h5>
            <button type="button" class="btn-close" @click="cerrarModalVariante"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="guardarVariante">
              <div class="mb-3">
                <label class="form-label">Talla *</label>
                <select v-model="formVariante.talla" class="form-select" required :disabled="varianteEditando">
                  <option value="">Seleccione...</option>
                  <option v-for="talla in tallas" :key="talla.id" :value="talla.id">
                    {{ talla.nombre }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Color *</label>
                <select v-model="formVariante.color" class="form-select" required :disabled="varianteEditando">
                  <option value="">Seleccione...</option>
                  <option v-for="color in colores" :key="color.id" :value="color.id">
                    {{ color.nombre }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Stock Actual *</label>
                <input v-model.number="formVariante.stock_actual" type="number" class="form-control" required min="0">
              </div>
              <div class="mb-3">
                <label class="form-label">Stock Mínimo *</label>
                <input v-model.number="formVariante.stock_minimo" type="number" class="form-control" required min="0">
              </div>
              <div class="mb-3 form-check">
                <input v-model="formVariante.activo" type="checkbox" class="form-check-input" id="varianteActivo">
                <label class="form-check-label" for="varianteActivo">Activo</label>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModalVariante">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarVariante">Guardar</button>
          </div>
        </div>
      </div>
    </div>
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
      } catch (error) {
        console.error('Error al cargar producto:', error)
        alert('Error al cargar el producto')
        this.$router.push('/productos')
      }
    },
    async guardarProducto() {
      try {
        if (this.esEdicion) {
          await api.updateProducto(this.productoId, this.form)
          alert('Producto actualizado correctamente')
        } else {
          await api.createProducto(this.form)
          alert('Producto creado correctamente')
        }
        this.$router.push('/productos')
      } catch (error) {
        console.error('Error al guardar producto:', error)
        alert('Error al guardar el producto')
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
          alert('Variante actualizada correctamente')
        } else {
          await api.createProductoVariante(data)
          alert('Variante creada correctamente')
        }
        await this.cargarVariantes()
        this.cerrarModalVariante()
      } catch (error) {
        console.error('Error al guardar variante:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al guardar la variante. Verifica que la combinación talla/color no exista.')
      }
    },
    async eliminarVariante(id) {
      if (confirm('¿Estás seguro de eliminar esta variante?')) {
        try {
          await api.deleteProductoVariante(id)
          alert('Variante eliminada correctamente')
          await this.cargarVariantes()
        } catch (error) {
          console.error('Error al eliminar variante:', error)
          alert('Error al eliminar la variante')
        }
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
    getStockClass(variante) {
      if (variante.stock_actual === 0) return 'badge bg-danger'
      if (variante.stock_actual <= variante.stock_minimo) return 'badge bg-warning text-dark'
      return 'badge bg-success'
    },
    getColorHex(colorId) {
      const color = this.colores.find(c => c.id === colorId)
      return color ? color.codigo_hex : '#999999'
    }
  }
}
</script>
