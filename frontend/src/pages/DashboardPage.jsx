import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { fetchDashboardSummary } from '../features/dashboard/dashboardApi.js'
import { fetchSoilData } from '../features/soil/soilApi.js'
import Badge from '../shared/components/Badge.jsx'
import Card from '../shared/components/Card.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'
import Skeleton from '../shared/components/Skeleton.jsx'
import StatCard from '../shared/components/StatCard.jsx'
import Alert from '../shared/components/Alert.jsx'

function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [soilCount, setSoilCount] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    Promise.all([fetchDashboardSummary(), fetchSoilData().catch(() => [])])
      .then(([dash, soil]) => {
        if (!active) return
        setSummary(dash)
        setSoilCount(soil.length)
      })
      .catch((err) => {
        if (!active) return
        setError(err.message)
      })
    return () => {
      active = false
    }
  }, [])

  if (error) {
    return (
      <Card>
        <PageHeader title="Dashboard" description="We couldn’t load your overview." />
        <div className="mt-4 max-w-lg">
          <Alert>{error}</Alert>
        </div>
        <p className="mt-4 text-sm text-stone-600">
          <Link className="font-semibold text-primary-800 underline" to="/login">
            Sign in
          </Link>{' '}
          to continue.
        </p>
      </Card>
    )
  }

  if (!summary) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-56" />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32" />
          ))}
        </div>
      </div>
    )
  }

  const latest = summary.recentRecommendations?.[0]

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Overview"
        title="Dashboard"
        description="A quick read on farms, fields, soil coverage, and saved recommendations."
        actions={
          <Link
            to="/recommendations"
            className="inline-flex min-h-11 items-center justify-center rounded-xl border border-primary-200 bg-primary-50/50 px-4 py-2.5 text-sm font-semibold text-primary-900 shadow-sm transition hover:bg-primary-50"
          >
            Recommendations
          </Link>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Farms" value={summary.totalFarms} accent="primary" />
        <StatCard label="Fields" value={summary.totalFields} />
        <StatCard
          label="Soil records"
          value={soilCount ?? '—'}
          hint={soilCount === 0 ? 'Add a reading from Soil' : undefined}
          accent="warm"
        >
          <Badge variant={soilCount > 0 ? 'success' : 'warning'} className="mt-3">
            {soilCount > 0 ? 'Data on file' : 'Needs soil data'}
          </Badge>
        </StatCard>
        <StatCard label="Saved recommendations" value={summary.totalRecommendations} />
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        <Card className="lg:col-span-3" variant="default">
          <h2 className="font-display text-lg font-semibold text-stone-900">Latest recommendation</h2>
          {latest ? (
            <div className="mt-4 rounded-2xl border border-primary-100 bg-gradient-to-br from-primary-50/80 to-white p-5">
              <p className="font-display text-xl font-semibold text-primary-950">{latest.cropName}</p>
              <p className="mt-1 text-sm text-stone-600">
                {latest.fieldName} · {Number(latest.confidenceScore).toFixed(0)}% confidence
              </p>
              <Link
                to="/recommendations"
                className="mt-4 inline-flex text-sm font-semibold text-primary-800 hover:underline"
              >
                View all recommendations →
              </Link>
            </div>
          ) : (
            <p className="mt-4 text-sm leading-relaxed text-stone-600">
              No recommendations yet. Add soil and weather, then generate crops for a field.
            </p>
          )}
        </Card>

        <Card className="lg:col-span-2" variant="inset">
          <h2 className="font-display text-lg font-semibold text-stone-900">Next steps</h2>
          <ul className="mt-4 space-y-3 text-sm text-stone-600">
            <li className="flex gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary-500" />
              Register farms and split them into fields for accurate area math.
            </li>
            <li className="flex gap-2">
              <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-primary-500" />
              Capture soil and fetch weather so rankings reflect real conditions.
            </li>
          </ul>
          <div className="mt-6 flex flex-col gap-2 sm:flex-row">
            <Link
              to="/farms"
              className="inline-flex min-h-11 items-center justify-center rounded-xl bg-primary-600 px-4 py-2.5 text-sm font-semibold text-white shadow-soft transition hover:bg-primary-700"
            >
              Manage farms
            </Link>
            <Link
              to="/recommendations"
              className="inline-flex min-h-11 items-center justify-center rounded-xl border border-stone-200 bg-white px-4 py-2.5 text-sm font-semibold text-stone-800 shadow-sm transition hover:bg-stone-50"
            >
              Generate crops
            </Link>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default DashboardPage
