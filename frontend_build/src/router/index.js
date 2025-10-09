import { createRouter, createWebHistory } from 'vue-router'

// Componentes principales
import Dashboard from '../components/Dashboard.vue'
import Login from '../components/Login.vue'

// Inventario
import ProductosLista from '../components/ProductosLista.vue'
import ProductoForm from '../components/ProductoForm.vue'
import ProductosEliminados from '../components/ProductosEliminados.vue'
import CategoriasLista from '../components/CategoriasLista.vue'
import MarcasLista from '../components/MarcasLista.vue'
import TallasLista from '../components/TallasLista.vue'
import ColoresLista from '../components/ColoresLista.vue'
import MovimientosLista from '../components/MovimientosLista.vue'

// Ventas
import VentasLista from '../components/VentasLista.vue'
import NuevaVenta from '../components/NuevaVenta.vue'
import VentaDetalle from '../components/VentaDetalle.vue'

// Clientes
import ClientesLista from '../components/ClientesLista.vue'

// Proveedores
import ProveedoresLista from '../components/ProveedoresLista.vue'

// Legacy components (mantener compatibilidad)
import ArticulosLista from '../components/ArticulosLista.vue'
import AdicionarArticulo from '../components/AdicionarArticulo.vue'
import ArticuloDetalle from '../components/Articulo.vue'
import AdicionarCliente from '../components/AdicionarCliente.vue'
import ClienteDetalle from '../components/Cliente.vue'

const routes = [
  // Login
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  // Dashboard
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/dashboard',
    redirect: '/'
  },

  // ========== INVENTARIO ==========
  // Productos
  {
    path: '/productos',
    name: 'ProductosLista',
    component: ProductosLista
  },
  {
    path: '/productos/eliminados',
    name: 'ProductosEliminados',
    component: ProductosEliminados
  },
  {
    path: '/productos/nuevo',
    name: 'NuevoProducto',
    component: ProductoForm
  },
  {
    path: '/productos/editar/:id',
    name: 'EditarProducto',
    component: ProductoForm
  },

  // Categorías
  {
    path: '/categorias',
    name: 'CategoriasLista',
    component: CategoriasLista
  },

  // Marcas
  {
    path: '/marcas',
    name: 'MarcasLista',
    component: MarcasLista
  },

  // Tallas
  {
    path: '/tallas',
    name: 'TallasLista',
    component: TallasLista
  },

  // Colores
  {
    path: '/colores',
    name: 'ColoresLista',
    component: ColoresLista
  },

  // Movimientos de Inventario
  {
    path: '/movimientos',
    name: 'MovimientosLista',
    component: MovimientosLista
  },

  // ========== VENTAS ==========
  {
    path: '/ventas',
    name: 'VentasLista',
    component: VentasLista
  },
  {
    path: '/ventas/nueva',
    name: 'NuevaVenta',
    component: NuevaVenta
  },
  {
    path: '/ventas/:id',
    name: 'VentaDetalle',
    component: VentaDetalle
  },

  // ========== CLIENTES ==========
  {
    path: '/clientes',
    name: 'ClientesLista',
    component: ClientesLista
  },

  // ========== PROVEEDORES ==========
  {
    path: '/proveedores',
    name: 'ProveedoresLista',
    component: ProveedoresLista
  },

  // ========== RUTAS LEGACY (compatibilidad) ==========
  {
    path: '/articulos',
    name: 'ArticulosLista',
    component: ArticulosLista
  },
  {
    path: '/adicionar-articulo',
    name: 'AdicionarArticulo',
    component: AdicionarArticulo
  },
  {
    path: '/adicionar-articulo/:id',
    name: 'EditarArticulo',
    component: AdicionarArticulo
  },
  {
    path: '/articulo/:id',
    name: 'ArticuloDetalle',
    component: ArticuloDetalle
  },
  {
    path: '/adicionar-cliente',
    name: 'AdicionarCliente',
    component: AdicionarCliente
  },
  {
    path: '/adicionar-cliente/:id',
    name: 'EditarCliente',
    component: AdicionarCliente
  },
  {
    path: '/cliente/:id',
    name: 'ClienteDetalle',
    component: ClienteDetalle
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isLoginPage = to.path === '/login'

  if (!token && !isLoginPage) {
    // Si no hay token y no está en login, redirigir a login
    next('/login')
  } else if (token && isLoginPage) {
    // Si ya está logueado e intenta ir a login, redirigir a dashboard
    next('/')
  } else {
    // En cualquier otro caso, permitir la navegación
    next()
  }
})

export default router