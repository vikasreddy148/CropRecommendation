function Card({ children, className = '', padding = true, variant = 'default' }) {
  const variants = {
    default: 'border-stone-100/90 bg-white shadow-card',
    inset: 'border-transparent bg-stone-50/80 shadow-none',
    highlight: 'border-primary-100/80 bg-gradient-to-br from-primary-50/40 via-white to-white shadow-soft',
  }
  return (
    <div
      className={`rounded-2xl border ${variants[variant]} ${padding ? 'p-5 md:p-6' : ''} ${className}`}
    >
      {children}
    </div>
  )
}

export default Card
