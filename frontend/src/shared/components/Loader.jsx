function Loader({ label = 'Loading', className = '' }) {
  return (
    <div
      className={`flex flex-col items-center justify-center gap-4 py-16 ${className}`}
      role="status"
      aria-live="polite"
    >
      <span className="relative h-11 w-11">
        <span className="absolute inset-0 animate-ping rounded-full bg-primary-400/30" />
        <span className="absolute inset-1 animate-spin rounded-full border-2 border-primary-600 border-t-transparent" />
      </span>
      <span className="text-sm font-medium text-stone-600">{label}</span>
    </div>
  )
}

export default Loader
