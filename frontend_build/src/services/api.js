import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'https://nuve-sistema-production.up.railway.app/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Interceptor para agregar el token a cada petición
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token inválido o expirado, redirigir a login
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // ============ CATEGORÍAS ============
  getCategorias() {
    return api.get('/categorias/')
  },
  getCategoria(id) {
    return api.get(`/categorias/${id}/`)
  },
  createCategoria(data) {
    return api.post('/categorias/', data)
  },
  updateCategoria(id, data) {
    return api.put(`/categorias/${id}/`, data)
  },
  deleteCategoria(id) {
    return api.delete(`/categorias/${id}/`)
  },

  // ============ MARCAS ============
  getMarcas() {
    return api.get('/marcas/')
  },
  getMarca(id) {
    return api.get(`/marcas/${id}/`)
  },
  createMarca(data) {
    return api.post('/marcas/', data)
  },
  updateMarca(id, data) {
    return api.put(`/marcas/${id}/`, data)
  },
  deleteMarca(id) {
    return api.delete(`/marcas/${id}/`)
  },

  // ============ TALLAS ============
  getTallas() {
    return api.get('/tallas/')
  },
  getTalla(id) {
    return api.get(`/tallas/${id}/`)
  },
  createTalla(data) {
    return api.post('/tallas/', data)
  },
  updateTalla(id, data) {
    return api.put(`/tallas/${id}/`, data)
  },
  deleteTalla(id) {
    return api.delete(`/tallas/${id}/`)
  },

  // ============ COLORES ============
  getColores() {
    return api.get('/colores/')
  },
  getColor(id) {
    return api.get(`/colores/${id}/`)
  },
  createColor(data) {
    return api.post('/colores/', data)
  },
  updateColor(id, data) {
    return api.put(`/colores/${id}/`, data)
  },
  deleteColor(id) {
    return api.delete(`/colores/${id}/`)
  },

  // ============ PRODUCTOS ============
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
    // Soft delete - elimina pero mantiene en BD
    return api.delete(`/productos/${id}/`)
  },
  activarProducto(id) {
    return api.post(`/productos/${id}/activar/`)
  },
  restaurarProducto(id) {
    // Restaurar un producto eliminado
    return api.post(`/productos/${id}/restaurar/`)
  },
  getProductosInactivos() {
    return api.get('/productos/?incluir_inactivos=true')
  },
  getProductosEliminados() {
    // Obtener solo productos eliminados
    return api.get('/productos/?solo_eliminados=true')
  },
  getProductosConEliminados() {
    // Obtener todos los productos incluyendo eliminados
    return api.get('/productos/?incluir_eliminados=true')
  },

  // ============ PRODUCTO VARIANTES ============
  getProductoVariantes() {
    return api.get('/producto-variantes/')
  },
  getProductoVariante(id) {
    return api.get(`/producto-variantes/${id}/`)
  },
  createProductoVariante(data) {
    return api.post('/producto-variantes/', data)
  },
  updateProductoVariante(id, data) {
    return api.put(`/producto-variantes/${id}/`, data)
  },
  deleteProductoVariante(id) {
    return api.delete(`/producto-variantes/${id}/`)
  },
  duplicarProductoVariante(id, data) {
    // Duplicar una variante cambiando talla/color
    // data puede contener: { talla, color, stock_actual, stock_minimo }
    return api.post(`/producto-variantes/${id}/duplicar/`, data)
  },

  // ============ CLIENTES ============
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
  },

  // ============ VENTAS ============
  getVentas() {
    return api.get('/ventas/')
  },
  getVenta(id) {
    return api.get(`/ventas/${id}/`)
  },
  createVenta(data) {
    return api.post('/ventas/', data)
  },
  updateVenta(id, data) {
    return api.put(`/ventas/${id}/`, data)
  },
  deleteVenta(id) {
    return api.delete(`/ventas/${id}/`)
  },
  registrarPagoVenta(ventaId, data) {
    // Registrar un pago/abono a una venta
    // data debe contener: { monto, tipo_pago, observaciones? }
    return api.post(`/ventas/${ventaId}/registrar_pago/`, data)
  },

  // ============ DETALLE VENTAS ============
  getDetalleVentas() {
    return api.get('/detalle-ventas/')
  },
  getDetalleVenta(id) {
    return api.get(`/detalle-ventas/${id}/`)
  },

  // ============ MOVIMIENTOS INVENTARIO ============
  getMovimientos() {
    return api.get('/movimientos/')
  },
  getMovimiento(id) {
    return api.get(`/movimientos/${id}/`)
  },

  // ============ PROVEEDORES ============
  getProveedores() {
    return api.get('/proveedores/')
  },
  getProveedor(id) {
    return api.get(`/proveedores/${id}/`)
  },
  createProveedor(data) {
    return api.post('/proveedores/', data)
  },
  updateProveedor(id, data) {
    return api.put(`/proveedores/${id}/`, data)
  },
  deleteProveedor(id) {
    return api.delete(`/proveedores/${id}/`)
  },

  // ============ ESTADÍSTICAS ============
  getEstadisticas() {
    // Esta será una vista personalizada que crearemos después
    return api.get('/estadisticas/')
  },

  // ============ PROMOCIONES WHATSAPP ============
  getPromocionesWhatsApp() {
    return api.get('/promociones-whatsapp/')
  },
  getPromocionWhatsApp(id) {
    return api.get(`/promociones-whatsapp/${id}/`)
  },
  createPromocionWhatsApp(data) {
    return api.post('/promociones-whatsapp/', data)
  },
  updatePromocionWhatsApp(id, data) {
    return api.put(`/promociones-whatsapp/${id}/`, data)
  },
  deletePromocionWhatsApp(id) {
    return api.delete(`/promociones-whatsapp/${id}/`)
  },
  enviarPromocionWhatsApp(id) {
    // Enviar promoción a todos los clientes
    return api.post(`/promociones-whatsapp/${id}/enviar_promocion/`)
  },

  // ============ ENVÍOS WHATSAPP ============
  getEnviosWhatsApp() {
    return api.get('/envios-whatsapp/')
  },
  getEnvioWhatsApp(id) {
    return api.get(`/envios-whatsapp/${id}/`)
  },
}
