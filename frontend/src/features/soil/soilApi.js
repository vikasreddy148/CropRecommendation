import httpClient, { unwrapList } from '../../api/httpClient.js'

function fetchSoilData() {
  return httpClient.request('/api/v1/soil/').then(unwrapList)
}

function createSoilData(payload) {
  return httpClient.request('/api/v1/soil/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

function fetchSoilFromSource(payload) {
  return httpClient.request('/api/v1/soil/fetch/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export { createSoilData, fetchSoilData, fetchSoilFromSource }
