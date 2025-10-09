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
          primary: '#d369c6',      // Rosa principal
          secondary: '#69d37c',    // Verde complementario
          accent: '#d369c6',       // Rosa accent
          error: '#EF4444',        // Rojo
          info: '#3B82F6',         // Azul info
          success: '#69d37c',      // Verde complementario
          warning: '#F59E0B',      // Naranja/Amarillo
          background: '#fdf5fc',   // Fondo rosa muy claro
          surface: '#FFFFFF',      // Blanco
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#d369c6',
          secondary: '#69d37c',
          accent: '#d369c6',
          error: '#EF4444',
          info: '#3B82F6',
          success: '#69d37c',
          warning: '#F59E0B',
          background: '#1F1B24',
          surface: '#2D2433',
        },
      },
    },
  },
})

export default vuetify
