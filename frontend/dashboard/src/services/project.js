import apiClient from './api'

export const projectService = {
  fetchProjects(userId) {
    // Send user_id both as query param and body for compatibility
    const params = {}
    const data = {}
    if (userId) {
      params.user_id = userId
      data.user_id = userId
    }
    return apiClient.request({
      method: 'GET',
      url: '/projects/',
      params,
      data
    })
  },

  fetchAllProjects() {
    return apiClient.get('/projects/')
  },

  createProject(name, description = '') {
    return apiClient.post('/projects/', {
      name,
      description
    })
  },

  updateProject(projectId, name, description = '') {
    return apiClient.put('/projects/', {
      project_id: projectId,
      name,
      description
    })
  },

  partialUpdateProject(projectId, data) {
    return apiClient.patch('/projects/', {
      project_id: projectId,
      ...data
    })
  },

  deleteProject(projectId) {
    return apiClient.delete('/projects/', {
      data: {
        project_id: projectId
      }
    })
  }
}
