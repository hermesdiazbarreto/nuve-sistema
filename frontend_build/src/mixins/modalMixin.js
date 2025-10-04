/**
 * Mixin global para mostrar modales en lugar de alert() y confirm()
 * Uso:
 * this.$showAlert('Mensaje de éxito', 'success')
 * this.$showConfirm('¿Estás seguro?', () => { // código si confirma }, 'warning')
 */

export default {
  data() {
    return {
      modalState: {
        show: false,
        title: '',
        message: '',
        icon: '',
        type: 'confirm',
        confirmText: 'Aceptar',
        cancelText: 'Cancelar',
        showCancelButton: true,
        showClose: true,
        onConfirm: null,
        onCancel: null
      }
    }
  },
  methods: {
    /**
     * Mostrar un alert simple (solo botón Aceptar)
     * @param {string} message - Mensaje a mostrar
     * @param {string} type - Tipo: success, error, warning, info
     * @param {string} title - Título del modal (opcional)
     */
    $showAlert(message, type = 'info', title = null) {
      const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
      }

      const titles = {
        success: 'Éxito',
        error: 'Error',
        warning: 'Advertencia',
        info: 'Información'
      }

      this.modalState = {
        show: true,
        title: title || titles[type] || 'Información',
        message,
        icon: icons[type] || '',
        type: type === 'info' ? 'alert' : type,
        confirmText: 'Aceptar',
        showCancelButton: false,
        showClose: true,
        onConfirm: () => {
          this.modalState.show = false
        },
        onCancel: null
      }
    },

    /**
     * Mostrar un confirm (botones Aceptar y Cancelar)
     * @param {string} message - Mensaje a mostrar
     * @param {function} onConfirm - Callback al confirmar
     * @param {string} type - Tipo: confirm, warning, danger
     * @param {string} title - Título del modal (opcional)
     * @param {string} confirmText - Texto del botón confirmar (opcional)
     * @param {string} cancelText - Texto del botón cancelar (opcional)
     */
    $showConfirm(message, onConfirm, type = 'confirm', title = null, confirmText = null, cancelText = null) {
      const icons = {
        confirm: '❓',
        warning: '⚠️',
        danger: '🗑️'
      }

      const titles = {
        confirm: 'Confirmación',
        warning: 'Advertencia',
        danger: 'Eliminar'
      }

      const defaultConfirmTexts = {
        confirm: 'Sí, confirmar',
        warning: 'Sí, continuar',
        danger: 'Sí, eliminar'
      }

      this.modalState = {
        show: true,
        title: title || titles[type] || 'Confirmación',
        message,
        icon: icons[type] || '❓',
        type,
        confirmText: confirmText || defaultConfirmTexts[type] || 'Aceptar',
        cancelText: cancelText || 'Cancelar',
        showCancelButton: true,
        showClose: true,
        onConfirm: () => {
          this.modalState.show = false
          if (onConfirm) onConfirm()
        },
        onCancel: () => {
          this.modalState.show = false
        }
      }
    },

    /**
     * Cerrar el modal manualmente
     */
    $closeModal() {
      this.modalState.show = false
    }
  }
}
