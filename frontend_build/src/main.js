import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

// Importar componente modal y mixin global (si existen)
// import ModalConfirm from './components/ModalConfirm.vue'
// import modalMixin from './mixins/modalMixin'

const app = createApp(App)

// Registrar componente modal globalmente (comentado por ahora, Vuetify tiene sus propios modals)
// app.component('ModalConfirm', ModalConfirm)

// Registrar mixin globalmente
// app.mixin(modalMixin)

app.use(router)
app.use(vuetify)
app.mount('#app')