import { NavLink } from 'react-router-dom'
import { NAV_SECTIONS } from '../navConfig.js'
import BrandLogo from './BrandLogo.jsx'
import { NavIcon } from './NavIcons.jsx'

function Sidebar() {
  return (
    <aside className="hidden w-60 shrink-0 flex-col border-r border-stone-200/80 bg-white lg:flex">
      <div className="flex h-14 items-center border-b border-stone-100 px-4">
        <BrandLogo />
      </div>
      <nav className="flex flex-1 flex-col gap-6 overflow-y-auto p-3" aria-label="Main">
        {NAV_SECTIONS.map((section) => (
          <div key={section.title ?? 'main'}>
            {section.title ? (
              <p className="mb-2 px-3 text-[11px] font-semibold uppercase tracking-wider text-stone-400">
                {section.title}
              </p>
            ) : null}
            <div className="flex flex-col gap-0.5">
              {section.items.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold transition ${
                      isActive
                        ? 'bg-primary-50 text-primary-900 shadow-sm ring-1 ring-primary-100/80'
                        : 'text-stone-600 hover:bg-stone-50 hover:text-stone-900'
                    }`
                  }
                  end={item.to === '/dashboard'}
                >
                  <NavIcon to={item.to} className="h-5 w-5 shrink-0 text-current opacity-90" />
                  {item.label}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
