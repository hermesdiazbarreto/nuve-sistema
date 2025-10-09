<template>
  <v-container class="mt-4">
    <h2>{{ isEdit ? 'Editar Cliente' : 'Agregar Cliente' }}</h2>

    <v-form @submit.prevent="guardarCliente">
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            v-model="cliente.tipo_documento"
            :items="[
              { title: 'DNI', value: 'DNI' },
              { title: 'Carné de Extranjería', value: 'CE' },
              { title: 'Pasaporte', value: 'PASAPORTE' }
            ]"
            label="Tipo de Documento:"
            variant="outlined"
            density="comfortable"
            required
          ></v-select>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="cliente.numero_documento"
            label="Número de Documento:"
            variant="outlined"
            density="comfortable"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="cliente.nombres"
            label="Nombres: *"
            variant="outlined"
            density="comfortable"
            required
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="cliente.apellidos"
            label="Apellidos: *"
            variant="outlined"
            density="comfortable"
            required
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="cliente.email"
            type="email"
            label="Email:"
            variant="outlined"
            density="comfortable"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field
            v-model="cliente.telefono"
            type="tel"
            label="Teléfono:"
            variant="outlined"
            density="comfortable"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-textarea
        v-model="cliente.direccion"
        label="Dirección:"
        variant="outlined"
        rows="2"
        class="mb-3"
      ></v-textarea>

      <v-text-field
        v-model="cliente.fecha_nacimiento"
        type="date"
        label="Fecha de Nacimiento:"
        variant="outlined"
        density="comfortable"
        class="mb-3"
      ></v-text-field>

      <div class="mb-3">
        <v-btn type="submit" color="success" class="me-2">
          <v-icon left>mdi-content-save</v-icon>
          {{ isEdit ? 'Actualizar' : 'Guardar' }}
        </v-btn>
        <v-btn :to="'/clientes'" color="secondary" variant="outlined">
          <v-icon left>mdi-cancel</v-icon>
          Cancelar
        </v-btn>
      </div>
    </v-form>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
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
      isEdit: false,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success'
    }
  },
  async created() {
    if (this.$route.params.id) {
      this.isEdit = true
      await this.cargarCliente()
    }
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async cargarCliente() {
      try {
        const response = await api.getCliente(this.$route.params.id)
        this.cliente = response.data
      } catch (error) {
        console.error('Error al cargar cliente:', error)
        this.showSnackbar('Error al cargar el cliente', 'error')
      }
    },
    async guardarCliente() {
      try {
        if (this.isEdit) {
          await api.updateCliente(this.$route.params.id, this.cliente)
          this.showSnackbar('Cliente actualizado correctamente', 'success')
        } else {
          await api.createCliente(this.cliente)
          this.showSnackbar('Cliente creado correctamente', 'success')
        }
        this.$router.push('/clientes')
      } catch (error) {
        console.error('Error al guardar cliente:', error)
        console.error('Detalles:', error.response?.data)
        this.showSnackbar('Error al guardar el cliente: ' + JSON.stringify(error.response?.data || error.message), 'error')
      }
    }
  }
}
</script>
