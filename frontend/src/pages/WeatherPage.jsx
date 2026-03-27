import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import useToast from '../app/useToast.js'
import { fetchFields } from '../features/farms/farmsApi.js'
import { fetchWeatherData, fetchWeatherFromField } from '../features/weather/weatherApi.js'
import Alert from '../shared/components/Alert.jsx'
import Button from '../shared/components/Button.jsx'
import Card from '../shared/components/Card.jsx'
import EmptyState from '../shared/components/EmptyState.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'
import Select from '../shared/components/Select.jsx'
import Skeleton from '../shared/components/Skeleton.jsx'

function WeatherPage() {
  const navigate = useNavigate()
  const { showToast } = useToast()
  const [fields, setFields] = useState([])
  const [weatherData, setWeatherData] = useState([])
  const [selectedField, setSelectedField] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    Promise.all([fetchFields(), fetchWeatherData()])
      .then(([fieldData, weatherList]) => {
        if (!active) return
        setFields(fieldData)
        setWeatherData(weatherList)
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

  async function refreshWeather() {
    const data = await fetchWeatherData()
    setWeatherData(data)
  }

  async function handleFetch() {
    setError('')
    try {
      await fetchWeatherFromField({ field: Number(selectedField) })
      await refreshWeather()
      showToast('Weather updated', 'success')
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-48" />
        <div className="grid gap-4 sm:grid-cols-2">
          <Skeleton className="h-40" />
          <Skeleton className="h-40" />
        </div>
      </div>
    )
  }

  if (fields.length === 0) {
    return (
      <div className="space-y-6">
        <PageHeader
          eyebrow="Field data"
          title="Weather"
          description="Pull current conditions using a field’s coordinates."
        />
        <EmptyState
          title="Add a field first"
          description="Weather is tied to a field location. Create fields, then fetch weather snapshots here."
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
        title="Weather"
        description="Fetch the latest snapshot for a field. History stays in the cards below."
      />

      <Card>
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end">
          <div className="flex-1">
            <Select
              label="Field"
              id="weather-field"
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
          <Button type="button" onClick={handleFetch} disabled={!selectedField} className="w-full shrink-0 lg:w-auto">
            Fetch current weather
          </Button>
        </div>
        {error ? (
          <div className="mt-4">
            <Alert>{error}</Alert>
          </div>
        ) : null}
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {weatherData.length === 0 ? (
          <Card variant="inset" className="sm:col-span-2 lg:col-span-3">
            <p className="text-sm text-stone-600">
              No weather records yet. Choose a field and fetch to populate this list.
            </p>
          </Card>
        ) : (
          weatherData.map((item) => (
            <Card key={item.id} className="relative overflow-hidden">
              <div className="pointer-events-none absolute -right-6 -top-10 h-28 w-28 rounded-full bg-sky-100/80 blur-2xl" />
              <p className="text-xs font-semibold uppercase tracking-wider text-stone-400">{item.date}</p>
              <p className="mt-1 font-display text-4xl font-semibold tabular-nums text-stone-900">{item.temperature}°C</p>
              <p className="text-sm text-stone-600">Ambient temperature</p>
              <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
                <div className="rounded-2xl border border-sky-100 bg-sky-50/80 px-3 py-2 text-sky-950">
                  <p className="text-xs font-medium text-sky-800">Humidity</p>
                  <p className="font-semibold text-sky-950">{item.humidity}%</p>
                </div>
                <div className="rounded-2xl border border-blue-100 bg-blue-50/80 px-3 py-2 text-blue-950">
                  <p className="text-xs font-medium text-blue-800">Rain</p>
                  <p className="font-semibold text-blue-950">{item.rainfall} mm</p>
                </div>
                <div className="rounded-2xl border border-stone-100 bg-stone-50 px-3 py-2">
                  <p className="text-xs font-medium text-stone-600">Wind</p>
                  <p className="font-semibold text-stone-900">{item.wind_speed} km/h</p>
                </div>
                <div className="rounded-2xl border border-primary-100 bg-primary-50/80 px-3 py-2 text-primary-950">
                  <p className="text-xs font-medium text-primary-800">Condition</p>
                  <p className="font-semibold leading-snug text-primary-950">
                    {item.forecast_data?.description ?? '—'}
                  </p>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}

export default WeatherPage
