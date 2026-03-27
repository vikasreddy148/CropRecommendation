import { Outlet, useNavigate } from 'react-router-dom'
import useAuth from '../../app/useAuth.js'
import MobileBottomNav from '../components/MobileBottomNav.jsx'
import Navbar from '../components/Navbar.jsx'
import Sidebar from '../components/Sidebar.jsx'

function AppLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    try {
      await logout()
      navigate('/login', { replace: true })
    } catch {
      navigate('/login', { replace: true })
    }
  }

  return (
    <div className="flex min-h-screen bg-surface-muted grain">
      <Sidebar />
      <div className="flex min-h-screen flex-1 flex-col lg:min-h-0">
        <Navbar user={user} onLogout={handleLogout} />
        <div className="flex-1 overflow-auto pb-[calc(4.25rem+env(safe-area-inset-bottom,0px))] lg:pb-6">
          <div className="mx-auto max-w-6xl px-4 py-5 md:px-6 md:py-8">
            <Outlet />
          </div>
        </div>
      </div>
      <MobileBottomNav />
    </div>
  )
}

export default AppLayout
