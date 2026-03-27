import axios from 'axios'
import { API_BASE_URL } from './config.js'

function getCookie(name) {
  const cookieValue = document.cookie
    .split('; ')
    .find((cookie) => cookie.startsWith(`${name}=`))
  return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : ''
}

function parseErrorMessage(data) {
  if (!data) return 'Request failed'
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) {
    return data.detail.map((d) => (typeof d === 'string' ? d : d?.message || String(d))).join(' ')
  }
  if (typeof data === 'object') {
    const parts = []
    for (const [key, value] of Object.entries(data)) {
      if (key === 'detail') continue
      if (Array.isArray(value)) parts.push(`${key}: ${value.join(' ')}`)
      else if (typeof value === 'object' && value !== null) {
        parts.push(`${key}: ${JSON.stringify(value)}`)
      } else parts.push(`${key}: ${value}`)
    }
    if (parts.length) return parts.join(' ')
  }
  return 'Request failed'
}

const client = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

client.interceptors.request.use((config) => {
  const method = config.method?.toUpperCase() ?? 'GET'
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const csrfToken = getCookie('csrftoken')
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
  }
  return config
})

async function request(path, options = {}) {
  const { method = 'GET', body, data: rawData, ...axiosRest } = options
  let data = rawData
  if (body !== undefined) {
    data = typeof body === 'string' ? JSON.parse(body) : body
  }

  const m = method.toUpperCase()
  const config = {
    url: path,
    method: m,
    ...axiosRest,
  }
  if (m !== 'GET' && m !== 'HEAD' && data !== undefined) {
    config.data = data
  }

  try {
    const response = await client.request(config)
    if (response.status === 204) {
      return null
    }
    const contentType = response.headers['content-type'] ?? ''
    if (!contentType.includes('application/json')) {
      return null
    }
    return response.data
  } catch (error) {
    const payload = error.response?.data
    throw new Error(parseErrorMessage(payload))
  }
}

/** DRF page-number pagination returns `{ count, next, previous, results }`; unwrap to an array. */
function unwrapList(data) {
  if (data == null) return []
  if (Array.isArray(data)) return data
  if (Array.isArray(data.results)) return data.results
  return []
}

const httpClient = { request, unwrapList }

export default httpClient
export { unwrapList }
