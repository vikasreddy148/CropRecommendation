import { useEffect } from 'react'
import Button from './Button.jsx'

function Modal({ open, title, titleId, children, onClose, size = 'md' }) {
  useEffect(() => {
    if (!open) return
    function onKey(e) {
      if (e.key === 'Escape') onClose?.()
    }
    window.addEventListener('keydown', onKey)
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      window.removeEventListener('keydown', onKey)
      document.body.style.overflow = prev
    }
  }, [open, onClose])

  if (!open) return null

  const widths = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center p-4 sm:items-center" role="presentation">
      <button
        type="button"
        className="absolute inset-0 bg-stone-900/50 backdrop-blur-[2px]"
        aria-label="Close dialog"
        onClick={onClose}
      />
      <div
        className={`relative z-10 max-h-[min(90vh,880px)] w-full ${widths[size]} overflow-y-auto rounded-2xl border border-stone-100 bg-white shadow-lift`}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? titleId : undefined}
      >
        <div className="flex items-start justify-between gap-3 border-b border-stone-100 px-5 py-4 md:px-6">
          {title ? (
            <h2 id={titleId} className="pr-8 font-display text-lg font-semibold text-stone-900">
              {title}
            </h2>
          ) : (
            <span />
          )}
          <Button type="button" variant="ghost" size="sm" className="shrink-0" onClick={onClose} aria-label="Close dialog">
            <span aria-hidden>✕</span>
          </Button>
        </div>
        <div className="px-5 py-4 md:px-6 md:py-5">{children}</div>
      </div>
    </div>
  )
}

export default Modal
