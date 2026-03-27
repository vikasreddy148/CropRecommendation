import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useToast from '../app/useToast.js'
import {
  createField,
  deleteField,
  fetchFarms,
  fetchFields,
  updateField,
} from '../features/farms/farmsApi.js'
import Alert from '../shared/components/Alert.jsx'
import Button from '../shared/components/Button.jsx'
import Card from '../shared/components/Card.jsx'
import EmptyState from '../shared/components/EmptyState.jsx'
import Input from '../shared/components/Input.jsx'
import Modal from '../shared/components/Modal.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'
import Select from '../shared/components/Select.jsx'
import Skeleton from '../shared/components/Skeleton.jsx'

const initialForm = {
  farm: '',
  name: '',
  latitude: '',
  longitude: '',
  area: '',
}

function FieldsPage() {
  const navigate = useNavigate()
  const { showToast } = useToast()
  const [fields, setFields] = useState([])
  const [farms, setFarms] = useState([])
  const [form, setForm] = useState(initialForm)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null)
  const [error, setError] = useState('')

  const grouped = useMemo(() => {
    const map = new Map()
    farms.forEach((f) => map.set(f.id, { farm: f, fields: [] }))
    fields.forEach((field) => {
      const fid = field.farm
      if (!map.has(fid)) {
        map.set(fid, { farm: { id: fid, name: field.farm_name, area: 0 }, fields: [] })
      }
      map.get(fid).fields.push(field)
    })
    return Array.from(map.values())
  }, [farms, fields])

  async function loadData() {
    try {
      setError('')
      const [farmData, fieldData] = await Promise.all([fetchFarms(), fetchFields()])
      setFarms(farmData)
      setFields(fieldData)
      if (!form.farm && farmData.length > 0) {
        setForm((prev) => ({ ...prev, farm: String(farmData[0].id) }))
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let active = true
    Promise.all([fetchFarms(), fetchFields()])
      .then(([farmData, fieldData]) => {
        if (!active) return
        setFarms(farmData)
        setFields(fieldData)
        if (farmData.length > 0) {
          setForm((prev) => (prev.farm ? prev : { ...prev, farm: String(farmData[0].id) }))
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

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    try {
      await createField({
        farm: Number(form.farm),
        name: form.name,
        latitude: form.latitude ? Number(form.latitude) : null,
        longitude: form.longitude ? Number(form.longitude) : null,
        area: Number(form.area),
      })
      setForm((prev) => ({ ...initialForm, farm: prev.farm }))
      await loadData()
      showToast('Field added', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this field?')) return
    try {
      await deleteField(id)
      await loadData()
      showToast('Field removed', 'success')
    } catch (err) {
      showToast(err.message, 'error')
    }
  }

  async function handleUpdate(e) {
    e.preventDefault()
    if (!editing) return
    try {
      await updateField(editing.id, {
        farm: editing.farm,
        name: editing.name,
        latitude: editing.latitude ? Number(editing.latitude) : null,
        longitude: editing.longitude ? Number(editing.longitude) : null,
        area: Number(editing.area),
      })
      setEditing(null)
      await loadData()
      showToast('Field updated', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  function areaUsed(farmId) {
    const list = fields.filter((f) => f.farm === farmId)
    return list.reduce((s, f) => s + Number(f.area), 0)
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-40" />
        <Skeleton className="h-72" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Land"
        title="Fields"
        description="Split each farm into parcels. Total field area should stay within the farm boundary."
      />

      {farms.length === 0 ? (
        <EmptyState
          title="Create a farm first"
          description="Fields attach to a farm. Add a farm, then return here to draw parcels."
          actionLabel="Go to farms"
          onAction={() => navigate('/farms')}
        />
      ) : (
        <Card>
          <h2 className="font-display text-lg font-semibold text-stone-900">Add a field</h2>
          <p className="mt-1 text-sm text-stone-600">Coordinates are optional but help weather and soil line up.</p>
          <form onSubmit={handleSubmit} className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="md:col-span-2">
              <Select
                label="Farm"
                id="field-farm"
                value={form.farm}
                onChange={(e) => setForm({ ...form, farm: e.target.value })}
                required
              >
                {farms.map((farm) => (
                  <option key={farm.id} value={farm.id}>
                    {farm.name}
                  </option>
                ))}
              </Select>
            </div>
            <Input
              label="Field name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
            <Input
              label="Area (ha)"
              type="number"
              step="0.01"
              min="0.01"
              value={form.area}
              onChange={(e) => setForm({ ...form, area: e.target.value })}
              required
            />
            <Input
              label="Latitude (optional)"
              type="number"
              step="any"
              value={form.latitude}
              onChange={(e) => setForm({ ...form, latitude: e.target.value })}
            />
            <Input
              label="Longitude (optional)"
              type="number"
              step="any"
              value={form.longitude}
              onChange={(e) => setForm({ ...form, longitude: e.target.value })}
            />
            <div className="md:col-span-2">
              <Button type="submit">Add field</Button>
            </div>
          </form>
          {error ? (
            <div className="mt-4">
              <Alert>{error}</Alert>
            </div>
          ) : null}
        </Card>
      )}

      <div className="space-y-6">
        {grouped.map(({ farm, fields: flist }) => {
          const used = areaUsed(farm.id)
          const cap = Number(farm.area) || 1
          const pct = Math.min(100, Math.round((used / cap) * 100))
          return (
            <Card key={farm.id}>
              <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
                <div>
                  <h3 className="font-display text-lg font-semibold text-stone-900">{farm.name}</h3>
                  <p className="text-sm text-stone-600">
                    Farm area {farm.area} ha · Fields use {used.toFixed(2)} ha
                  </p>
                </div>
                <span className="rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold text-primary-900 ring-1 ring-primary-100">
                  {pct}% allocated
                </span>
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-stone-100">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-primary-500 to-emerald-500 transition-[width]"
                  style={{ width: `${pct}%` }}
                />
              </div>
              <ul className="mt-5 space-y-3">
                {flist.length === 0 ? (
                  <li className="text-sm text-stone-600">No fields for this farm yet.</li>
                ) : (
                  flist.map((field) => (
                    <li
                      key={field.id}
                      className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-stone-100 bg-stone-50/80 px-4 py-3"
                    >
                      <div>
                        <p className="font-semibold text-stone-900">{field.name}</p>
                        <p className="text-sm text-stone-600">{field.area} ha</p>
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="secondary" type="button" onClick={() => setEditing({ ...field })}>
                          Edit
                        </Button>
                        <Button size="sm" variant="danger" type="button" onClick={() => handleDelete(field.id)}>
                          Delete
                        </Button>
                      </div>
                    </li>
                  ))
                )}
              </ul>
            </Card>
          )
        })}
      </div>

      <Modal open={Boolean(editing)} title="Edit field" titleId="edit-field-title" onClose={() => setEditing(null)}>
        {editing ? (
          <form onSubmit={handleUpdate} className="grid gap-4">
            <Select
              label="Farm"
              value={editing.farm}
              onChange={(e) => setEditing({ ...editing, farm: Number(e.target.value) })}
            >
              {farms.map((farm) => (
                <option key={farm.id} value={farm.id}>
                  {farm.name}
                </option>
              ))}
            </Select>
            <Input
              label="Name"
              value={editing.name}
              onChange={(e) => setEditing({ ...editing, name: e.target.value })}
              required
            />
            <Input
              label="Area (ha)"
              type="number"
              step="0.01"
              value={editing.area}
              onChange={(e) => setEditing({ ...editing, area: e.target.value })}
              required
            />
            <Input
              label="Latitude"
              type="number"
              step="any"
              value={editing.latitude ?? ''}
              onChange={(e) => setEditing({ ...editing, latitude: e.target.value })}
            />
            <Input
              label="Longitude"
              type="number"
              step="any"
              value={editing.longitude ?? ''}
              onChange={(e) => setEditing({ ...editing, longitude: e.target.value })}
            />
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="secondary" onClick={() => setEditing(null)}>
                Cancel
              </Button>
              <Button type="submit">Save</Button>
            </div>
          </form>
        ) : null}
      </Modal>
    </div>
  )
}

export default FieldsPage
