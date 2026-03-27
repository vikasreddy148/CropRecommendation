function BrandLogo({ className = '', compact = false, theme = 'light' }) {
  const isDark = theme === 'dark'
  return (
    <span
      className={`inline-flex items-center gap-2 font-display font-semibold tracking-tight ${
        isDark ? 'text-white' : 'text-stone-900'
      } ${className}`}
    >
      <span
        className={`flex h-8 w-8 items-center justify-center rounded-xl text-sm font-bold shadow-soft ${
          isDark
            ? 'bg-white/15 text-white ring-1 ring-white/25'
            : 'bg-gradient-to-br from-primary-500 to-primary-700 text-white'
        }`}
        aria-hidden
      >
        C
      </span>
      {!compact ? (
        <span className="text-lg">
          Crop<span className={isDark ? 'text-emerald-200' : 'text-primary-600'}>AI</span>
        </span>
      ) : null}
    </span>
  )
}

export default BrandLogo
