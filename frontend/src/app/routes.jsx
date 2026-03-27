import { Route, Routes } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute.jsx'
import PublicRoute from './PublicRoute.jsx'
import AppLayout from '../shared/layouts/AppLayout.jsx'
import DashboardPage from '../pages/DashboardPage.jsx'
import FarmsPage from '../pages/FarmsPage.jsx'
import FieldsPage from '../pages/FieldsPage.jsx'
import LandingPage from '../pages/LandingPage.jsx'
import LoginPage from '../pages/LoginPage.jsx'
import RegisterPage from '../pages/RegisterPage.jsx'
import NotFoundPage from '../pages/NotFoundPage.jsx'
import RecommendationsPage from '../pages/RecommendationsPage.jsx'
import RecommendationDetailPage from '../pages/RecommendationDetailPage.jsx'
import SoilPage from '../pages/SoilPage.jsx'
import WeatherPage from '../pages/WeatherPage.jsx'
import ChatPage from '../pages/ChatPage.jsx'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route
        path="/login"
        element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicRoute>
            <RegisterPage />
          </PublicRoute>
        }
      />

      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/farms" element={<FarmsPage />} />
        <Route path="/fields" element={<FieldsPage />} />
        <Route path="/soil" element={<SoilPage />} />
        <Route path="/weather" element={<WeatherPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/recommendations/:id" element={<RecommendationDetailPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default AppRoutes
