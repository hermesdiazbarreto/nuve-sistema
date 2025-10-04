import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'https://nuve-sistema-production.up.railway.app/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  // Clientes
  getClientes() {
    return api.get('/clientes/')
  },
  getCliente(id) {
    return api.get(`/clientes/${id}/`)
  },
  createCliente(data) {
    return api.post('/clientes/', data)
  },
  updateCliente(id, data) {
    return api.put(`/clientes/${id}/`, data)
  },
  deleteCliente(id) {
    return api.delete(`/clientes/${id}/`)
  }
}