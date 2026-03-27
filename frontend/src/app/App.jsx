import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './AuthContext.jsx'
import AppRoutes from './routes.jsx'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
