import httpClient from '../../api/httpClient.js'

async function ensureCsrfToken() {
  return httpClient.request('/api/v1/auth/csrf/')
}

async function loginWithSession({ username, password }) {
  if (!username || !password) {
    throw new Error('Username and password are required.')
  }

  await ensureCsrfToken()
  return httpClient.request('/api/v1/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}

async function registerUser(payload) {
  await ensureCsrfToken()
  return httpClient.request('/api/v1/auth/register/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

async function fetchCurrentUser() {
  return httpClient.request('/api/v1/auth/me/')
}

async function logoutSession() {
  return httpClient.request('/api/v1/auth/logout/', {
    method: 'POST',
  })
}

export { fetchCurrentUser, loginWithSession, logoutSession, registerUser }
