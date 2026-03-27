import { Link } from 'react-router-dom'
import BrandLogo from '../shared/components/BrandLogo.jsx'
import Card from '../shared/components/Card.jsx'

function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-primary-50/50 via-surface-muted to-white px-4 py-12">
      <div className="mb-8">
        <BrandLogo />
      </div>
      <Card className="w-full max-w-md text-center shadow-lift">
        <p className="text-xs font-semibold uppercase tracking-widest text-primary-800">404</p>
        <h1 className="mt-3 font-display text-2xl font-semibold text-stone-900">Page not found</h1>
        <p className="mt-2 text-sm leading-relaxed text-stone-600">
          The link may be broken or the page was moved. Pick a destination below.
        </p>
        <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">
          <Link
            to="/"
            className="inline-flex min-h-11 items-center justify-center rounded-xl border border-stone-200 bg-white px-4 py-2.5 text-sm font-semibold text-stone-800 shadow-sm hover:bg-stone-50"
          >
            Home
          </Link>
          <Link
            to="/dashboard"
            className="inline-flex min-h-11 items-center justify-center rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white shadow-soft hover:bg-primary-700"
          >
            Dashboard
          </Link>
        </div>
      </Card>
    </div>
  )
}

export default NotFoundPage
