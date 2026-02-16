# Vue.js Learning Notes

This document captures key Vue.js concepts learned while building the Project Dashboard frontend.

## Core Concepts

### 1. Single-File Components (SFC)
Vue components combine template, script, and styles in a single `.vue` file:

```vue
<template>
  <!-- HTML structure -->
</template>

<script>
export default {
  name: 'ComponentName',
  // Component logic
}
</script>

<style scoped>
/* Component-specific styles */
</style>
```

**Lessons learned:**
- `scoped` attribute keeps styles isolated to the component
- Components must have a single root element (Vue 2)
- Name property helps with debugging in Vue DevTools

### 2. Reactive Data
```javascript
data() {
  return {
    message: 'Hello',
    count: 0
  }
}
```

**Key insight:** Data must be a function returning an object (not just an object) so each component instance gets its own reactive state.

### 3. Computed Properties vs Methods
```javascript
computed: {
  // Cached, only re-evaluates when dependencies change
  fullName() {
    return `${this.firstName} ${this.lastName}`
  }
},
methods: {
  // Called every time, good for actions
  handleClick() {
    this.count++
  }
}
```

**When to use each:**
- Computed: Derived data that depends on reactive state
- Methods: Actions, event handlers, or when you need to pass arguments

### 4. Props and Events
```javascript
// Parent provides data via props
<TaskCard :task="myTask" @deleted="handleDelete" />

// Child receives and emits
props: {
  task: { type: Object, required: true }
},
methods: {
  deleteTask() {
    this.$emit('deleted')
  }
}
```

**Props down, events up:** One-way data flow keeps components predictable.

### 5. Lifecycle Hooks
```javascript
export default {
  mounted() {
    // DOM is ready, fetch data
    this.loadData()
  },
  beforeDestroy() {
    // Cleanup (event listeners, timers)
    clearInterval(this.timer)
  }
}
```

**Common hooks used:**
- `mounted`: Initial data fetching, DOM manipulation
- `beforeDestroy`: Cleanup to prevent memory leaks
- `watch`: React to specific data changes

## Vuex State Management

### Store Structure
```javascript
const store = new Vuex.Store({
  modules: {
    auth: authModule,
    projects: projectsModule,
    tasks: tasksModule
  }
})
```

### Module Pattern
```javascript
const projectsModule = {
  namespaced: true,
  state: { projects: [], loading: false },
  getters: { allProjects: state => state.projects },
  mutations: { SET_PROJECTS(state, data) { state.projects = data } },
  actions: {
    async fetchProjects({ commit }, userId) {
      const response = await api.get(`/projects/?user_id=${userId}`)
      commit('SET_PROJECTS', response.data.projects)
    }
  }
}
```

**Key patterns learned:**
- **Mutations** = Synchronous state changes (trackable in DevTools)
- **Actions** = Async operations that commit mutations
- **Getters** = Computed properties for the store
- **namespaced: true** = Prevents naming conflicts between modules

### Using Store in Components
```javascript
import { mapState, mapGetters, mapActions } from 'vuex'

computed: {
  ...mapState('projects', ['loading']),
  ...mapGetters('projects', ['allProjects'])
},
methods: {
  ...mapActions('projects', ['fetchProjects'])
}
```

## Vue Router

### Route Configuration
```javascript
const routes = [
  { path: '/', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/projects/:id', component: ProjectDetail },
  { path: '/login', component: Login }
]
```

### Navigation Guards
```javascript
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.auth.isLoggedIn
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})
```

### Route Parameters
```javascript
// In component
computed: {
  projectId() {
    return this.$route.params.id
  }
}
```

## Third-Party Libraries

### vuedraggable (v2.x)
```vue
<draggable 
  v-model="tasks" 
  group="tasks"
  @change="onDragChange"
>
  <div v-for="task in tasks" :key="task.id">
    {{ task.title }}
  </div>
</draggable>
```

**Gotchas discovered:**
- Vue 2 version (2.x) syntax differs from Vue 3 version (4.x)
- Direct DOM children required (wrap components in divs)
- `empty-insert-threshold` needed for empty list drops

### Axios for HTTP
```javascript
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' }
})
```

## CSS Patterns

### CSS Custom Properties
```css
:root {
  --bg-primary: #0d0d0f;
  --accent: #7c3aed;
  --radius-md: 12px;
}

.card {
  background: var(--bg-primary);
  border-radius: var(--radius-md);
}
```

### Transitions
```vue
<transition name="fade">
  <div v-if="show">Content</div>
</transition>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
```

## Common Mistakes Made

1. **Mutating props directly** - Always emit events to parent
2. **Forgetting `key` attribute in `v-for`** - Causes rendering bugs
3. **Not cleaning up event listeners** - Memory leaks in SPAs
4. **Using `mapState` for getters** - They're different! Use `mapGetters`
5. **Reactive arrays** - Use `splice()` or `Vue.set()`, not direct assignment

## Best Practices Adopted

1. **Component naming**: PascalCase for components, kebab-case in templates
2. **Prop validation**: Always specify type and required
3. **Computed over watch**: Prefer computed when possible
4. **Single responsibility**: Keep components focused
5. **Async/await**: Cleaner than promise chains for API calls
