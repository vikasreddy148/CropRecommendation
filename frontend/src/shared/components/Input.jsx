function Input({ label, error, hint, id, className = '', ...props }) {
  const inputId = id || props.name
  return (
    <div className="w-full">
      {label ? (
        <label htmlFor={inputId} className="mb-1.5 block text-sm font-medium text-stone-700">
          {label}
        </label>
      ) : null}
      <input
        id={inputId}
        className={`w-full min-h-11 rounded-xl border bg-white px-3 py-2.5 text-stone-900 shadow-sm transition placeholder:text-stone-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/25 ${
          error ? 'border-red-400' : 'border-stone-200'
        } ${className}`}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        {...props}
      />
      {hint && !error ? (
        <p id={`${inputId}-hint`} className="mt-1 text-xs text-stone-500">
          {hint}
        </p>
      ) : null}
      {error ? (
        <p id={`${inputId}-error`} className="mt-1 text-sm text-red-600" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  )
}

export default Input
