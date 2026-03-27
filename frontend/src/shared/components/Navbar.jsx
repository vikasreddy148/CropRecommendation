import { Link } from 'react-router-dom'
import BrandLogo from './BrandLogo.jsx'
import Button from './Button.jsx'

function Navbar({ user, onLogout }) {
  return (
    <header className="sticky top-0 z-30 flex h-14 shrink-0 items-center justify-between gap-3 border-b border-stone-200/80 bg-white/90 px-4 backdrop-blur-md lg:px-6">
      <Link to="/dashboard" className="min-w-0 lg:hidden">
        <BrandLogo compact />
      </Link>
      <div className="hidden flex-1 lg:block" aria-hidden />
      <div className="flex items-center gap-2 sm:gap-3">
        <span
          className="hidden max-w-[160px] truncate text-sm font-medium text-stone-600 sm:inline"
          title={user?.username}
        >
          {user?.username}
        </span>
        <Button type="button" variant="secondary" size="sm" onClick={onLogout}>
          Sign out
        </Button>
      </div>
    </header>
  )
}

export default Navbar
