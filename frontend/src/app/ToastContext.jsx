import { useCallback, useMemo, useState } from 'react'
import ToastContext from './toastContext.js'

function ToastViewport({ toasts }) {
  return (
    <div
      className="pointer-events-none fixed bottom-[calc(5rem+env(safe-area-inset-bottom,0px))] left-0 right-0 z-[100] flex flex-col items-center gap-2 p-4 sm:bottom-auto sm:left-auto sm:right-4 sm:top-4 sm:items-end lg:bottom-4"
      aria-live="polite"
    >
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`pointer-events-auto max-w-md rounded-2xl border px-4 py-3 text-sm font-semibold shadow-lift transition ${
            t.type === 'success'
              ? 'border-primary-100 bg-white text-primary-900'
              : t.type === 'error'
                ? 'border-red-100 bg-white text-red-800'
                : 'border-stone-200 bg-stone-900 text-white'
          }`}
          role="status"
        >
          {t.message}
        </div>
      ))}
    </div>
  )
}

function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const showToast = useCallback((message, type = 'info') => {
    const id = crypto.randomUUID()
    setToasts((prev) => [...prev, { id, message, type }])
    window.setTimeout(() => {
      setToasts((prev) => prev.filter((x) => x.id !== id))
    }, 4200)
  }, [])

  const value = useMemo(() => ({ showToast }), [showToast])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastViewport toasts={toasts} />
    </ToastContext.Provider>
  )
}

export { ToastProvider }
