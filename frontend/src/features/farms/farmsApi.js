import httpClient, { unwrapList } from '../../api/httpClient.js'

function fetchFarms() {
  return httpClient.request('/api/v1/farms/').then(unwrapList)
}

function createFarm(payload) {
  return httpClient.request('/api/v1/farms/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

function updateFarm(id, payload) {
  return httpClient.request(`/api/v1/farms/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

function deleteFarm(id) {
  return httpClient.request(`/api/v1/farms/${id}/`, {
    method: 'DELETE',
  })
}

function fetchFields(params = {}) {
  const q = new URLSearchParams(params).toString()
  const suffix = q ? `?${q}` : ''
  return httpClient.request(`/api/v1/fields/${suffix}`).then(unwrapList)
}

function createField(payload) {
  return httpClient.request('/api/v1/fields/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

function updateField(id, payload) {
  return httpClient.request(`/api/v1/fields/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

function deleteField(id) {
  return httpClient.request(`/api/v1/fields/${id}/`, {
    method: 'DELETE',
  })
}

export {
  createFarm,
  createField,
  deleteFarm,
  deleteField,
  fetchFarms,
  fetchFields,
  updateFarm,
  updateField,
}
