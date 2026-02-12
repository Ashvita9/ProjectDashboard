import apiClient from './api'

export const authService = {
  register(username, email, password, confirmPassword) {
    return apiClient.post('/auth/register/', {
      username,
      email,
      password,
      confirm_password: confirmPassword
    })
  },

  login(usernameOrEmail, password) {
    // Detect if input is email (contains @) and send in correct field
    const isEmail = usernameOrEmail && usernameOrEmail.includes('@')
    const loginData = {
      password
    }
    
    if (isEmail) {
      loginData.email = usernameOrEmail
    } else {
      loginData.username = usernameOrEmail
    }
    
    return apiClient.post('/auth/login/', loginData)
  },

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('user_id')
  }
}
