<template>
  <nav class="navbar">
    <router-link to="/dashboard" class="navbar-brand">
      📊 Project Dashboard
    </router-link>

    <ul v-if="isAuthenticated" class="navbar-nav">
      <li>
        <router-link to="/dashboard" exact-active-class="active">
          Dashboard
        </router-link>
      </li>
      <li>
        <router-link to="/projects" active-class="active">
          Projects
        </router-link>
      </li>
      <li>
        <span class="separator">|</span>
      </li>
      <li class="user-menu">
        <span class="user-name">{{ user?.username }}</span>
        <button class="logout-btn" @click="handleLogout">Logout</button>
      </li>
    </ul>
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
.navbar {
  background-color: var(--clay-primary);
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px var(--clay-shadow-dark);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-brand {
  font-size: 24px;
  font-weight: 700;
  text-decoration: none;
  color: white;
  transition: opacity 0.3s ease;
}

.navbar-brand:hover {
  opacity: 0.8;
}

.navbar-nav {
  display: flex;
  gap: 25px;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: center;
}

.navbar-nav a {
  color: white;
  text-decoration: none;
  transition: color 0.3s ease;
  font-weight: 500;
}

.navbar-nav a:hover {
  color: var(--clay-secondary-light);
}

.navbar-nav a.active {
  color: var(--clay-secondary-light);
  border-bottom: 2px solid var(--clay-secondary-light);
  padding-bottom: 8px;
}

.separator {
  opacity: 0.5;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-left: 10px;
}

.user-name {
  font-weight: 600;
}

.logout-btn {
  background-color: var(--clay-secondary);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: var(--clay-secondary-dark);
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 15px;
    padding: 15px;
  }

  .navbar-nav {
    width: 100%;
    justify-content: center;
    gap: 15px;
  }
}
</style>
