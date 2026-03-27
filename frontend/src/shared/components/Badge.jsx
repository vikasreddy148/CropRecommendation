function Badge({ children, variant = 'neutral', className = '' }) {
  const styles = {
    success: 'bg-primary-50 text-primary-900 ring-1 ring-primary-200/80',
    warning: 'bg-amber-50 text-amber-900 ring-1 ring-amber-200/80',
    danger: 'bg-red-50 text-red-800 ring-1 ring-red-200/80',
    neutral: 'bg-stone-100 text-stone-700 ring-1 ring-stone-200/80',
    info: 'bg-sky-50 text-sky-900 ring-1 ring-sky-200/80',
  }
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${styles[variant]} ${className}`}
    >
      {children}
    </span>
  )
}

export default Badge
