import Button from './Button.jsx'

function EmptyState({ title, description, actionLabel, onAction, icon }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-stone-200 bg-gradient-to-b from-stone-50/90 to-white px-6 py-14 text-center">
      {icon ? <div className="mb-4 text-primary-600">{icon}</div> : null}
      <h3 className="font-display text-lg font-semibold text-stone-900">{title}</h3>
      {description ? <p className="mt-2 max-w-md text-pretty text-sm leading-relaxed text-stone-600">{description}</p> : null}
      {actionLabel && onAction ? (
        <Button className="mt-6" onClick={onAction}>
          {actionLabel}
        </Button>
      ) : null}
    </div>
  )
}

export default EmptyState
