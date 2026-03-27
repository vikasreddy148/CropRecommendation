import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import useToast from '../app/useToast.js'
import { fetchFields } from '../features/farms/farmsApi.js'
import { createSoilData, fetchSoilData, fetchSoilFromSource } from '../features/soil/soilApi.js'
import Alert from '../shared/components/Alert.jsx'
import Badge from '../shared/components/Badge.jsx'
import Button from '../shared/components/Button.jsx'
import Card from '../shared/components/Card.jsx'
import EmptyState from '../shared/components/EmptyState.jsx'
import Input from '../shared/components/Input.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'
import Select from '../shared/components/Select.jsx'
import Skeleton from '../shared/components/Skeleton.jsx'

function SoilPage() {
  const navigate = useNavigate()
  const { showToast } = useToast()
  const [fields, setFields] = useState([])
  const [soilData, setSoilData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    field: '',
    ph: '',
    moisture: '',
    n: '',
    p: '',
    k: '',
  })

  async function reloadSoilData() {
    const data = await fetchSoilData()
    setSoilData(data)
  }

  useEffect(() => {
    let active = true
    Promise.all([fetchFields(), fetchSoilData()])
      .then(([fieldData, soilList]) => {
        if (!active) return
        setFields(fieldData)
        setSoilData(soilList)
        if (fieldData.length > 0) {
          setForm((prev) => (prev.field ? prev : { ...prev, field: String(fieldData[0].id) }))
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

  async function handleManualSubmit(event) {
    event.preventDefault()
    setError('')
    try {
      await createSoilData({
        field: Number(form.field),
        ph: form.ph ? Number(form.ph) : null,
        moisture: form.moisture ? Number(form.moisture) : null,
        n: form.n ? Number(form.n) : null,
        p: form.p ? Number(form.p) : null,
        k: form.k ? Number(form.k) : null,
        source: 'manual',
      })
      await reloadSoilData()
      showToast('Soil data saved', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleFetch() {
    setError('')
    try {
      await fetchSoilFromSource({ field: Number(form.field), source: 'auto' })
      await reloadSoilData()
      showToast('Soil data fetched', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <Skeleton className="h-72" />
      </div>
    )
  }

  if (fields.length === 0) {
    return (
      <div className="space-y-6">
        <PageHeader
          eyebrow="Field data"
          title="Soil"
          description="Log nutrients and pH for each field—or fetch from a connected source."
        />
        <EmptyState
          title="Add a field first"
          description="Soil readings attach to a field. Create farms, add fields, then record soil here."
          actionLabel="Go to fields"
          onAction={() => navigate('/fields')}
        />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Field data"
        title="Soil"
        description="Keep NPK, pH, and moisture aligned with the parcel you are managing."
      />

      <Card>
        <h2 className="font-display text-lg font-semibold text-stone-900">New reading</h2>
        <p className="mt-1 text-sm text-stone-600">Leave a value blank if unknown—we’ll still store what you have.</p>
        {error ? (
          <div className="mt-4">
            <Alert>{error}</Alert>
          </div>
        ) : null}
        <form onSubmit={handleManualSubmit} className="mt-6 grid gap-4 md:grid-cols-2">
          <div className="md:col-span-2">
            <Select
              label="Field"
              id="soil-field"
              value={form.field}
              onChange={(e) => setForm({ ...form, field: e.target.value })}
              required
            >
              {fields.map((field) => (
                <option key={field.id} value={field.id}>
                  {field.name} ({field.farm_name})
                </option>
              ))}
            </Select>
          </div>
          <Input
            label="pH"
            type="number"
            step="0.01"
            value={form.ph}
            onChange={(e) => setForm({ ...form, ph: e.target.value })}
          />
          <Input
            label="Moisture %"
            type="number"
            step="0.01"
            value={form.moisture}
            onChange={(e) => setForm({ ...form, moisture: e.target.value })}
          />
          <div className="md:col-span-2">
            <p className="mb-3 text-sm font-semibold text-stone-800">Nutrients (kg/ha)</p>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border border-sky-100 bg-sky-50/50 p-3">
                <span className="flex items-center gap-2 text-xs font-semibold text-sky-900">
                  <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-200/80 text-xs font-bold">
                    N
                  </span>
                  Nitrogen
                </span>
                <input
                  type="number"
                  step="0.01"
                  value={form.n}
                  onChange={(e) => setForm({ ...form, n: e.target.value })}
                  className="mt-2 w-full min-h-11 rounded-xl border border-sky-100 bg-white px-3 py-2.5 text-stone-900 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/25"
                />
              </div>
              <div className="rounded-2xl border border-amber-100 bg-amber-50/50 p-3">
                <span className="flex items-center gap-2 text-xs font-semibold text-amber-900">
                  <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-200/80 text-xs font-bold">
                    P
                  </span>
                  Phosphorus
                </span>
                <input
                  type="number"
                  step="0.01"
                  value={form.p}
                  onChange={(e) => setForm({ ...form, p: e.target.value })}
                  className="mt-2 w-full min-h-11 rounded-xl border border-amber-100 bg-white px-3 py-2.5 text-stone-900 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/25"
                />
              </div>
              <div className="rounded-2xl border border-emerald-100 bg-emerald-50/50 p-3">
                <span className="flex items-center gap-2 text-xs font-semibold text-emerald-900">
                  <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-200/80 text-xs font-bold">
                    K
                  </span>
                  Potassium
                </span>
                <input
                  type="number"
                  step="0.01"
                  value={form.k}
                  onChange={(e) => setForm({ ...form, k: e.target.value })}
                  className="mt-2 w-full min-h-11 rounded-xl border border-emerald-100 bg-white px-3 py-2.5 text-stone-900 shadow-sm focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/25"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 md:col-span-2">
            <Button type="submit">Save reading</Button>
            <Button type="button" variant="secondary" onClick={handleFetch} disabled={!form.field}>
              Fetch from source
            </Button>
          </div>
        </form>
      </Card>

      <div>
        <h2 className="mb-4 font-display text-lg font-semibold text-stone-900">Recent records</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {soilData.length === 0 ? (
            <Card variant="inset">
              <p className="text-sm text-stone-600">No soil data yet. Save a reading or fetch from source.</p>
              <Link to="/fields" className="mt-3 inline-block text-sm font-semibold text-primary-800 hover:underline">
                Review fields →
              </Link>
            </Card>
          ) : (
            soilData.slice(0, 12).map((item) => (
              <Card key={item.id}>
                <p className="font-semibold text-stone-900">{item.field_name}</p>
                <p className="text-xs text-stone-500">{item.farm_name}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Badge variant="neutral">pH {item.ph ?? '—'}</Badge>
                  <Badge variant="info">N {item.n ?? '—'}</Badge>
                  <Badge variant="warning">P {item.p ?? '—'}</Badge>
                  <Badge variant="success">K {item.k ?? '—'}</Badge>
                </div>
                <p className="mt-3 text-xs text-stone-400">Source: {item.source}</p>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default SoilPage
