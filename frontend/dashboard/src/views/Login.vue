<template>
  <div class="login-page">
    <div class="auth-container">
      <div class="auth-card card">
        <div class="card-header">
          <h1 class="card-title">Login</h1>
        </div>
        
        <div v-if="errors.length" class="alert alert-error mb-20">
          <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username or Email</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              placeholder="Enter username or email"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              placeholder="Enter password"
            />
          </div>

          <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
            {{ isLoading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <p class="text-center mt-20">
          Don't have an account?
          <router-link to="/register" class="link">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services/auth'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      isLoading: false,
      errors: []
    }
  },
  methods: {
    async handleLogin() {
      this.errors = []
      this.isLoading = true

      try {
        console.log('Attempting login with username:', this.form.username)
        const response = await authService.login(this.form.username, this.form.password)
        console.log('Login response:', response.data)
        const user = response.data.user
        
        this.$store.dispatch('auth/setAuth', {
          user,
          token: user.id
        })

        this.$router.push('/dashboard')
      } catch (error) {
        console.error('Login error:', error)
        console.error('Error response:', error.response)
        const errorMsg = error.response?.data?.message || 'Login failed. Please check your credentials.'
        this.errors.push(errorMsg)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--clay-primary) 0%, var(--clay-secondary) 100%);
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 400px;
}

.auth-card {
  width: 100%;
}

.link {
  color: var(--clay-primary);
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

.w-100 {
  width: 100%;
}
</style>
