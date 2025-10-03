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

createApp(App).use(router).mount('#app')