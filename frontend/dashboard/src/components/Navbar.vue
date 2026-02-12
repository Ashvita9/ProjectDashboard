<template>
  <nav class="nav">
    <div class="nav-inner">
      <router-link to="/dashboard" class="nav-brand">
        <span class="brand-icon">◆</span>
        <span class="brand-text">Dashboard</span>
      </router-link>

      <div v-if="isAuthenticated" class="nav-links">
        <router-link to="/dashboard" exact-active-class="is-active">
          Overview
        </router-link>
        <router-link to="/projects" active-class="is-active">
          Projects
        </router-link>
      </div>

      <div v-if="isAuthenticated" class="nav-right">
        <div class="user-pill">
          <span class="avatar">{{ user?.username?.charAt(0)?.toUpperCase() }}</span>
          <span class="username">{{ user?.username }}</span>
        </div>
        <button class="btn-ghost" @click="handleLogout">Sign out</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'NavBar',
  computed: {
    ...mapState('auth', ['user', 'isAuthenticated'])
  },
  methods: {
    handleLogout() {
      this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 10, 15, 0.8);
  backdrop-filter: blur(16px) saturate(180%);
  border-bottom: 1px solid var(--border);
}

.nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 700;
  font-size: 15px;
  letter-spacing: -0.02em;
  flex-shrink: 0;
}

.brand-icon {
  color: var(--accent);
  font-size: 18px;
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-links a {
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.15s var(--ease);
}

.nav-links a:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.nav-links a.is-active {
  color: var(--text-primary);
  background: var(--bg-elevated);
}

.nav-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px 4px 4px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
}

.avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.username {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.btn-ghost {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  transition: all 0.15s var(--ease);
  box-shadow: none;
}

.btn-ghost:hover {
  color: var(--color-danger);
  background: var(--color-danger-muted);
  box-shadow: none;
}

@media (max-width: 640px) {
  .nav-inner {
    padding: 0 16px;
    gap: 16px;
  }

  .brand-text {
    display: none;
  }

  .username {
    display: none;
  }
}
</style>
