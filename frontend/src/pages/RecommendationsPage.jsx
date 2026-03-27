import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import useToast from '../app/useToast.js'
import { fetchFields } from '../features/farms/farmsApi.js'
import {
  fetchRecommendations,
  requestRecommendations,
  requestRecommendationsForField,
} from '../features/recommendations/recommendationsApi.js'
import Alert from '../shared/components/Alert.jsx'
import Badge from '../shared/components/Badge.jsx'
import Button from '../shared/components/Button.jsx'
import Card from '../shared/components/Card.jsx'
import EmptyState from '../shared/components/EmptyState.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'
import Select from '../shared/components/Select.jsx'
import Skeleton from '../shared/components/Skeleton.jsx'

const CHART_COLORS = { yield: '#059669', profit: '#99f6e4' }

function RecommendationsPage() {
  const navigate = useNavigate()
  const { showToast } = useToast()
  const [fields, setFields] = useState([])
  const [records, setRecords] = useState([])
  const [selectedField, setSelectedField] = useState('')
  const [generated, setGenerated] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)

  const chartData = useMemo(
    () =>
      generated.slice(0, 8).map((item) => ({
        name: item.crop_name?.slice(0, 12) || 'Crop',
        yield: Number(item.expected_yield) || 0,
        profit: Number(item.profit_margin) || 0,
      })),
    [generated]
  )

  useEffect(() => {
    let active = true
    Promise.all([fetchFields(), fetchRecommendations()])
      .then(([fieldData, recData]) => {
        if (!active) return
        setFields(fieldData)
        setRecords(recData)
        if (fieldData.length > 0) {
          setSelectedField(String(fieldData[0].id))
        }
      })
      .catch((err) => {
        if (!active) return
        setError(err.message)
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  async function refreshSaved() {
    const saved = await fetchRecommendations()
    setRecords(saved)
  }

  async function handleRequestManual() {
    setError('')
    setBusy(true)
    try {
      const response = await requestRecommendations({
        field: Number(selectedField),
        include_weather: true,
      })
      setGenerated(response.generated ?? [])
      await refreshSaved()
      showToast('Recommendations generated', 'success')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function handleRequestByField() {
    setError('')
    setBusy(true)
    try {
      const response = await requestRecommendationsForField(Number(selectedField))
      setGenerated(response.generated ?? [])
      await refreshSaved()
      showToast('Recommendations generated', 'success')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-96" />
      </div>
    )
  }

  if (fields.length === 0) {
    return (
      <div className="space-y-6">
        <PageHeader
          eyebrow="Decisions"
          title="Recommendations"
          description="Generate ranked crops for a field using soil, weather, and models."
        />
        <EmptyState
          title="Add a field first"
          description="Recommendations need a field context. Create farms and fields, then return here."
          actionLabel="Go to fields"
          onAction={() => navigate('/fields')}
        />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Decisions"
        title="Recommendations"
        description="Pick a field, generate, and compare yield and profit signals side by side."
      />

      <Card>
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end">
          <div className="flex-1">
            <Select
              label="Field"
              id="rec-field"
              value={selectedField}
              onChange={(e) => setSelectedField(e.target.value)}
            >
              {fields.map((field) => (
                <option key={field.id} value={field.id}>
                  {field.name} ({field.farm_name})
                </option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
            <Button type="button" onClick={handleRequestManual} disabled={!selectedField} loading={busy}>
              Full generate
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={handleRequestByField}
              disabled={!selectedField}
              loading={busy}
            >
              Quick generate
            </Button>
          </div>
        </div>
        {error ? (
          <div className="mt-4">
            <Alert>{error}</Alert>
          </div>
        ) : null}
      </Card>

      {generated.length > 0 ? (
        <Card>
          <h2 className="font-display text-lg font-semibold text-stone-900">Yield & profit snapshot</h2>
          <p className="mt-1 text-sm text-stone-600">Top crops from the latest run—yield and profit in one view.</p>
          <div className="mt-6 h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e7e5e4" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#57534e' }} />
                <YAxis tick={{ fontSize: 11, fill: '#57534e' }} />
                <Tooltip
                  contentStyle={{ borderRadius: '12px', border: '1px solid #e7e5e4' }}
                  formatter={(value, name) => [value, name === 'yield' ? 'Yield (kg/ha)' : 'Profit']}
                />
                <Bar dataKey="yield" fill={CHART_COLORS.yield} radius={[6, 6, 0, 0]} name="yield" />
                <Bar dataKey="profit" fill={CHART_COLORS.profit} radius={[6, 6, 0, 0]} name="profit" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      ) : null}

      {generated.length > 0 ? (
        <div>
          <h2 className="mb-4 font-display text-lg font-semibold text-stone-900">Top matches</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {generated.slice(0, 6).map((item, idx) => (
              <Card key={`${item.crop_name}-${idx}`} variant="highlight">
                <p className="font-display text-2xl font-semibold text-stone-900">{item.crop_name}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Badge variant="success">{(Number(item.confidence_score) || 0).toFixed(0)}% match</Badge>
                  <Badge variant="neutral">Yield {item.expected_yield} kg/ha</Badge>
                  <Badge variant="info">Profit {item.profit_margin}</Badge>
                </div>
              </Card>
            ))}
          </div>
        </div>
      ) : null}

      <div>
        <h2 className="mb-4 font-display text-lg font-semibold text-stone-900">Saved</h2>
        <div className="grid gap-3">
          {records.length === 0 ? (
            <Card variant="inset">
              <p className="text-sm text-stone-600">No saved recommendations yet. Generate a batch above.</p>
            </Card>
          ) : (
            records.map((item) => (
              <Link key={item.id} to={`/recommendations/${item.id}`} className="block rounded-2xl focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500/40">
                <Card className="transition hover:border-primary-200 hover:shadow-lift">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="font-display text-lg font-semibold text-stone-900">{item.crop_name}</p>
                      <p className="text-sm text-stone-600">
                        {item.field_name} · {Number(item.confidence_score).toFixed(0)}% confidence
                      </p>
                    </div>
                    <span className="text-primary-700" aria-hidden>
                      →
                    </span>
                  </div>
                </Card>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default RecommendationsPage
