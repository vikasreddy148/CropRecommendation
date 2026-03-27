import { Navigate } from 'react-router-dom'
import useAuth from './useAuth.js'
import Loader from '../shared/components/Loader.jsx'

function PublicRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-muted">
        <Loader label="Checking your session…" />
      </div>
    )
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />
  }

  return children
}

export default PublicRoute
