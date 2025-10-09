// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#1976D2',      // Azul moderno
          secondary: '#424242',    // Gris oscuro
          accent: '#82B1FF',       // Azul claro
          error: '#FF5252',        // Rojo
          info: '#2196F3',         // Azul info
          success: '#4CAF50',      // Verde
          warning: '#FB8C00',      // Naranja
          background: '#F5F5F5',   // Fondo gris claro
          surface: '#FFFFFF',      // Blanco
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#2196F3',
          secondary: '#424242',
          accent: '#FF4081',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
          background: '#121212',
          surface: '#212121',
        },
      },
    },
  },
})

export default vuetify
