function Alert({ children, variant = 'error', className = '' }) {
  const styles = {
    error: 'border-red-100 bg-red-50/90 text-red-800',
    success: 'border-primary-100 bg-primary-50/90 text-primary-900',
    info: 'border-sky-100 bg-sky-50/90 text-sky-900',
  }
  return (
    <div
      role={variant === 'error' ? 'alert' : 'status'}
      className={`rounded-xl border px-3 py-2.5 text-sm font-medium ${styles[variant]} ${className}`}
    >
      {children}
    </div>
  )
}

export default Alert
