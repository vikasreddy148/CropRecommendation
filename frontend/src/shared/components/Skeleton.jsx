function Skeleton({ className = '' }) {
  return (
    <div
      className={`relative overflow-hidden rounded-xl bg-stone-200/80 ${className}`}
      aria-hidden
    >
      <div className="absolute inset-0 -translate-x-full animate-shimmer bg-gradient-to-r from-transparent via-white/50 to-transparent" />
    </div>
  )
}

export default Skeleton
