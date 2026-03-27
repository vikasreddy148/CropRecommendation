import httpClient, { unwrapList } from '../../api/httpClient.js'

function fetchWeatherData() {
  return httpClient.request('/api/v1/weather/').then(unwrapList)
}

function createWeatherData(payload) {
  return httpClient.request('/api/v1/weather/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

function fetchWeatherFromField(payload) {
  return httpClient.request('/api/v1/weather/fetch/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export { createWeatherData, fetchWeatherData, fetchWeatherFromField }
