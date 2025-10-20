<template>
  <v-container fluid>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span class="text-h5">Promociones WhatsApp</span>
        <v-btn color="primary" @click="abrirDialogoNuevaPromocion">
          <v-icon left>mdi-plus</v-icon>
          Nueva Promoción
        </v-btn>
      </v-card-title>

      <v-card-text>
        <!-- Tabla de Promociones -->
        <v-data-table
          :headers="headers"
          :items="promociones"
          :loading="loading"
          class="elevation-1"
        >
          <!-- Estado con chip de colores -->
          <template v-slot:item.estado="{ item }">
            <v-chip
              :color="getEstadoColor(item.estado)"
              text-color="white"
              small
            >
              {{ item.estado }}
            </v-chip>
          </template>

          <!-- Fecha de creación -->
          <template v-slot:item.fecha_creacion="{ item }">
            {{ formatearFecha(item.fecha_creacion) }}
          </template>

          <!-- Fecha de envío -->
          <template v-slot:item.fecha_envio="{ item }">
            {{ item.fecha_envio ? formatearFecha(item.fecha_envio) : '-' }}
          </template>

          <!-- Estadísticas -->
          <template v-slot:item.estadisticas="{ item }">
            <div class="text-caption">
              <div v-if="item.total_destinatarios > 0">
                Total: {{ item.total_destinatarios }}<br>
                Enviados: {{ item.mensajes_enviados }}<br>
                Fallidos: {{ item.mensajes_fallidos }}
              </div>
              <div v-else>-</div>
            </div>
          </template>

          <!-- Acciones -->
          <template v-slot:item.acciones="{ item }">
            <v-btn
              v-if="item.estado === 'BORRADOR'"
              icon
              color="success"
              @click="enviarPromocion(item)"
              :loading="enviando === item.id"
            >
              <v-icon>mdi-send</v-icon>
            </v-btn>
            <v-btn icon color="info" @click="verDetalles(item)">
              <v-icon>mdi-eye</v-icon>
            </v-btn>
            <v-btn
              v-if="item.estado === 'BORRADOR'"
              icon
              color="error"
              @click="eliminarPromocion(item)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Diálogo Nueva Promoción -->
    <v-dialog v-model="dialogoNuevaPromocion" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Nueva Promoción</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="formularioValido">
            <v-text-field
              v-model="nuevaPromocion.titulo"
              label="Título de la promoción"
              :rules="[rules.required]"
              outlined
              dense
            ></v-text-field>

            <v-textarea
              v-model="nuevaPromocion.mensaje"
              label="Mensaje"
              :rules="[rules.required]"
              hint="Usa {nombre} para personalizar el mensaje con el nombre del cliente"
              persistent-hint
              outlined
              rows="5"
            ></v-textarea>

            <v-alert type="info" text dense class="mt-3">
              <strong>Ejemplo:</strong><br>
              Hola {nombre}, tenemos una nueva promoción en ropa con descuentos del 20%. ¡No te lo pierdas!
            </v-alert>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="cerrarDialogoNuevaPromocion">Cancelar</v-btn>
          <v-btn
            color="primary"
            @click="guardarPromocion"
            :disabled="!formularioValido"
            :loading="guardando"
          >
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Diálogo Detalles -->
    <v-dialog v-model="dialogoDetalles" max-width="900px">
      <v-card v-if="promocionSeleccionada">
        <v-card-title>
          <span class="text-h5">{{ promocionSeleccionada.titulo }}</span>
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <div class="text-subtitle-2">Estado</div>
              <v-chip
                :color="getEstadoColor(promocionSeleccionada.estado)"
                text-color="white"
                class="mt-1"
              >
                {{ promocionSeleccionada.estado }}
              </v-chip>
            </v-col>
            <v-col cols="12" md="6">
              <div class="text-subtitle-2">Creado por</div>
              <div>{{ promocionSeleccionada.creado_por_nombre }}</div>
            </v-col>
          </v-row>

          <v-row class="mt-3">
            <v-col cols="12">
              <div class="text-subtitle-2">Mensaje</div>
              <v-sheet color="grey lighten-4" class="pa-3 mt-1" rounded>
                {{ promocionSeleccionada.mensaje }}
              </v-sheet>
            </v-col>
          </v-row>

          <v-row class="mt-3" v-if="promocionSeleccionada.total_destinatarios > 0">
            <v-col cols="12" md="4">
              <v-card outlined>
                <v-card-text class="text-center">
                  <div class="text-h4">{{ promocionSeleccionada.total_destinatarios }}</div>
                  <div class="text-caption">Total Destinatarios</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="4">
              <v-card outlined>
                <v-card-text class="text-center">
                  <div class="text-h4 success--text">{{ promocionSeleccionada.mensajes_enviados }}</div>
                  <div class="text-caption">Enviados</div>
                </v-card-text>
              </v-card>
            </v-col>
            <v-col cols="12" md="4">
              <v-card outlined>
                <v-card-text class="text-center">
                  <div class="text-h4 error--text">{{ promocionSeleccionada.mensajes_fallidos }}</div>
                  <div class="text-caption">Fallidos</div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Lista de envíos individuales -->
          <v-row class="mt-3" v-if="promocionSeleccionada.envios && promocionSeleccionada.envios.length > 0">
            <v-col cols="12">
              <div class="text-subtitle-2 mb-2">Envíos Individuales</div>
              <v-data-table
                :headers="headersEnvios"
                :items="promocionSeleccionada.envios"
                dense
                :items-per-page="10"
              >
                <template v-slot:item.estado="{ item }">
                  <v-chip
                    :color="getEstadoEnvioColor(item.estado)"
                    text-color="white"
                    x-small
                  >
                    {{ item.estado }}
                  </v-chip>
                </template>

                <template v-slot:item.fecha_envio="{ item }">
                  {{ item.fecha_envio ? formatearFecha(item.fecha_envio) : '-' }}
                </template>
              </v-data-table>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialogoDetalles = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar para notificaciones -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
      {{ snackbar.mensaje }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.show = false">Cerrar</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'PromocionesWhatsApp',

  data() {
    return {
      promociones: [],
      loading: false,
      enviando: null,
      guardando: false,
      dialogoNuevaPromocion: false,
      dialogoDetalles: false,
      formularioValido: false,
      promocionSeleccionada: null,
      nuevaPromocion: {
        titulo: '',
        mensaje: '',
      },
      headers: [
        { text: 'Título', value: 'titulo', sortable: true },
        { text: 'Estado', value: 'estado', sortable: true },
        { text: 'Fecha Creación', value: 'fecha_creacion', sortable: true },
        { text: 'Fecha Envío', value: 'fecha_envio', sortable: true },
        { text: 'Estadísticas', value: 'estadisticas', sortable: false },
        { text: 'Acciones', value: 'acciones', sortable: false, align: 'center' },
      ],
      headersEnvios: [
        { text: 'Cliente', value: 'cliente_nombre' },
        { text: 'Teléfono', value: 'telefono' },
        { text: 'Estado', value: 'estado' },
        { text: 'Fecha Envío', value: 'fecha_envio' },
        { text: 'Error', value: 'mensaje_error' },
      ],
      rules: {
        required: (v) => !!v || 'Campo requerido',
      },
      snackbar: {
        show: false,
        mensaje: '',
        color: 'success',
      },
    }
  },

  mounted() {
    this.cargarPromociones()
  },

  methods: {
    async cargarPromociones() {
      this.loading = true
      try {
        const response = await api.getPromocionesWhatsApp()
        this.promociones = response.data
      } catch (error) {
        console.error('Error al cargar promociones:', error)
        this.mostrarSnackbar('Error al cargar promociones', 'error')
      } finally {
        this.loading = false
      }
    },

    abrirDialogoNuevaPromocion() {
      this.nuevaPromocion = {
        titulo: '',
        mensaje: '',
      }
      this.dialogoNuevaPromocion = true
    },

    cerrarDialogoNuevaPromocion() {
      this.dialogoNuevaPromocion = false
      this.$refs.form.reset()
    },

    async guardarPromocion() {
      if (!this.$refs.form.validate()) return

      this.guardando = true
      try {
        await api.createPromocionWhatsApp(this.nuevaPromocion)
        this.mostrarSnackbar('Promoción creada exitosamente', 'success')
        this.cerrarDialogoNuevaPromocion()
        this.cargarPromociones()
      } catch (error) {
        console.error('Error al crear promoción:', error)
        this.mostrarSnackbar('Error al crear promoción', 'error')
      } finally {
        this.guardando = false
      }
    },

    async enviarPromocion(promocion) {
      if (!confirm(`¿Está seguro de enviar esta promoción a todos los clientes con teléfono registrado?`)) {
        return
      }

      this.enviando = promocion.id
      try {
        const response = await api.enviarPromocionWhatsApp(promocion.id)
        const { mensajes_enviados, mensajes_fallidos } = response.data
        this.mostrarSnackbar(
          `Promoción enviada: ${mensajes_enviados} exitosos, ${mensajes_fallidos} fallidos`,
          'success'
        )
        this.cargarPromociones()
      } catch (error) {
        console.error('Error al enviar promoción:', error)
        const mensaje = error.response?.data?.error || 'Error al enviar promoción'
        this.mostrarSnackbar(mensaje, 'error')
      } finally {
        this.enviando = null
      }
    },

    async verDetalles(promocion) {
      try {
        const response = await api.getPromocionWhatsApp(promocion.id)
        this.promocionSeleccionada = response.data
        this.dialogoDetalles = true
      } catch (error) {
        console.error('Error al cargar detalles:', error)
        this.mostrarSnackbar('Error al cargar detalles', 'error')
      }
    },

    async eliminarPromocion(promocion) {
      if (!confirm(`¿Está seguro de eliminar la promoción "${promocion.titulo}"?`)) {
        return
      }

      try {
        await api.deletePromocionWhatsApp(promocion.id)
        this.mostrarSnackbar('Promoción eliminada exitosamente', 'success')
        this.cargarPromociones()
      } catch (error) {
        console.error('Error al eliminar promoción:', error)
        this.mostrarSnackbar('Error al eliminar promoción', 'error')
      }
    },

    getEstadoColor(estado) {
      const colores = {
        BORRADOR: 'grey',
        ENVIANDO: 'warning',
        ENVIADO: 'success',
        ERROR: 'error',
      }
      return colores[estado] || 'grey'
    },

    getEstadoEnvioColor(estado) {
      const colores = {
        PENDIENTE: 'warning',
        ENVIADO: 'success',
        FALLIDO: 'error',
      }
      return colores[estado] || 'grey'
    },

    formatearFecha(fecha) {
      if (!fecha) return '-'
      const date = new Date(fecha)
      return date.toLocaleString('es-CO', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
      })
    },

    mostrarSnackbar(mensaje, color = 'success') {
      this.snackbar.mensaje = mensaje
      this.snackbar.color = color
      this.snackbar.show = true
    },
  },
}
</script>

<style scoped>
.v-data-table >>> .v-data-table__wrapper {
  overflow-x: auto;
}
</style>
