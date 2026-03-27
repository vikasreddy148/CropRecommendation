import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchRecommendationById } from '../features/recommendations/recommendationsApi.js'
import Card from '../shared/components/Card.jsx'
import Loader from '../shared/components/Loader.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'
import Alert from '../shared/components/Alert.jsx'

function RecommendationDetailPage() {
  const { id } = useParams()
  const [record, setRecord] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let isActive = true
    fetchRecommendationById(id)
      .then((data) => {
        if (!isActive) return
        setRecord(data)
      })
      .catch((err) => {
        if (!isActive) return
        setError(err.message)
      })
    return () => {
      isActive = false
    }
  }, [id])

  if (error) {
    return (
      <div className="space-y-6">
        <Card variant="inset" className="border-red-100 bg-red-50/50">
          <PageHeader title="Could not load recommendation" description="The record may have been removed." />
          <div className="mt-4 max-w-lg">
            <Alert>{error}</Alert>
          </div>
          <Link
            to="/recommendations"
            className="mt-6 inline-flex min-h-11 items-center justify-center rounded-xl border border-stone-200 bg-white px-4 py-2.5 text-sm font-semibold text-primary-900 shadow-sm hover:bg-stone-50"
          >
            Back to recommendations
          </Link>
        </Card>
      </div>
    )
  }

  if (!record) {
    return <Loader label="Loading recommendation…" className="min-h-[40vh]" />
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <PageHeader
          eyebrow={`ID ${record.id}`}
          title={record.crop_name}
          description={record.field_name ? `${record.field_name}` : 'Field-linked recommendation'}
        />
        <Link
          to="/recommendations"
          className="inline-flex min-h-11 shrink-0 items-center justify-center rounded-xl border border-stone-200 bg-white px-4 py-2.5 text-sm font-semibold text-stone-800 shadow-sm hover:bg-stone-50"
        >
          ← All recommendations
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card variant="highlight" className="border-primary-100">
          <p className="text-xs font-semibold uppercase tracking-wider text-primary-900">Expected yield</p>
          <p className="mt-2 font-display text-3xl font-semibold tabular-nums text-stone-900">{record.expected_yield ?? '—'}</p>
        </Card>
        <Card>
          <p className="text-xs font-semibold uppercase tracking-wider text-stone-500">Profit margin</p>
          <p className="mt-2 font-display text-3xl font-semibold tabular-nums text-stone-900">{record.profit_margin ?? '—'}</p>
        </Card>
        <Card>
          <p className="text-xs font-semibold uppercase tracking-wider text-stone-500">Confidence</p>
          <p className="mt-2 flex items-baseline gap-1">
            <span className="font-display text-3xl font-semibold tabular-nums text-stone-900">
              {record.confidence_score ?? '—'}
            </span>
            {record.confidence_score != null ? <span className="text-sm text-stone-500">%</span> : null}
          </p>
        </Card>
        <Card>
          <p className="text-xs font-semibold uppercase tracking-wider text-stone-500">Sustainability</p>
          <p className="mt-2 font-display text-3xl font-semibold tabular-nums text-stone-900">{record.sustainability_score ?? '—'}</p>
        </Card>
      </div>

      <Card>
        <h2 className="font-display text-lg font-semibold text-stone-900">Details</h2>
        <dl className="mt-5 grid gap-6 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-stone-500">Crop</dt>
            <dd className="mt-1 text-base font-semibold text-stone-900">{record.crop_name ?? '—'}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-stone-500">Field</dt>
            <dd className="mt-1 text-base font-semibold text-stone-900">{record.field_name ?? '—'}</dd>
          </div>
        </dl>
      </Card>
    </div>
  )
}

export default RecommendationDetailPage
