<template>
  <div class="auth-container">
    <div class="auth-card card">
      <div class="card-header">
        <h1 class="card-title">Register</h1>
      </div>
      
      <div v-if="errors.length" class="alert alert-error mb-20">
        <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="Choose a username"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="Enter your email"
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

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            placeholder="Confirm password"
          />
        </div>

        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          {{ isLoading ? 'Registering...' : 'Register' }}
        </button>
      </form>

      <p class="text-center mt-20">
        Already have an account?
        <router-link to="/login" class="link">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services/auth'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      isLoading: false,
      errors: []
    }
  },
  methods: {
    async handleRegister() {
      this.errors = []

      if (this.form.password !== this.form.confirmPassword) {
        this.errors.push('Passwords do not match')
        return
      }

      this.isLoading = true

      try {
        const response = await authService.register(
          this.form.username,
          this.form.email,
          this.form.password,
          this.form.confirmPassword
        )

        if (response.status === 201) {
          this.$router.push('/login')
        }
      } catch (error) {
        const errorMsg = error.response?.data?.message || 'Registration failed'
        this.errors.push(errorMsg)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--clay-primary) 0%, var(--clay-secondary) 100%);
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 450px;
}

.link {
  color: var(--clay-primary);
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}
</style>
