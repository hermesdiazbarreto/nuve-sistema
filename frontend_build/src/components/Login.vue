<template>
  <div class="login-container">
    <v-card class="login-card" elevation="24">
      <v-card-text class="pa-8">
        <div class="login-header">
          <div class="login-logo">✨</div>
          <h2 class="text-h3 font-weight-bold">Nuve</h2>
          <p class="text-medium-emphasis">Inicia sesión en tu cuenta</p>
        </div>

        <v-alert
          v-if="error"
          type="error"
          variant="tonal"
          closable
          class="mb-4"
        >
          {{ error }}
        </v-alert>

        <v-form @submit.prevent="handleLogin">
          <v-text-field
            v-model="username"
            label="Usuario"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-account"
            required
            autocomplete="username"
            placeholder="Ingresa tu usuario"
            class="mb-3"
          ></v-text-field>

          <v-text-field
            v-model="password"
            type="password"
            label="Contraseña"
            variant="outlined"
            density="comfortable"
            prepend-inner-icon="mdi-lock"
            required
            autocomplete="current-password"
            placeholder="Ingresa tu contraseña"
            class="mb-4"
          ></v-text-field>

          <v-btn
            type="submit"
            color="primary"
            size="large"
            :loading="loading"
            :disabled="loading"
            block
            class="login-btn"
          >
            {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </v-btn>
        </v-form>

        <div class="login-footer">
          <small class="text-medium-emphasis">
            Usuario de prueba: <strong>admin</strong> / Contraseña: <strong>admin123</strong>
          </small>
        </div>
      </v-card-text>
    </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
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
      error: '',
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'success'
    }
  },
  methods: {
    showSnackbar(text, color = 'success') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },
    async handleLogin() {
      this.error = ''
      this.loading = true

      try {
        const API_URL = process.env.VUE_APP_API_URL || 'https://nuve-sistema-production.up.railway.app/api'
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

.login-btn {
  background: linear-gradient(135deg, #FF6BD5 0%, #A855F7 50%, #EC4899 100%) !important;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.login-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #EC4899 0%, #FF6BD5 50%, #A855F7 100%) !important;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(255, 107, 213, 0.5);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
