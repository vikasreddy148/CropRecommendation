import httpClient, { unwrapList } from '../../api/httpClient.js'

function fetchRecommendations() {
  return httpClient.request('/api/v1/recommendations/').then(unwrapList)
}

function fetchRecommendationById(id) {
  return httpClient.request(`/api/v1/recommendations/${id}/`)
}

function requestRecommendations(payload) {
  return httpClient.request('/api/v1/recommendations/request/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

function requestRecommendationsForField(fieldId) {
  return httpClient.request(`/api/v1/recommendations/field/${fieldId}/`, {
    method: 'POST',
  })
}

export {
  fetchRecommendationById,
  fetchRecommendations,
  requestRecommendations,
  requestRecommendationsForField,
}
