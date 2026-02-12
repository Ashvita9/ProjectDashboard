import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add user_id from localStorage
apiClient.interceptors.request.use(
  config => {
    const userId = localStorage.getItem('user_id')
    // Only add user_id if it exists AND we're not on login/register endpoints
    const isAuthEndpoint = config.url?.includes('/auth/login') || config.url?.includes('/auth/register')
    
    if (userId && config.data && !isAuthEndpoint) {
      config.data.user_id = userId
    }
    // Add header so server can trust the user id rather than body data
    if (userId && !isAuthEndpoint) {
      config.headers = config.headers || {}
      config.headers['X-User-Id'] = userId
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    // Don't redirect on login/register errors - let the component handle them
    const isAuthEndpoint = error.config?.url?.includes('/auth/login') || error.config?.url?.includes('/auth/register')
    
    if (error.response && error.response.status === 401 && !isAuthEndpoint) {
      // Only auto-redirect if NOT on login/register pages
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
