import apiClient from './api'

export const taskService = {
  fetchTasksByProject(projectId, userId = null) {
    // Send id filters both as query params and body for compatibility
    const params = { project_id: projectId }
    const data = { project_id: projectId }
    if (userId) {
      params.user_id = userId
      data.user_id = userId
    }
    return apiClient.request({
      method: 'GET',
      url: '/tasks/',
      params,
      data
    })
  },

  fetchTasksByUser(userId) {
    return apiClient.request({
      method: 'GET',
      url: '/tasks/',
      params: { user_id: userId },
      data: { user_id: userId }
    })
  },

  fetchAllTasks() {
    return apiClient.get('/tasks/')
  },

  createTask(projectId, title, description = '', status = 'todo', userId = null) {
    const data = {
      project_id: projectId,
      title,
      description,
      status
    }
    if (userId) data.user_id = userId
    return apiClient.post('/tasks/', data)
  },

  updateTask(taskId, title, description = '', status = 'todo', userId = null) {
    const data = {
      task_id: taskId,
      title,
      description,
      status
    }
    if (userId) data.user_id = userId
    return apiClient.put('/tasks/', data)
  },

  partialUpdateTask(taskId, data) {
    return apiClient.patch('/tasks/', {
      task_id: taskId,
      ...data
    })
  },

  deleteTask(taskId, userId = null) {
    const data = { task_id: taskId }
    if (userId) data.user_id = userId
    return apiClient.delete('/tasks/', { data })
  }
}
