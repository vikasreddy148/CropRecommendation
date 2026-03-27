function PageHeader({ title, description, eyebrow, actions, className = '' }) {
  return (
    <header className={`flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between ${className}`}>
      <div className="min-w-0">
        {eyebrow ? (
          <p className="text-xs font-semibold uppercase tracking-wider text-primary-700">{eyebrow}</p>
        ) : null}
        <h1 className="font-display text-2xl font-semibold tracking-tight text-stone-900 md:text-3xl">{title}</h1>
        {description ? <p className="mt-1 max-w-2xl text-pretty text-sm leading-relaxed text-stone-600">{description}</p> : null}
      </div>
      {actions ? <div className="flex shrink-0 flex-wrap items-center gap-2">{actions}</div> : null}
    </header>
  )
}

export default PageHeader
