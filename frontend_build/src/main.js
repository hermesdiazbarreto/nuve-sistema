import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Importar jQuery (necesario para Bootstrap 4)
import $ from 'jquery'
window.$ = window.jQuery = $

// Importar Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'

// Importar Popper.js y Bootstrap JS
import 'popper.js'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Importar componente modal y mixin global
import ModalConfirm from './components/ModalConfirm.vue'
import modalMixin from './mixins/modalMixin'

const app = createApp(App)

// Registrar componente modal globalmente
app.component('ModalConfirm', ModalConfirm)

// Registrar mixin globalmente
app.mixin(modalMixin)

app.use(router).mount('#app')