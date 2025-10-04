<template>
  <div id="app">
    <!-- Navbar (solo visible cuando está autenticado) -->
    <nav v-if="isAuthenticated" class="navbar navbar-expand-lg navbar-dark navbar-nuve">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <span class="brand-icon">✨</span> Nuve
        </router-link>
        
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path === '/' || $route.path === '/dashboard' }"
                to="/">
                Dashboard
              </router-link>
            </li>

            <!-- Dropdown Inventario -->
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-expanded="false">
                Inventario
              </a>
              <ul class="dropdown-menu">
                <li><router-link class="dropdown-item" to="/productos">Productos</router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><router-link class="dropdown-item" to="/categorias">Categorías</router-link></li>
                <li><router-link class="dropdown-item" to="/marcas">Marcas</router-link></li>
                <li><router-link class="dropdown-item" to="/tallas">Tallas</router-link></li>
                <li><router-link class="dropdown-item" to="/colores">Colores</router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><router-link class="dropdown-item" to="/movimientos">Movimientos</router-link></li>
              </ul>
            </li>

            <!-- Ventas -->
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path.includes('/venta') }"
                to="/ventas">
                Ventas
              </router-link>
            </li>

            <!-- Clientes -->
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path.includes('/cliente') }"
                to="/clientes">
                Clientes
              </router-link>
            </li>

            <!-- Proveedores -->
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path.includes('/proveedor') }"
                to="/proveedores">
                Proveedores
              </router-link>
            </li>
          </ul>

          <!-- Usuario y Cerrar Sesión -->
          <ul class="navbar-nav" v-if="isAuthenticated">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-toggle="dropdown" aria-expanded="false">
                👤 {{ username }}
              </a>
              <ul class="dropdown-menu dropdown-menu-right">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="logout">
                    🚪 Cerrar Sesión
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    
    <!-- Contenido principal -->
    <main>
      <router-view/>
    </main>
    
    <!-- Footer (solo visible cuando está autenticado) -->
    <footer v-if="isAuthenticated" class="footer-nuve text-center text-lg-start mt-5">
      <div class="text-center p-3">
        © 2025 Nuve - Sistema de Gestión Empresarial
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      isAuthenticated: false,
      username: ''
    }
  },
  mounted() {
    this.checkAuth()
    // Escuchar cambios de ruta para actualizar el estado de autenticación
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
        // Limpiar localStorage y redirigir al login
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
/* Paleta de Colores Nuve */
:root {
  --nuve-primary: #FF6BD5;
  --nuve-secondary: #A855F7;
  --nuve-accent: #EC4899;
  --nuve-light: #FDF4FF;
  --nuve-dark: #701A75;
  --nuve-gradient: linear-gradient(135deg, #FF6BD5 0%, #A855F7 50%, #EC4899 100%);
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

main {
  flex: 1;
}

/* Navbar Nuve */
.navbar-nuve {
  background: var(--nuve-gradient) !important;
  box-shadow: 0 2px 10px rgba(255, 107, 213, 0.3);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
  letter-spacing: 1px;
}

.brand-icon {
  font-size: 1.3rem;
  margin-right: 5px;
}

.nav-link {
  transition: all 0.3s ease;
  border-radius: 5px;
  margin: 0 5px;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.nav-link.active {
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.25);
}

.dropdown-menu {
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.dropdown-item:hover {
  background: linear-gradient(90deg, rgba(255, 107, 213, 0.1), rgba(168, 85, 247, 0.1));
  color: var(--nuve-dark);
}

/* Footer Nuve */
.footer-nuve {
  background: var(--nuve-gradient);
  color: white;
  font-weight: 500;
}

.container {
  max-width: 1200px;
}

/* Estilos para mejorar la apariencia */
.card {
  box-shadow: 0 0.125rem 0.5rem rgba(255, 107, 213, 0.1);
  border: 1px solid rgba(255, 107, 213, 0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(255, 107, 213, 0.2);
}

.table {
  background-color: white;
}

.table thead {
  background: var(--nuve-gradient) !important;
  color: white;
}

.btn-primary {
  background: var(--nuve-gradient);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 107, 213, 0.4);
}

.btn {
  margin-right: 0.5rem;
}

.me-2 {
  margin-right: 0.5rem;
}

/* Badges personalizados */
.badge.bg-success {
  background: linear-gradient(90deg, #10b981, #059669) !important;
}

.badge.bg-warning {
  background: linear-gradient(90deg, #f59e0b, #d97706) !important;
}

.badge.bg-danger {
  background: linear-gradient(90deg, #ef4444, #dc2626) !important;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }

  .table-responsive {
    font-size: 0.875rem;
  }

  .navbar-brand {
    font-size: 1.2rem;
  }
}
</style>