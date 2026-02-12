<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <div class="auth-card">
        <div class="auth-card-header">
          <span class="brand-icon">◆</span>
          <h1>Create account</h1>
          <p>Join to start managing your projects.</p>
        </div>

        <div v-if="errors.length" class="alert alert-error">
          <div v-for="(error, index) in errors" :key="index">{{ error }}</div>
        </div>

        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="username">Username</label>
            <input id="username" v-model="form.username" type="text" required placeholder="Choose a username" />
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input id="email" v-model="form.email" type="email" required placeholder="you@example.com" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="password">Password</label>
              <input id="password" v-model="form.password" type="password" required placeholder="••••••••" />
            </div>
            <div class="form-group">
              <label for="confirmPassword">Confirm</label>
              <input id="confirmPassword" v-model="form.confirmPassword" type="password" required
                placeholder="••••••••" />
            </div>
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="isLoading">
            {{ isLoading ? 'Creating…' : 'Create account' }}
          </button>
        </form>

        <p class="auth-switch">
          Already have an account?
          <router-link to="/login">Sign in</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services/auth'

export default {
  name: 'Register',
  data() {
    return {
      form: { username: '', email: '', password: '', confirmPassword: '' },
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
          this.form.username, this.form.email,
          this.form.password, this.form.confirmPassword
        )
        if (response.status === 201) this.$router.push('/login')
      } catch (error) {
        this.errors.push(error.response?.data?.message || 'Registration failed')
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

.auth-page::before {
  content: '';
  position: absolute;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124, 92, 252, 0.12), transparent 70%);
  bottom: -100px;
  left: -100px;
  pointer-events: none;
}

.auth-wrapper {
  width: 100%;
  max-width: 440px;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
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
