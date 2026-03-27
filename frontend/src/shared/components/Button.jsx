function Button({
  children,
  type = 'button',
  variant = 'primary',
  size = 'md',
  className = '',
  disabled,
  loading,
  ...props
}) {
  const variants = {
    primary:
      'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500 disabled:bg-stone-300',
    secondary:
      'border border-stone-200 bg-white text-stone-800 shadow-sm hover:bg-stone-50 focus-visible:ring-stone-300',
    outline:
      'border border-primary-200 bg-primary-50/50 text-primary-900 hover:bg-primary-50 focus-visible:ring-primary-400',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
    ghost: 'bg-transparent text-primary-800 hover:bg-primary-50 focus-visible:ring-primary-300',
  }
  const sizes = {
    sm: 'min-h-10 px-3 py-2 text-sm rounded-xl',
    md: 'min-h-11 px-4 py-2.5 text-sm font-semibold rounded-xl',
    lg: 'min-h-12 px-5 py-3 text-base font-semibold rounded-2xl',
  }

  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`inline-flex touch-target items-center justify-center gap-2 font-medium transition focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-white disabled:cursor-not-allowed ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {loading ? (
        <span
          className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
          aria-hidden
        />
      ) : null}
      {children}
    </button>
  )
}

export default Button
