import httpClient from '../../api/httpClient.js'

async function fetchDashboardSummary() {
  return httpClient.request('/api/v1/dashboard/')
}

export { fetchDashboardSummary }
