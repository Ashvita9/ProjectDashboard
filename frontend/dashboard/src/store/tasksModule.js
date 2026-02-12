import { taskService } from '@/services/task'

const state = {
  tasks: [],
  tasksByProject: {},
  loading: false,
  error: null,
  unsavedChanges: false
}

const getters = {
  tasksByProjectId: state => projectId => state.tasksByProject[projectId] || [],
  allTasks: state => state.tasks,
  completedTaskCount: state => state.tasks.filter(t => t.status === 'done').length,
  tasksGroupedByStatus: state => {
    return {
      todo: state.tasks.filter(t => t.status === 'todo'),
      in_progress: state.tasks.filter(t => t.status === 'in_progress'),
      done: state.tasks.filter(t => t.status === 'done')
    }
  },
  isLoading: state => state.loading,
  hasUnsavedChanges: state => state.unsavedChanges
}

const mutations = {
  SET_TASKS(state, tasks) {
    state.tasks = tasks
  },
  CLEAR_TASKS(state) {
    state.tasks = []
    state.tasksByProject = {}
  },
  SET_TASKS_BY_PROJECT(state, { projectId, tasks }) {
    state.tasksByProject = {
      ...state.tasksByProject,
      [projectId]: tasks
    }
  },
  ADD_TASK(state, task) {
    state.tasks.push(task)
    if (!state.tasksByProject[task.project]) {
      state.tasksByProject[task.project] = []
    }
    state.tasksByProject[task.project].push(task)
  },
  UPDATE_TASK(state, updatedTask) {
    const index = state.tasks.findIndex(t => t.id === updatedTask.id)
    if (index !== -1) {
      state.tasks.splice(index, 1, updatedTask)
    }
    
    const projectId = updatedTask.project
    if (state.tasksByProject[projectId]) {
      const projectIndex = state.tasksByProject[projectId].findIndex(t => t.id === updatedTask.id)
      if (projectIndex !== -1) {
        state.tasksByProject[projectId].splice(projectIndex, 1, updatedTask)
      }
    }
  },
  DELETE_TASK(state, taskId) {
    state.tasks = state.tasks.filter(t => t.id !== taskId)
    for (let projectId in state.tasksByProject) {
      state.tasksByProject[projectId] = state.tasksByProject[projectId].filter(t => t.id !== taskId)
    }
  },
  SET_LOADING(state, loading) {
    state.loading = loading
  },
  SET_ERROR(state, error) {
    state.error = error
  },
  SET_UNSAVED_CHANGES(state, hasChanges) {
    state.unsavedChanges = hasChanges
  }
}

const actions = {
  async fetchTasksByProject({ commit, rootState }, projectId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      // include current user id so backend enforces project ownership checks
      const userId = rootState?.auth?.userId
      const response = await taskService.fetchTasksByProject(projectId, userId)
      const tasks = response.data.tasks || response.data.result || []
      commit('SET_TASKS_BY_PROJECT', { projectId, tasks })
      return tasks
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to fetch tasks'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async createTask({ commit, rootState }, { projectId, title, description, status }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const userId = rootState?.auth?.userId
      const response = await taskService.createTask(projectId, title, description, status, userId)
      const newTask = response.data.task
      commit('ADD_TASK', newTask)
      return newTask
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to create task'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async updateTask({ commit, rootState }, { taskId, title, description, status }) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const userId = rootState?.auth?.userId
      const response = await taskService.updateTask(taskId, title, description, status, userId)
      const updatedTask = response.data.task
      commit('UPDATE_TASK', updatedTask)
      return updatedTask
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to update task'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  async deleteTask({ commit, rootState }, taskId) {
    commit('SET_LOADING', true)
    commit('SET_ERROR', null)
    try {
      const userId = rootState?.auth?.userId
      await taskService.deleteTask(taskId, userId)
      commit('DELETE_TASK', taskId)
      return true
    } catch (error) {
      const errorMsg = error.response?.data?.message || 'Failed to delete task'
      commit('SET_ERROR', errorMsg)
      throw error
    } finally {
      commit('SET_LOADING', false)
    }
  },

  setUnsavedChanges({ commit }, hasChanges) {
    commit('SET_UNSAVED_CHANGES', hasChanges)
  },

  clearTasks({ commit }) {
    commit('CLEAR_TASKS')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
