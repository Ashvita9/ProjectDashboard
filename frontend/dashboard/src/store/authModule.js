const state = {
  token: localStorage.getItem('token') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  userId: localStorage.getItem('user_id') || null,
  isAuthenticated: !!localStorage.getItem('token')
}

const getters = {
  isAuthenticated: state => state.isAuthenticated,
  user: state => state.user,
  userId: state => state.userId,
  token: state => state.token
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  },
  SET_USER(state, user) {
    state.user = user
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
      state.userId = user.id
      localStorage.setItem('user_id', user.id)
      state.isAuthenticated = true
    } else {
      localStorage.removeItem('user')
      localStorage.removeItem('user_id')
      state.userId = null
      state.isAuthenticated = false
    }
  },
  LOGOUT(state) {
    state.token = null
    state.user = null
    state.userId = null
    state.isAuthenticated = false
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('user_id')
  }
}

const actions = {
  setAuth({ commit, dispatch }, { user, token }) {
    // Clear old data from previous user
    dispatch('projects/clearProjects', null, { root: true })
    dispatch('tasks/clearTasks', null, { root: true })
    
    commit('SET_TOKEN', token || user.id)
    commit('SET_USER', user)
  },
  logout({ commit, dispatch }) {
    // Clear all user data
    dispatch('projects/clearProjects', null, { root: true })
    dispatch('tasks/clearTasks', null, { root: true })
    
    commit('LOGOUT')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
