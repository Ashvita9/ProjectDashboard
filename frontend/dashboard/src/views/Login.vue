<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <div class="auth-card">
        <div class="auth-card-header">
          <span class="brand-icon">◆</span>
          <h1>Sign in</h1>
          <p>Enter your credentials to access your dashboard.</p>
        </div>

        <div v-if="errors.length" class="alert alert-error">
          <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username or Email</label>
            <input id="username" v-model="form.username" type="text" required placeholder="you@example.com" />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input id="password" v-model="form.password" type="password" required placeholder="••••••••" />
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            {{ isLoading ? 'Signing in…' : 'Sign in' }}
          </button>
        </form>

        <p class="auth-switch">
          Don't have an account?
          <router-link to="/register">Create one</router-link>
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
      form: { username: '', password: '' },
      isLoading: false,
      errors: []
    }
  },
  methods: {
    async handleLogin() {
      this.errors = []
      this.isLoading = true
      try {
        const response = await authService.login(this.form.username, this.form.password)
        const user = response.data.user
        this.$store.dispatch('auth/setAuth', { user, token: user.id })
        this.$router.push('/dashboard')
      } catch (error) {
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
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  padding: 24px;
  position: relative;
  overflow: hidden;
}

/* Decorative glow */
.auth-page::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124, 92, 252, 0.12), transparent 70%);
  top: -100px;
  right: -100px;
  pointer-events: none;
}

.auth-wrapper {
  width: 100%;
  max-width: 400px;
}

.auth-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px;
}

.auth-card-header {
  text-align: center;
  margin-bottom: 28px;
}

.brand-icon {
  color: var(--accent);
  font-size: 28px;
  display: block;
  margin-bottom: 16px;
}

.auth-card-header h1 {
  font-size: 22px;
  margin-bottom: 8px;
}

.auth-card-header p {
  color: var(--text-secondary);
  font-size: 14px;
}

.btn-block {
  width: 100%;
  margin-top: 4px;
}

.auth-switch {
  text-align: center;
  margin-top: 24px;
  font-size: 13px;
  color: var(--text-secondary);
}

.auth-switch a {
  color: var(--accent-light);
  font-weight: 600;
}

.auth-switch a:hover {
  text-decoration: underline;
}
</style>
