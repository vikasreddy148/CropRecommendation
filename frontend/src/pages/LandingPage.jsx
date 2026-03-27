import { Link } from 'react-router-dom'
import useAuth from '../app/useAuth.js'
import heroImage from '../assets/hero.png'
import BrandLogo from '../shared/components/BrandLogo.jsx'
import Card from '../shared/components/Card.jsx'

const STEPS = [
  {
    title: 'Map farms & fields',
    body: 'Define parcels, areas, and coordinates so every insight ties back to real land.',
  },
  {
    title: 'Capture soil & weather',
    body: 'Log readings or pull data so recommendations reflect what the field actually faces.',
  },
  {
    title: 'Act on ranked crops',
    body: 'See yield, margin, and confidence together—readable on phones and in bright sun.',
  },
]

function LandingPage() {
  const { isAuthenticated } = useAuth()

  return (
    <div className="min-h-screen bg-surface-muted">
      <header className="sticky top-0 z-20 border-b border-stone-200/80 bg-white/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 md:px-6">
          <Link to="/" className="rounded-lg focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40">
            <BrandLogo />
          </Link>
          <div className="flex items-center gap-2">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="inline-flex min-h-11 items-center justify-center rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white shadow-soft transition hover:bg-primary-700"
              >
                Open app
              </Link>
            ) : (
              <>
                <Link
                  to="/login"
                  className="min-h-11 rounded-xl px-4 py-2.5 text-sm font-semibold text-stone-700 transition hover:bg-stone-100"
                >
                  Sign in
                </Link>
                <Link
                  to="/register"
                  className="inline-flex min-h-11 items-center justify-center rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white shadow-soft transition hover:bg-primary-700"
                >
                  Create account
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      <main>
        <section className="relative overflow-hidden border-b border-stone-100 bg-gradient-to-br from-primary-50/90 via-white to-amber-50/30">
          <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 md:grid-cols-2 md:items-center md:px-6 md:py-24">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-primary-800">Field intelligence</p>
              <h1 className="mt-4 font-display text-4xl font-semibold tracking-tight text-stone-900 text-balance md:text-5xl">
                Crop choices grounded in your soil and weather
              </h1>
              <p className="mt-5 max-w-xl text-pretty text-lg leading-relaxed text-stone-600">
                One calm workspace for farms, fields, soil, weather, and AI-ranked recommendations—built for clarity on
                mobile and long days outdoors.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link
                  to={isAuthenticated ? '/recommendations' : '/register'}
                  className="inline-flex min-h-12 items-center justify-center rounded-2xl bg-primary-600 px-6 text-base font-semibold text-white shadow-lift transition hover:bg-primary-700"
                >
                  {isAuthenticated ? 'View recommendations' : 'Get started'}
                </Link>
                <Link
                  to={isAuthenticated ? '/farms' : '/login'}
                  className="inline-flex min-h-12 items-center justify-center rounded-2xl border border-stone-200 bg-white/80 px-6 text-base font-semibold text-stone-800 shadow-sm backdrop-blur hover:bg-white"
                >
                  {isAuthenticated ? 'My farms' : 'Sign in'}
                </Link>
              </div>
            </div>
            <div className="relative">
              <div className="pointer-events-none absolute -right-8 -top-8 h-40 w-40 rounded-full bg-primary-200/40 blur-3xl" />
              <div className="pointer-events-none absolute -bottom-10 -left-10 h-48 w-48 rounded-full bg-amber-200/35 blur-3xl" />
              <img
                src={heroImage}
                alt=""
                className="relative z-10 w-full max-w-lg rounded-3xl border border-white/60 bg-white/40 shadow-lift backdrop-blur md:ml-auto"
              />
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-6xl px-4 py-16 md:px-6 md:py-20">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="font-display text-2xl font-semibold text-stone-900 md:text-3xl">How it works</h2>
            <p className="mt-3 text-pretty text-stone-600">
              Three focused steps—no clutter, no guesswork about where data belongs.
            </p>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {STEPS.map((step, i) => (
              <Card key={step.title} variant="highlight" className="flex flex-col">
                <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-primary-600 text-sm font-bold text-white shadow-soft">
                  {i + 1}
                </span>
                <h3 className="mt-4 font-display text-lg font-semibold text-stone-900">{step.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-stone-600">{step.body}</p>
              </Card>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t border-stone-200 bg-white/80 py-10 text-center text-sm text-stone-500">
        CropAI — crop recommendations for real farms
      </footer>
    </div>
  )
}

export default LandingPage
