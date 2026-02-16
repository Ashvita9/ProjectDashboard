# Project Dashboard Frontend — Documentation Handbook

This README explains the frontend code for the Project Dashboard (Vue.js 2.x) in a very simple and clear way—like explaining to a beginner. It shows where things live, what each file does, and includes short code snippets for important pieces.

## Quick summary
- Where: frontend/dashboard/ — this is the Vue.js application folder.
- Tech: Vue 2.7.x, Vuex, Vue Router, Axios.
- Purpose: UI for viewing projects, tasks, logging in, and interacting with the backend API.

## How to run (developer)
1. Install dependencies: `npm install` inside `frontend/dashboard`.
2. Start dev server: `npm run serve`.
3. Build for production: `npm run build`.

## Top-level files and what they do
- `package.json` — declares scripts and dependencies. Use it to run or build the frontend.
- `babel.config.js` / `vue.config.js` — build and bundler configuration.
- `public/index.html` — main HTML template that mounts the Vue app.
- `src/main.js` — app entry point. It creates the Vue instance and hooks up router and store.

### `src/main.js` (what it handles)
- Bootstraps the Vue app, sets up global plugins and the root component `App.vue`.

Minimal snippet:
```js
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
```

Explanation for a child: `main.js` is like waking up the whole app — it tells Vue where to start and which helpers (router, store) to use.

## `src/router/index.js` — navigation
- Handles URL routes (which page to show for which address), and route guards (checks if user is logged-in before entering certain pages).

Simple idea:
```js
const routes = [
  { path: '/', component: Dashboard },
  { path: '/login', component: Login }
]

const router = new VueRouter({ routes })

// navigation guard example
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth
  if (requiresAuth && !store.getters.isLoggedIn) next('/login')
  else next()
})
```

Explanation for a child: Router listens to the address bar and shows the right page. Before some pages, it asks: "Is the user allowed?"

## `src/store` — Vuex store (global state)
- `index.js` — registers modules.
- `authModule.js` — holds user token, login/logout actions.
- `projectsModule.js` — holds list of projects, actions to fetch or update projects.
- `tasksModule.js` — holds tasks and task operations.

Example `authModule` responsibilities:
- State: `token`, `user`
- Actions: `login`, `logout`, `fetchProfile`
- Mutations: `SET_TOKEN`, `SET_USER`

Short snippet:
```js
// in an action
async login({ commit }, credentials) {
  const res = await api.login(credentials)
  commit('SET_TOKEN', res.token)
}
```

Explanation for a child: The store is a central box holding the app's important data. Components read from and write to this box using actions and mutations.

## `src/services` (API helpers)
- `api.js` — central axios instance and small helpers for requests.
- `auth.js`, `project.js`, `task.js` — functions that call endpoints (login, fetch projects, create task, etc.).

Example `services/api.js`:
```js
import axios from 'axios'

const api = axios.create({ baseURL: process.env.VUE_APP_API_URL })

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default api
```

Explanation for a child: `api.js` is the phone the app uses to call the backend. It adds the user's token to each call so the backend knows who is talking.

## `src/components` and `src/views`
- `components/` — small reusable UI pieces (cards, buttons, forms).
- `views/` — page-level components that map to routes (Dashboard, Projects, Login, Register, ProjectDetail).

Tip: If you change a view (e.g., `ProjectDetail.vue`), check the router to see how it's reached and the store to see what data it needs.

## `src/App.vue` — root component
- Controls app-wide behaviors: top-level layout, global event bus usage, socket initialization if present, global modals.

Simple explanation: `App.vue` is the outer shell — it shows header, footer and the current page inside.

## Important development notes
- Follow naming: `PascalCase.vue` for components, `camelCase` for JS files.
- Keep API calls in `services/` and state updates in `store/` to keep components simple and focused on UI.

## Files-to-purpose quick map (child-friendly)
- `src/main.js`: starts the app.
- `src/App.vue`: the app frame.
- `src/router/index.js`: which page for which address.
- `src/store/*`: global data box (auth, projects, tasks).
- `src/services/*`: calls to backend.
- `src/views/*`: actual pages like Dashboard and Login.
- `src/components/*`: building blocks for pages.

## Where to add a new feature (step-by-step)
1. Add UI in `src/components` or `src/views`.
2. If data is needed globally, add state/actions to the appropriate `store` module.
3. Create API functions in `src/services/*`.
4. Wire everything in the view: call action, display store state.

## Troubleshooting
- If API calls fail, open browser developer tools network tab and check request URL and Authorization header.
- If route doesn't show, ensure `router/index.js` has an entry for that path.

---
This README gives a friendly tour for frontend contributors. For any file not described here, open it and look for `export default` (Vue components) or `export` (JS helpers) to see what it provides.
# dashboard

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
