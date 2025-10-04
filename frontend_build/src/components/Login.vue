<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="login-logo">✨</div>
        <h2>Nuve</h2>
        <p class="text-muted">Inicia sesión en tu cuenta</p>
      </div>

      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Usuario</label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="username"
            required
            autocomplete="username"
            placeholder="Ingresa tu usuario"
          >
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            required
            autocomplete="current-password"
            placeholder="Ingresa tu contraseña"
          >
        </div>

        <button
          type="submit"
          class="btn btn-primary w-100"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
        </button>
      </form>

      <div class="login-footer">
        <small class="text-muted">
          Usuario de prueba: <strong>admin</strong> / Contraseña: <strong>admin123</strong>
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      this.loading = true

      try {
        const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
        const response = await axios.post(`${API_URL}/login/`, {
          username: this.username,
          password: this.password
        })

        // Guardar token y datos de usuario en localStorage
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify({
          id: response.data.user_id,
          username: response.data.username,
          email: response.data.email,
          first_name: response.data.first_name,
          last_name: response.data.last_name
        }))

        // Redirigir al dashboard
        this.$router.push('/')
      } catch (error) {
        console.error('Error de login:', error)
        if (error.response && error.response.data && error.response.data.error) {
          this.error = error.response.data.error
        } else {
          this.error = 'Error al iniciar sesión. Por favor, intenta de nuevo.'
        }
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    // Si ya hay un token, redirigir al dashboard
    if (localStorage.getItem('token')) {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FF6BD5 0%, #A855F7 50%, #EC4899 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: moveBackground 20s linear infinite;
}

@keyframes moveBackground {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(255, 107, 213, 0.4);
  padding: 50px 40px;
  width: 100%;
  max-width: 420px;
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
}

.login-header {
  text-align: center;
  margin-bottom: 35px;
}

.login-logo {
  font-size: 4rem;
  margin-bottom: 15px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.login-header h2 {
  color: #FF6BD5;
  font-weight: bold;
  font-size: 2.5rem;
  margin-bottom: 10px;
  letter-spacing: 2px;
}

.login-footer {
  text-align: center;
  margin-top: 25px;
  padding-top: 25px;
  border-top: 1px solid #dee2e6;
}

.form-label {
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.form-control {
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px 15px;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #FF6BD5;
  box-shadow: 0 0 0 0.25rem rgba(255, 107, 213, 0.25);
  transform: translateY(-2px);
}

.btn-primary {
  background: linear-gradient(135deg, #FF6BD5 0%, #A855F7 50%, #EC4899 100%);
  border: none;
  padding: 14px;
  font-weight: 600;
  border-radius: 10px;
  font-size: 1.05rem;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #EC4899 0%, #FF6BD5 50%, #A855F7 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(255, 107, 213, 0.5);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.alert-danger {
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #fee2e2, #fecaca);
  color: #991b1b;
}
</style>
