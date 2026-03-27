import { useEffect, useState } from 'react'
import useToast from '../app/useToast.js'
import { createFarm, deleteFarm, fetchFarms, updateFarm } from '../features/farms/farmsApi.js'
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
  name: '',
  latitude: '',
  longitude: '',
  area: '',
  soil_type: 'unknown',
}

const SOIL_TYPES = [
  { value: 'unknown', label: 'Unknown' },
  { value: 'clay', label: 'Clay' },
  { value: 'sandy', label: 'Sandy' },
  { value: 'loamy', label: 'Loamy' },
  { value: 'silt', label: 'Silt' },
  { value: 'peat', label: 'Peat' },
  { value: 'chalky', label: 'Chalky' },
]

function FarmsPage() {
  const { showToast } = useToast()
  const [farms, setFarms] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState(initialForm)
  const [editing, setEditing] = useState(null)
  const [error, setError] = useState('')

  async function loadFarms() {
    try {
      setError('')
      const data = await fetchFarms()
      setFarms(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let active = true
    fetchFarms()
      .then((data) => {
        if (!active) return
        setFarms(data)
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

  async function handleCreate(event) {
    event.preventDefault()
    setError('')
    try {
      await createFarm({
        ...form,
        latitude: Number(form.latitude),
        longitude: Number(form.longitude),
        area: Number(form.area),
      })
      setForm(initialForm)
      await loadFarms()
      showToast('Farm added successfully', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleUpdate(event) {
    event.preventDefault()
    if (!editing) return
    setError('')
    try {
      await updateFarm(editing.id, {
        name: editing.name,
        latitude: Number(editing.latitude),
        longitude: Number(editing.longitude),
        area: Number(editing.area),
        soil_type: editing.soil_type,
      })
      setEditing(null)
      await loadFarms()
      showToast('Farm updated', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this farm and related data?')) return
    try {
      await deleteFarm(id)
      await loadFarms()
      showToast('Farm removed', 'success')
    } catch (err) {
      showToast(err.message, 'error')
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <div className="grid gap-4 sm:grid-cols-2">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-44" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Land"
        title="Farms"
        description="Register each farm once—name, coordinates, dominant soil, and total area."
      />

      <Card variant="default">
        <h2 className="font-display text-lg font-semibold text-stone-900">Add a farm</h2>
        <p className="mt-1 text-sm text-stone-600">Use WGS84 coordinates. Area is in hectares.</p>
        <form onSubmit={handleCreate} className="mt-6 grid gap-4 md:grid-cols-2">
          <Input
            label="Farm name"
            name="name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
          <Select
            label="Soil type"
            id="soil_type"
            value={form.soil_type}
            onChange={(e) => setForm({ ...form, soil_type: e.target.value })}
          >
            {SOIL_TYPES.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </Select>
          <Input
            label="Latitude"
            name="latitude"
            type="number"
            step="any"
            value={form.latitude}
            onChange={(e) => setForm({ ...form, latitude: e.target.value })}
            required
          />
          <Input
            label="Longitude"
            name="longitude"
            type="number"
            step="any"
            value={form.longitude}
            onChange={(e) => setForm({ ...form, longitude: e.target.value })}
            required
          />
          <Input
            label="Area (hectares)"
            name="area"
            type="number"
            step="0.01"
            min="0.01"
            value={form.area}
            onChange={(e) => setForm({ ...form, area: e.target.value })}
            required
          />
          <div className="flex items-end md:col-span-2">
            <Button type="submit">Add farm</Button>
          </div>
        </form>
        {error ? (
          <div className="mt-4">
            <Alert>{error}</Alert>
          </div>
        ) : null}
      </Card>

      {farms.length === 0 ? (
        <EmptyState
          title="No farms yet"
          description="Create your first farm to unlock fields, soil readings, and recommendations."
          actionLabel="Scroll to form"
          onAction={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {farms.map((farm) => (
            <Card key={farm.id} className="flex flex-col justify-between">
              <div>
                <h3 className="font-display text-lg font-semibold text-stone-900">{farm.name}</h3>
                <p className="mt-1 text-sm text-stone-600">
                  {farm.area} ha · {farm.field_count ?? 0} fields
                </p>
                <p className="mt-2 font-mono text-xs text-stone-500">
                  {farm.latitude}, {farm.longitude}
                </p>
              </div>
              <div className="mt-4 flex shrink-0 flex-wrap gap-2">
                <Button type="button" variant="secondary" size="sm" onClick={() => setEditing({ ...farm })}>
                  Edit
                </Button>
                <Button type="button" variant="danger" size="sm" onClick={() => handleDelete(farm.id)}>
                  Delete
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal
        open={Boolean(editing)}
        title="Edit farm"
        titleId="edit-farm-title"
        onClose={() => setEditing(null)}
      >
        {editing ? (
          <form onSubmit={handleUpdate} className="grid gap-4">
            <Input
              label="Name"
              value={editing.name}
              onChange={(e) => setEditing({ ...editing, name: e.target.value })}
              required
            />
            <Select
              label="Soil type"
              value={editing.soil_type}
              onChange={(e) => setEditing({ ...editing, soil_type: e.target.value })}
            >
              {SOIL_TYPES.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </Select>
            <Input
              label="Latitude"
              type="number"
              step="any"
              value={editing.latitude}
              onChange={(e) => setEditing({ ...editing, latitude: e.target.value })}
              required
            />
            <Input
              label="Longitude"
              type="number"
              step="any"
              value={editing.longitude}
              onChange={(e) => setEditing({ ...editing, longitude: e.target.value })}
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
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="secondary" onClick={() => setEditing(null)}>
                Cancel
              </Button>
              <Button type="submit">Save changes</Button>
            </div>
          </form>
        ) : null}
      </Modal>
    </div>
  )
}

export default FarmsPage
