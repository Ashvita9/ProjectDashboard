import { projectService } from '@/services/project'

const state = {
  projects: [],
  activeProject: null,
  loading: false,
  error: null
}

const getters = {
  projectCount: state => state.projects.length,
  getProjectById: state => id => state.projects.find(p => p.id === id),
  allProjects: state => state.projects,
  activeProject: state => state.activeProject,
  isLoading: state => state.loading
}

const mutations = {
  SET_PROJECTS(state, projects) {
    state.projects = projects
  },
  CLEAR_PROJECTS(state) {
    state.projects = []
    state.activeProject = null
  },
  ADD_PROJECT(state, project) {
    state.projects.push(project)
  },
  UPDATE_PROJECT(state, updatedProject) {
    const index = state.projects.findIndex(p => p.id === updatedProject.id)
    if (index !== -1) {
      state.projects.splice(index, 1, updatedProject)
    }
  },
  DELETE_PROJECT(state, projectId) {
    state.projects = state.projects.filter(p => p.id !== projectId)
  },
  SET_ACTIVE_PROJECT(state, project) {
    state.activeProject = project
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  }
}

const actions = {
  async fetchProjects({ commit }, userId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await projectService.fetchProjects(userId)
      commit('SET_PROJECTS', response.data.result || [])
      return response.data.result
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to fetch projects'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createProject({ commit }, { name, description }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await projectService.createProject(name, description)
      const newProject = response.data.project
      commit('ADD_PROJECT', newProject)
      return newProject
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to create project'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateProject({ commit }, { projectId, name, description }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const response = await projectService.updateProject(projectId, name, description)
      const updatedProject = response.data.project
      commit('UPDATE_PROJECT', updatedProject)
      if (commit._vm.$store.state.projects.activeProject?.id === projectId) {
        commit('SET_ACTIVE_PROJECT', updatedProject)
      }
      return updatedProject
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to update project'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async deleteProject({ commit }, projectId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      await projectService.deleteProject(projectId)
      commit('DELETE_PROJECT', projectId)
      return true
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to delete project'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  setActiveProject({ commit }, project) {
    commit('SET_ACTIVE_PROJECT', project)
  },

  clearProjects({ commit }) {
    commit('CLEAR_PROJECTS')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
