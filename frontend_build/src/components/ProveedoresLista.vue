<template>
  <v-container class="mt-4">
    <div class="d-flex justify-space-between align-center mb-4">
      <h2>Proveedores</h2>
      <v-btn @click="mostrarModal = true" color="primary">
        <v-icon left>mdi-plus</v-icon> Nuevo Proveedor
      </v-btn>
    </div>

    <div v-if="loading" class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else>
      <v-table hover>
        <thead>
          <tr>
            <th>Código</th>
            <th>Nombre</th>
            <th>RUC</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Contacto</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prov in proveedores" :key="prov.id">
            <td><strong>{{ prov.codigo }}</strong></td>
            <td>{{ prov.nombre }}</td>
            <td>{{ prov.ruc }}</td>
            <td>{{ prov.telefono || '-' }}</td>
            <td>{{ prov.email || '-' }}</td>
            <td>{{ prov.contacto || '-' }}</td>
            <td>
              <v-chip
                :color="prov.activo ? 'success' : 'secondary'"
                size="small"
                variant="flat"
              >
                {{ prov.activo ? 'Activo' : 'Inactivo' }}
              </v-chip>
            </td>
            <td>
              <v-btn @click="editarProveedor(prov)" icon="mdi-pencil" size="small" color="warning" class="me-1"></v-btn>
              <v-btn @click="eliminarProveedor(prov.id)" icon="mdi-delete" size="small" color="error"></v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </div>

    <!-- Modal -->
    <v-dialog v-model="mostrarModal" max-width="800">
      <v-card>
        <v-card-title class="text-h6">{{ proveedorEditando ? 'Editar' : 'Nuevo' }} Proveedor</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.codigo"
                label="Código *"
                variant="outlined"
                density="comfortable"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.ruc"
                label="RUC *"
                variant="outlined"
                density="comfortable"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="form.nombre"
                label="Nombre *"
                variant="outlined"
                density="comfortable"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.telefono"
                label="Teléfono"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.email"
                type="email"
                label="Email"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.contacto"
                label="Contacto"
                variant="outlined"
                density="comfortable"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                v-model="form.direccion"
                label="Dirección"
                variant="outlined"
                rows="2"
              ></v-textarea>
            </v-col>
            <v-col cols="12">
              <v-checkbox
                v-model="form.activo"
                label="Activo"
                color="primary"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="cerrarModal">Cancelar</v-btn>
          <v-btn color="primary" @click="guardarProveedor">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>

    <v-dialog v-model="dialogConfirm" max-width="400">
      <v-card>
        <v-card-title class="text-h6">Confirmar eliminación</v-card-title>
        <v-card-text>¿Eliminar este proveedor?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="secondary" @click="dialogConfirm = false">No</v-btn>
          <v-btn color="error" @click="confirmarEliminar">Sí</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProveedoresLista',
  data() {
    return {
      proveedores: [],
      loading: true,
      mostrarModal: false,
      proveedorEditando: null,
      form: {
        codigo: '',
        nombre: '',
        ruc: '',
        direccion: '',
        telefono: '',
        email: '',
        contacto: '',
        activo: true
      },
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success',
      dialogConfirm: false,
      proveedorIdToDelete: null
    }
  },
  async created() {
    await this.cargarProveedores()
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarProveedores() {
      try {
        this.loading = true
        const response = await api.getProveedores()
        this.proveedores = response.data.results || response.data
      } catch (error) {
        console.error('Error:', error)
        this.showSnackbar('Error al cargar proveedores', 'error')
      } finally {
        this.loading = false
      }
    },
    editarProveedor(prov) {
      this.proveedorEditando = prov
      this.form = { ...prov }
      this.mostrarModal = true
    },
    async guardarProveedor() {
      try {
        if (this.proveedorEditando) {
          await api.updateProveedor(this.proveedorEditando.id, this.form)
        } else {
          await api.createProveedor(this.form)
        }
        await this.cargarProveedores()
        this.cerrarModal()
        this.showSnackbar('Proveedor guardado correctamente', 'success')
      } catch (error) {
        console.error('Error:', error)
        this.showSnackbar('Error al guardar el proveedor', 'error')
      }
    },
    eliminarProveedor(id) {
      this.proveedorIdToDelete = id
      this.dialogConfirm = true
    },
    async confirmarEliminar() {
      try {
        await api.deleteProveedor(this.proveedorIdToDelete)
        await this.cargarProveedores()
        this.showSnackbar('Proveedor eliminado', 'success')
      } catch (error) {
        this.showSnackbar('Error al eliminar', 'error')
      } finally {
        this.dialogConfirm = false
        this.proveedorIdToDelete = null
      }
    },
    cerrarModal() {
      this.mostrarModal = false
      this.proveedorEditando = null
      this.form = {
        codigo: '',
        nombre: '',
        ruc: '',
        direccion: '',
        telefono: '',
        email: '',
        contacto: '',
        activo: true
      }
    }
  }
}
</script>
