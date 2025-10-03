<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>🏢 Proveedores</h2>
      <button @click="mostrarModal = true" class="btn btn-primary">➕ Nuevo Proveedor</button>
    </div>

    <div v-if="loading" class="text-center">
      <div class="spinner-border"></div>
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-striped table-hover">
          <thead class="table-dark">
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
                <span class="badge" :class="prov.activo ? 'bg-success' : 'bg-secondary'">
                  {{ prov.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>
                <button @click="editarProveedor(prov)" class="btn btn-sm btn-warning me-1">✏️</button>
                <button @click="eliminarProveedor(prov.id)" class="btn btn-sm btn-danger">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="mostrarModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ proveedorEditando ? 'Editar' : 'Nuevo' }} Proveedor</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Código *</label>
                <input v-model="form.codigo" type="text" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">RUC *</label>
                <input v-model="form.ruc" type="text" class="form-control" required>
              </div>
              <div class="col-md-12 mb-3">
                <label class="form-label">Nombre *</label>
                <input v-model="form.nombre" type="text" class="form-control" required>
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Teléfono</label>
                <input v-model="form.telefono" type="text" class="form-control">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Email</label>
                <input v-model="form.email" type="email" class="form-control">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Contacto</label>
                <input v-model="form.contacto" type="text" class="form-control">
              </div>
              <div class="col-md-12 mb-3">
                <label class="form-label">Dirección</label>
                <textarea v-model="form.direccion" class="form-control" rows="2"></textarea>
              </div>
              <div class="col-md-12 form-check">
                <input v-model="form.activo" type="checkbox" class="form-check-input" id="activo">
                <label class="form-check-label" for="activo">Activo</label>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
            <button type="button" class="btn btn-primary" @click="guardarProveedor">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
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
      }
    }
  },
  async created() {
    await this.cargarProveedores()
  },
  methods: {
    async cargarProveedores() {
      try {
        this.loading = true
        const response = await api.getProveedores()
        this.proveedores = response.data.results || response.data
      } catch (error) {
        console.error('Error:', error)
        alert('Error al cargar proveedores')
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
        alert('Proveedor guardado correctamente')
      } catch (error) {
        console.error('Error:', error)
        alert('Error al guardar el proveedor')
      }
    },
    async eliminarProveedor(id) {
      if (confirm('¿Eliminar este proveedor?')) {
        try {
          await api.deleteProveedor(id)
          await this.cargarProveedores()
          alert('Proveedor eliminado')
        } catch (error) {
          alert('Error al eliminar')
        }
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
