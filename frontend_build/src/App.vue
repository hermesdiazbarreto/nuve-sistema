<template>
  <v-app>
    <!-- App Bar / Navbar -->
    <v-app-bar
      v-if="isAuthenticated"
      app
      elevate-on-scroll
      color="primary"
      dark
      height="70"
    >
      <v-app-bar-nav-icon @click="drawer = !drawer" class="d-lg-none"></v-app-bar-nav-icon>

      <v-toolbar-title class="text-h5 font-weight-bold ml-2">
        <v-icon large class="mr-2">mdi-star-four-points</v-icon>
        Nuve
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Desktop Menu -->
      <v-btn
        v-for="item in menuItems"
        :key="item.title"
        :to="item.to"
        text
        class="d-none d-lg-flex mx-1"
      >
        <v-icon left>{{ item.icon }}</v-icon>
        {{ item.title }}
      </v-btn>

      <v-spacer></v-spacer>

      <!-- User Menu -->
      <v-menu offset-y>
        <template #activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar color="white" size="40">
              <v-icon color="primary">mdi-account-circle</v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title class="font-weight-bold">{{ username }}</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="logout">
            <template #prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Navigation Drawer (Mobile) -->
    <v-navigation-drawer
      v-if="isAuthenticated"
      v-model="drawer"
      app
      temporary
      width="280"
    >
      <v-list>
        <v-list-item class="py-4">
          <v-list-item-title class="text-h6 font-weight-bold primary--text">
            <v-icon large color="primary" class="mr-2">mdi-star-four-points</v-icon>
            Nuve
          </v-list-item-title>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item
          v-for="item in allMenuItems"
          :key="item.title"
          :to="item.to"
          link
        >
          <template #prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
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
      drawer: false,
      isAuthenticated: false,
      username: '',
      menuItems: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/' },
        { title: 'Productos', icon: 'mdi-package-variant', to: '/productos' },
        { title: 'Ventas', icon: 'mdi-point-of-sale', to: '/ventas' },
        { title: 'Clientes', icon: 'mdi-account-group', to: '/clientes' },
      ],
      allMenuItems: [
        { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/' },
        { title: 'Productos', icon: 'mdi-package-variant', to: '/productos' },
        { title: 'Categorías', icon: 'mdi-tag-multiple', to: '/categorias' },
        { title: 'Marcas', icon: 'mdi-bookmark-multiple', to: '/marcas' },
        { title: 'Tallas', icon: 'mdi-ruler', to: '/tallas' },
        { title: 'Colores', icon: 'mdi-palette', to: '/colores' },
        { title: 'Movimientos', icon: 'mdi-swap-horizontal', to: '/movimientos' },
        { title: 'Ventas', icon: 'mdi-point-of-sale', to: '/ventas' },
        { title: 'Clientes', icon: 'mdi-account-group', to: '/clientes' },
        { title: 'Proveedores', icon: 'mdi-truck', to: '/proveedores' },
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

* {
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Asegurar que v-main tenga el fondo correcto */
.v-main {
  background-color: #F5F5F5;
}

/* Animaciones suaves */
.v-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.v-btn:hover {
  transform: translateY(-2px);
}

/* Cards con sombra bonita */
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(25, 118, 210, 0.15) !important;
}
</style>
