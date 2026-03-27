import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { registerUser } from '../features/auth/authApi.js'
import BrandLogo from '../shared/components/BrandLogo.jsx'
import Button from '../shared/components/Button.jsx'
import Card from '../shared/components/Card.jsx'
import Input from '../shared/components/Input.jsx'
import Select from '../shared/components/Select.jsx'
import Alert from '../shared/components/Alert.jsx'

const initialForm = {
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  phone: '',
  preferred_language: 'en',
  password: '',
  confirm_password: '',
}

function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      await registerUser(form)
      navigate('/login', { replace: true })
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex min-h-screen bg-surface-muted">
      <div className="relative hidden w-[38%] flex-col justify-between bg-gradient-to-br from-emerald-900 via-primary-700 to-primary-600 p-10 text-white xl:flex">
        <BrandLogo theme="dark" />
        <div>
          <p className="font-display text-3xl font-semibold leading-tight">Start with one account for every field</p>
          <p className="mt-4 max-w-sm text-sm leading-relaxed text-emerald-100/90">
            Add your profile once—then track farms, soil, and weather in a single, readable flow.
          </p>
        </div>
        <p className="text-xs text-emerald-200/80">No credit card · Built for real farm workflows</p>
      </div>

      <div className="flex flex-1 items-center justify-center px-4 py-12">
        <Card className="w-full max-w-2xl border-stone-100 shadow-lift">
          <div className="mb-6 xl:hidden">
            <BrandLogo />
          </div>
          <h1 className="font-display text-2xl font-semibold text-stone-900">Create your account</h1>
          <p className="mt-1 text-sm text-stone-600">We’ll use this to secure your farm data and recommendations.</p>

          <form onSubmit={handleSubmit} className="mt-8 grid gap-4 md:grid-cols-2">
            <div className="md:col-span-2">
              <Input
                label="Username"
                name="username"
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                required
              />
            </div>
            <div className="md:col-span-2">
              <Input
                label="Email"
                name="email"
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
            </div>
            <Input
              label="First name"
              name="first_name"
              value={form.first_name}
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
            />
            <Input
              label="Last name"
              name="last_name"
              value={form.last_name}
              onChange={(e) => setForm({ ...form, last_name: e.target.value })}
            />
            <Input
              label="Phone"
              name="phone"
              value={form.phone}
              onChange={(e) => setForm({ ...form, phone: e.target.value })}
            />
            <Select
              label="Preferred language"
              id="preferred_language"
              name="preferred_language"
              value={form.preferred_language}
              onChange={(e) => setForm({ ...form, preferred_language: e.target.value })}
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="te">Telugu</option>
              <option value="ta">Tamil</option>
              <option value="kn">Kannada</option>
              <option value="mr">Marathi</option>
            </Select>
            <div className="md:col-span-2">
              <Input
                label="Password"
                name="password"
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                hint="At least 8 characters"
                required
              />
            </div>
            <div className="md:col-span-2">
              <Input
                label="Confirm password"
                name="confirm_password"
                type="password"
                value={form.confirm_password}
                onChange={(e) => setForm({ ...form, confirm_password: e.target.value })}
                required
              />
            </div>
            <div className="md:col-span-2">
              <Button type="submit" className="w-full" size="lg" loading={isSubmitting} disabled={isSubmitting}>
                Create account
              </Button>
            </div>
          </form>
          {error ? (
            <div className="mt-4">
              <Alert>{error}</Alert>
            </div>
          ) : null}
          <p className="mt-8 text-center text-sm text-stone-600">
            Already registered?{' '}
            <Link className="font-semibold text-primary-800 hover:underline" to="/login">
              Sign in
            </Link>
          </p>
        </Card>
      </div>
    </div>
  )
}

export default RegisterPage
