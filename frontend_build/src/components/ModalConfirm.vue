<template>
  <!-- Modal de Confirmación -->
  <div v-if="show" class="modal d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5); position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999;">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header" :class="headerClass">
          <h5 class="modal-title">{{ title }}</h5>
          <button v-if="showClose" type="button" class="close" @click="cancel" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div v-if="icon" class="text-center mb-3">
            <div style="font-size: 4rem;">{{ icon }}</div>
          </div>
          <div v-html="message"></div>
        </div>
        <div class="modal-footer">
          <button v-if="showCancelButton" type="button" class="btn btn-secondary" @click="cancel">
            {{ cancelText }}
          </button>
          <button type="button" :class="confirmButtonClass" @click="confirm">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalConfirm',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Confirmación'
    },
    message: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'confirm', // confirm, alert, success, error, warning, danger
      validator: (value) => ['confirm', 'alert', 'success', 'error', 'warning', 'danger'].includes(value)
    },
    confirmText: {
      type: String,
      default: 'Aceptar'
    },
    cancelText: {
      type: String,
      default: 'Cancelar'
    },
    showCancelButton: {
      type: Boolean,
      default: true
    },
    showClose: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    headerClass() {
      const classes = {
        confirm: 'bg-primary text-white',
        alert: 'bg-info text-white',
        success: 'bg-success text-white',
        error: 'bg-danger text-white',
        warning: 'bg-warning text-dark',
        danger: 'bg-danger text-white'
      }
      return classes[this.type] || 'bg-primary text-white'
    },
    confirmButtonClass() {
      const classes = {
        confirm: 'btn btn-primary',
        alert: 'btn btn-info',
        success: 'btn btn-success',
        error: 'btn btn-danger',
        warning: 'btn btn-warning',
        danger: 'btn btn-danger'
      }
      return classes[this.type] || 'btn btn-primary'
    }
  },
  methods: {
    confirm() {
      this.$emit('confirm')
    },
    cancel() {
      this.$emit('cancel')
    }
  }
}
</script>
