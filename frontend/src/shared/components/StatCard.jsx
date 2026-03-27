import Card from './Card.jsx'

function StatCard({ label, value, hint, accent = 'default', children }) {
  const accents = {
    default: 'from-white to-stone-50/80',
    primary: 'from-primary-50/90 to-white border-primary-100/80',
    warm: 'from-amber-50/50 to-white border-amber-100/60',
  }
  return (
    <Card className={`relative overflow-hidden border-stone-100/90 bg-gradient-to-br ${accents[accent]}`}>
      <p className="text-xs font-medium uppercase tracking-wide text-stone-500">{label}</p>
      <p className="mt-2 font-display text-3xl font-semibold tabular-nums text-stone-900">{value}</p>
      {hint ? <p className="mt-1 text-sm text-stone-500">{hint}</p> : null}
      {children}
    </Card>
  )
}

export default StatCard
