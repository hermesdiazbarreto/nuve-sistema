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
          primary: '#FF6BD5',      // Rosa Nuve (antes era el color principal)
          secondary: '#A855F7',    // Morado Nuve
          accent: '#EC4899',       // Rosa accent
          error: '#EF4444',        // Rojo
          info: '#3B82F6',         // Azul info
          success: '#10B981',      // Verde
          warning: '#F59E0B',      // Naranja/Amarillo
          background: '#FDF4FF',   // Fondo rosa muy claro
          surface: '#FFFFFF',      // Blanco
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#FF6BD5',
          secondary: '#A855F7',
          accent: '#EC4899',
          error: '#EF4444',
          info: '#3B82F6',
          success: '#10B981',
          warning: '#F59E0B',
          background: '#1F1B24',
          surface: '#2D2433',
        },
      },
    },
  },
})

export default vuetify
