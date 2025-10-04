import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'https://nuve-sistema-production.up.railway.app/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  // Productos
  getProductos() {
    return api.get('/productos/')
  },
  getProducto(id) {
    return api.get(`/productos/${id}/`)
  },
  createProducto(data) {
    return api.post('/productos/', data)
  },
  updateProducto(id, data) {
    return api.put(`/productos/${id}/`, data)
  },
  deleteProducto(id) {
    return api.delete(`/productos/${id}/`)
  }
}