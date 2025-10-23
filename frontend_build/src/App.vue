<template>
  <v-app>
    <!-- Top App Bar -->
    <v-app-bar
      v-if="isAuthenticated"
      app
      color="white"
      elevation="1"
      height="64"
    >
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title class="text-h6 font-weight-bold">
        <v-icon color="primary" class="mr-2">mdi-star-four-points</v-icon>
        Nuve
      </v-toolbar-title>
    </v-app-bar>

    <!-- Sidebar (Menú Lateral) -->
    <v-navigation-drawer
      v-if="isAuthenticated"
      v-model="drawer"
      app
      width="280"
      color="white"
      elevation="2"
    >
      <!-- Header del Sidebar -->
      <div class="sidebar-header pa-6">
        <div class="d-flex align-center mb-2">
          <v-icon size="40" color="primary">mdi-star-four-points</v-icon>
          <span class="text-h5 font-weight-bold ml-3" style="background: var(--nuve-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Nuve</span>
        </div>
        <div class="text-caption text-medium-emphasis">Sistema de Gestión</div>
      </div>

      <v-divider></v-divider>

      <!-- Menu completo en un solo v-list -->
      <v-list nav class="py-2">
        <!-- Menu Principal -->
        <v-list-item
          v-for="item in mainMenuItems"
          :key="item.title"
          :to="item.to"
          link
          rounded="xl"
          class="mx-2 my-1"
        >
          <template #prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>

        <v-divider class="my-2"></v-divider>

        <!-- Sección Maestros (Desplegable) -->
        <v-list-group value="maestros">
          <template #activator="{ props }">
            <v-list-item
              v-bind="props"
              rounded="xl"
              class="mx-2 my-1"
            >
              <template #prepend>
                <v-icon>mdi-database</v-icon>
              </template>
              <v-list-item-title>MAESTROS</v-list-item-title>
            </v-list-item>
          </template>

          <v-list-item
            v-for="item in maestrosMenuItems"
            :key="item.title"
            :to="item.to"
            link
            rounded="xl"
            class="mx-2 my-1"
          >
            <template #prepend>
              <v-icon>{{ item.icon }}</v-icon>
            </template>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list-group>

      </v-list>

      <template #append>
        <v-divider></v-divider>
        <!-- User Menu -->
        <v-list nav class="py-2">
          <v-list-item class="mx-2" rounded="xl">
            <template #prepend>
              <v-avatar color="primary" size="40">
                <v-icon color="white">mdi-account-circle</v-icon>
              </v-avatar>
            </template>
            <v-list-item-title class="font-weight-bold">{{ username }}</v-list-item-title>
            <v-list-item-subtitle>Administrador</v-list-item-subtitle>
          </v-list-item>
          <v-list-item
            @click="logout"
            rounded="xl"
            class="mx-2 my-1"
          >
            <template #prepend>
              <v-icon color="error">mdi-logout</v-icon>
            </template>
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container fluid class="pa-4">
        <router-view />
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer
      v-if="isAuthenticated"
      app
      color="primary"
      dark
      class="text-center"
    >
      <v-container>
        <v-row>
          <v-col cols="12">
            <span class="font-weight-medium">
              © {{ new Date().getFullYear() }} Nuve - Sistema de Gestión Empresarial
            </span>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      drawer: true, // Abierto por defecto en desktop
      isAuthenticated: false,
      username: '',
      mainMenuItems: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/' },
        { title: 'Productos', icon: 'mdi-package-variant', to: '/productos' },
        { title: 'Ventas', icon: 'mdi-point-of-sale', to: '/ventas' },
        { title: 'Clientes', icon: 'mdi-account-group', to: '/clientes' },
        { title: 'Proveedores', icon: 'mdi-truck', to: '/proveedores' },
        { title: 'Movimientos', icon: 'mdi-swap-horizontal', to: '/movimientos' },
        { title: 'Etiquetas QR', icon: 'mdi-qrcode', to: '/etiquetas-qr' },
      ],
      maestrosMenuItems: [
        { title: 'Categorías', icon: 'mdi-tag-multiple', to: '/categorias' },
        { title: 'Marcas', icon: 'mdi-bookmark-multiple', to: '/marcas' },
        { title: 'Tallas', icon: 'mdi-ruler', to: '/tallas' },
        { title: 'Colores', icon: 'mdi-palette', to: '/colores' },
      ],
    }
  },
  mounted() {
    this.checkAuth()
    this.$router.afterEach(() => {
      this.checkAuth()
    })
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')

      if (token && user) {
        this.isAuthenticated = true
        const userData = JSON.parse(user)
        this.username = userData.username
      } else {
        this.isAuthenticated = false
        this.username = ''
      }
    },
    async logout() {
      try {
        const token = localStorage.getItem('token')
        const API_URL = process.env.VUE_APP_API_URL || 'https://nuve-sistema-production.up.railway.app/api'
        if (token) {
          await axios.post(`${API_URL}/logout/`, {}, {
            headers: {
              'Authorization': `Token ${token}`
            }
          })
        }
      } catch (error) {
        console.error('Error al cerrar sesión:', error)
      } finally {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        this.isAuthenticated = false
        this.username = ''
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style>
/* Fuente personalizada */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Paleta de colores Nuve */
:root {
  --nuve-primary: #d369c6;
  --nuve-secondary: #69d37c;
  --nuve-accent: #d369c6;
  --nuve-gradient: linear-gradient(135deg, #d369c6 0%, #69d37c 100%);
}

* {
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Asegurar que v-main tenga el fondo correcto */
.v-main {
  background-color: #fdf5fc;
}

/* Sidebar styling */
.sidebar-header {
  background: linear-gradient(135deg, rgba(211, 105, 198, 0.05) 0%, rgba(105, 211, 124, 0.05) 100%);
}

/* Active menu item */
.v-list-item--active {
  background: var(--nuve-gradient) !important;
  color: white !important;
}

.v-list-item--active .v-icon {
  color: white !important;
}

/* Gradiente rosa/morado en footer */
.v-footer {
  background: var(--nuve-gradient) !important;
}

/* Animaciones suaves */
.v-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.v-btn:hover {
  transform: translateY(-2px);
}

/* Cards con sombra rosa */
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(211, 105, 198, 0.2) !important;
}

/* Avatar del usuario */
.v-avatar {
  border: 2px solid white;
}

/* Nombres de productos en mayúsculas - aplicar globalmente */
.nombre-producto,
.producto-nombre {
  text-transform: uppercase !important;
}
</style>
