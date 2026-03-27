import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import useAuth from '../app/useAuth.js'
import { fetchCurrentUser, loginWithSession } from '../features/auth/authApi.js'
import BrandLogo from '../shared/components/BrandLogo.jsx'
import Button from '../shared/components/Button.jsx'
import Card from '../shared/components/Card.jsx'
import Input from '../shared/components/Input.jsx'
import Alert from '../shared/components/Alert.jsx'

function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { setUser } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      await loginWithSession({ username, password })
      const user = await fetchCurrentUser()
      setUser(user)
      const nextPath = location.state?.from ?? '/dashboard'
      navigate(nextPath, { replace: true })
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-surface-muted">
      <div className="relative hidden w-[42%] flex-col justify-between bg-gradient-to-br from-primary-700 via-primary-600 to-emerald-900 p-10 text-white lg:flex">
        <BrandLogo theme="dark" />
        <div>
          <p className="font-display text-3xl font-semibold leading-tight">Welcome back to your fields</p>
          <p className="mt-4 max-w-sm text-sm leading-relaxed text-emerald-100/90">
            Sign in to manage farms, sync soil and weather, and review crop recommendations tailored to each parcel.
          </p>
        </div>
        <p className="text-xs text-emerald-200/80">Secure session · Same experience on phone and desktop</p>
      </div>

      <div className="flex flex-1 items-center justify-center px-4 py-12">
        <Card className="w-full max-w-md border-stone-100 shadow-lift">
          <div className="mb-6 lg:hidden">
            <BrandLogo />
          </div>
          <h1 className="font-display text-2xl font-semibold text-stone-900">Sign in</h1>
          <p className="mt-1 text-sm text-stone-600">Use your account to access farms and recommendations.</p>

          <form onSubmit={handleSubmit} className="mt-8 space-y-4">
            <Input
              label="Username"
              name="username"
              autoComplete="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <Input
              label="Password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Button type="submit" className="w-full" size="lg" loading={isSubmitting} disabled={isSubmitting}>
              Continue
            </Button>
          </form>
          {error ? (
            <div className="mt-4">
              <Alert>{error}</Alert>
            </div>
          ) : null}
          <p className="mt-8 text-center text-sm text-stone-600">
            New here?{' '}
            <Link className="font-semibold text-primary-800 hover:underline" to="/register">
              Create an account
            </Link>
          </p>
        </Card>
      </div>
    </div>
  )
}

export default LoginPage
