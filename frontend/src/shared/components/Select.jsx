function Select({ label, id, error, className = '', children, ...props }) {
  const selectId = id || props.name
  return (
    <div className="w-full">
      {label ? (
        <label htmlFor={selectId} className="mb-1.5 block text-sm font-medium text-stone-700">
          {label}
        </label>
      ) : null}
      <div className="relative">
        <select
          id={selectId}
          className={`w-full min-h-11 appearance-none rounded-xl border bg-white px-3 py-2.5 pr-10 text-stone-900 shadow-sm transition focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/25 ${
            error ? 'border-red-400' : 'border-stone-200'
          } ${className}`}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? `${selectId}-error` : undefined}
          {...props}
        >
          {children}
        </select>
        <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center text-stone-400" aria-hidden>
          <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M6 9l6 6 6-6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </span>
      </div>
      {error ? (
        <p id={`${selectId}-error`} className="mt-1 text-sm text-red-600" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}

export default Select
