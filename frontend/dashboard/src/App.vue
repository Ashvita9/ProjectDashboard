<template>
  <div id="app">
    <NavBar v-if="isAuthenticated" />
    <NotificationCenter />
    <router-view />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import NavBar from '@/components/Navbar.vue'
import NotificationCenter from '@/components/NotificationCenter.vue'

export default {
  name: 'App',
  components: { NavBar, NotificationCenter },
  computed: {
    ...mapState('auth', ['isAuthenticated'])
  }
}
</script>

<style>
@import '@/styles/clay-theme.css';

#app {
  min-height: 100vh;
  background-color: var(--bg-primary);
}
</style>
