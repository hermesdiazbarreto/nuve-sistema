// Mixin global para formatear precios con el formato $65.000
export default {
  methods: {
    formatearPrecio(precio) {
      const numero = Number(precio)
      if (isNaN(numero)) return '$0'
      // Formatear con separador de miles (punto) sin decimales
      const precioFormateado = numero.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, '.')
      return `$${precioFormateado}`
    }
  }
}
