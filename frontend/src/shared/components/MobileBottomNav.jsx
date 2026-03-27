import { NavLink } from 'react-router-dom'
import { NAV_ITEMS } from '../navConfig.js'
import { NavIcon } from './NavIcons.jsx'

function MobileBottomNav() {
  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-40 border-t border-stone-200/90 bg-white/95 pb-[env(safe-area-inset-bottom,0px)] shadow-[0_-4px_24px_-8px_rgba(0,0,0,0.08)] backdrop-blur-md lg:hidden"
      aria-label="Primary"
    >
      <div className="scrollbar-none flex h-[4.25rem] snap-x snap-mandatory items-stretch gap-0 overflow-x-auto px-1">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex min-w-[4.25rem] max-w-[5.5rem] flex-1 snap-center flex-col items-center justify-center gap-0.5 px-1 py-2 text-[10px] font-semibold leading-tight transition ${
                isActive ? 'text-primary-800' : 'text-stone-500'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span
                  className={`flex h-9 w-9 items-center justify-center rounded-xl transition ${
                    isActive ? 'bg-primary-100 text-primary-800 shadow-sm' : 'text-stone-500'
                  }`}
                >
                  <NavIcon to={item.to} className="h-5 w-5" />
                </span>
                <span className="line-clamp-2 text-center">{item.short}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  )
}

export default MobileBottomNav
