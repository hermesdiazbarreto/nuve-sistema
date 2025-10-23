<template>
  <v-container fluid class="mt-4">
    <h2 class="mb-4">Imprimir Etiquetas con Código QR</h2>

    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="3">
          <v-card-title class="bg-primary">
            <span class="text-white">Seleccionar Productos</span>
          </v-card-title>
          <v-card-text class="pt-4">
            <v-text-field
              v-model="busqueda"
              variant="outlined"
              density="comfortable"
              placeholder="Buscar producto o código..."
              prepend-inner-icon="mdi-magnify"
              clearable
              class="mb-4"
            ></v-text-field>

            <div style="max-height: 500px; overflow-y: auto;">
              <v-list>
                <v-list-item
                  v-for="variante in variantesFiltradas"
                  :key="variante.id"
                  @click="toggleVariante(variante)"
                  :class="{ 'bg-blue-lighten-5': variantesSeleccionadas.includes(variante.id) }"
                >
                  <template v-slot:prepend>
                    <v-checkbox-btn
                      :model-value="variantesSeleccionadas.includes(variante.id)"
                      @click.stop="toggleVariante(variante)"
                    ></v-checkbox-btn>
                  </template>

                  <v-list-item-title>
                    {{ variante.producto_nombre }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ variante.codigo_variante }} | Talla: {{ variante.talla_nombre }} | Color: {{ variante.color_nombre }}
                  </v-list-item-subtitle>

                  <template v-slot:append>
                    <v-chip size="small">{{ formatearPrecio(variante.precio_venta) }}</v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn
              color="primary"
              block
              :disabled="variantesSeleccionadas.length === 0"
              @click="imprimirEtiquetas"
            >
              <v-icon left>mdi-printer</v-icon>
              Imprimir {{ variantesSeleccionadas.length }} Etiqueta(s)
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="3">
          <v-card-title class="bg-secondary">
            <span class="text-white">Vista Previa</span>
          </v-card-title>
          <v-card-text class="pt-4">
            <div v-if="variantesSeleccionadas.length === 0" class="text-center text-grey py-8">
              <v-icon size="64" color="grey-lighten-1">mdi-tag-off</v-icon>
              <p class="mt-4">Selecciona productos para ver la vista previa</p>
            </div>

            <div v-else id="area-impresion" class="etiquetas-container">
              <div
                v-for="variante in getVariantesParaImprimir()"
                :key="variante.id"
                class="etiqueta"
              >
                <div class="etiqueta-contenido">
                  <h3 class="etiqueta-nombre">{{ variante.producto_nombre }}</h3>
                  <div class="etiqueta-detalles">
                    <span><strong>Talla:</strong> {{ variante.talla_nombre }}</span>
                    <span class="ml-3"><strong>Color:</strong> {{ variante.color_nombre }}</span>
                  </div>
                  <div class="etiqueta-precio">
                    Precio: {{ formatearPrecio(variante.precio_venta) }}
                  </div>
                  <div class="etiqueta-qr">
                    <img v-if="variante.qr_code" :src="getQrUrl(variante.qr_code)" alt="QR Code" class="qr-image" />
                    <div v-else class="sin-qr">Sin QR</div>
                  </div>
                  <div class="etiqueta-codigo">
                    {{ variante.codigo_variante }}
                  </div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      :timeout="3000"
      top
    >
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script>
import api from '../services/api'
import formatoPrecio from '../mixins/formatoPrecio'

export default {
  name: 'ImprimirEtiquetasQR',
  mixins: [formatoPrecio],
  data() {
    return {
      busqueda: '',
      variantes: [],
      variantesSeleccionadas: [],
      productos: [],
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success'
    }
  },
  computed: {
    variantesFiltradas() {
      if (!this.busqueda) {
        return this.variantes
      }

      const busquedaLower = this.busqueda.toLowerCase()
      return this.variantes.filter(v =>
        v.producto_nombre.toLowerCase().includes(busquedaLower) ||
        v.codigo_variante.toLowerCase().includes(busquedaLower) ||
        v.talla_nombre.toLowerCase().includes(busquedaLower) ||
        v.color_nombre.toLowerCase().includes(busquedaLower)
      )
    }
  },
  mounted() {
    this.cargarDatos()
  },
  methods: {
    async cargarDatos() {
      try {
        const [variantesRes, productosRes] = await Promise.all([
          api.getProductoVariantes(),
          api.getProductos()
        ])

        const variantes = variantesRes.data.results || variantesRes.data || []
        const productos = productosRes.data.results || productosRes.data || []

        this.productos = productos

        this.variantes = variantes.map(v => {
          const producto = productos.find(p => p.id === v.producto)
          return {
            ...v,
            precio_venta: producto ? producto.precio_venta : 0
          }
        })
      } catch (error) {
        console.error('Error al cargar datos:', error)
        this.showSnackbar('Error al cargar productos', 'error')
      }
    },
    toggleVariante(variante) {
      const index = this.variantesSeleccionadas.indexOf(variante.id)
      if (index > -1) {
        this.variantesSeleccionadas.splice(index, 1)
      } else {
        this.variantesSeleccionadas.push(variante.id)
      }
    },
    getVariantesParaImprimir() {
      return this.variantes.filter(v => this.variantesSeleccionadas.includes(v.id))
    },
    getQrUrl(qrPath) {
      if (qrPath && qrPath.startsWith('http')) {
        return qrPath
      }
      const baseUrl = process.env.VUE_APP_API_URL || 'https://nuve-sistema-production.up.railway.app'
      const cleanBaseUrl = baseUrl.replace(/\/api$/, '')
      return `${cleanBaseUrl}${qrPath}`
    },
    imprimirEtiquetas() {
      window.print()
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
.etiquetas-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 10px;
}

.etiqueta {
  border: 2px solid #333;
  border-radius: 8px;
  padding: 15px;
  background: white;
  page-break-inside: avoid;
  break-inside: avoid;
}

.etiqueta-contenido {
  text-align: center;
}

.etiqueta-nombre {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.etiqueta-detalles {
  font-size: 12px;
  margin-bottom: 8px;
  color: #666;
}

.etiqueta-precio {
  font-size: 18px;
  font-weight: bold;
  margin: 10px 0;
  color: #2196F3;
}

.etiqueta-qr {
  margin: 15px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.qr-image {
  width: 150px;
  height: 150px;
  border: 1px solid #ddd;
}

.sin-qr {
  width: 150px;
  height: 150px;
  border: 2px dashed #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.etiqueta-codigo {
  font-size: 11px;
  font-weight: bold;
  margin-top: 8px;
  color: #666;
  font-family: monospace;
}

@media print {
  .v-app-bar,
  .v-navigation-drawer,
  .v-footer,
  h2,
  .v-card-title,
  .v-card-actions,
  .v-text-field {
    display: none !important;
  }

  .v-main {
    padding: 0 !important;
  }

  .v-container {
    max-width: 100% !important;
    padding: 0 !important;
  }

  .etiquetas-container {
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 10px;
  }

  .etiqueta {
    border: 2px solid #000;
    margin-bottom: 0;
  }
}
</style>
