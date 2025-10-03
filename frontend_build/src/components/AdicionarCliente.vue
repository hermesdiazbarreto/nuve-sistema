<template>
  <div class="container mt-4">
    <h2>{{ isEdit ? 'Editar Cliente' : 'Agregar Cliente' }}</h2>

    <form @submit.prevent="guardarCliente">
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="tipo_documento" class="form-label">Tipo de Documento:</label>
          <select class="form-select" id="tipo_documento" v-model="cliente.tipo_documento" required>
            <option value="DNI">DNI</option>
            <option value="CE">Carné de Extranjería</option>
            <option value="PASAPORTE">Pasaporte</option>
          </select>
        </div>

        <div class="col-md-6 mb-3">
          <label for="numero_documento" class="form-label">Número de Documento:</label>
          <input
            type="text"
            class="form-control"
            id="numero_documento"
            v-model="cliente.numero_documento">
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="nombres" class="form-label">Nombres: *</label>
          <input
            type="text"
            class="form-control"
            id="nombres"
            v-model="cliente.nombres"
            required>
        </div>

        <div class="col-md-6 mb-3">
          <label for="apellidos" class="form-label">Apellidos: *</label>
          <input
            type="text"
            class="form-control"
            id="apellidos"
            v-model="cliente.apellidos"
            required>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="email" class="form-label">Email:</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="cliente.email">
        </div>

        <div class="col-md-6 mb-3">
          <label for="telefono" class="form-label">Teléfono:</label>
          <input
            type="tel"
            class="form-control"
            id="telefono"
            v-model="cliente.telefono">
        </div>
      </div>

      <div class="mb-3">
        <label for="direccion" class="form-label">Dirección:</label>
        <textarea
          class="form-control"
          id="direccion"
          v-model="cliente.direccion"
          rows="2">
        </textarea>
      </div>

      <div class="mb-3">
        <label for="fecha_nacimiento" class="form-label">Fecha de Nacimiento:</label>
        <input
          type="date"
          class="form-control"
          id="fecha_nacimiento"
          v-model="cliente.fecha_nacimiento">
      </div>

      <div class="mb-3">
        <button type="submit" class="btn btn-success me-2">
          {{ isEdit ? 'Actualizar' : 'Guardar' }}
        </button>
        <router-link to="/clientes" class="btn btn-secondary">
          Cancelar
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'AdicionarCliente',
  data() {
    return {
      cliente: {
        tipo_documento: 'DNI',
        numero_documento: '',
        nombres: '',
        apellidos: '',
        email: '',
        telefono: '',
        direccion: '',
        fecha_nacimiento: '',
        activo: true
      },
      isEdit: false
    }
  },
  async created() {
    if (this.$route.params.id) {
      this.isEdit = true
      await this.cargarCliente()
    }
  },
  methods: {
    async cargarCliente() {
      try {
        const response = await api.getCliente(this.$route.params.id)
        this.cliente = response.data
      } catch (error) {
        console.error('Error al cargar cliente:', error)
        alert('Error al cargar el cliente')
      }
    },
    async guardarCliente() {
      try {
        if (this.isEdit) {
          await api.updateCliente(this.$route.params.id, this.cliente)
          alert('Cliente actualizado correctamente')
        } else {
          await api.createCliente(this.cliente)
          alert('Cliente creado correctamente')
        }
        this.$router.push('/clientes')
      } catch (error) {
        console.error('Error al guardar cliente:', error)
        console.error('Detalles:', error.response?.data)
        alert('Error al guardar el cliente: ' + JSON.stringify(error.response?.data || error.message))
      }
    }
  }
}
</script>