import { useEffect, useRef, useState } from 'react'
import Card from '../shared/components/Card.jsx'
import Button from '../shared/components/Button.jsx'
import PageHeader from '../shared/components/PageHeader.jsx'

const DEMO_MESSAGES = [
  {
    id: '1',
    role: 'assistant',
    text: 'नमस्ते! Ask about soil, weather, or crop recommendations in your language.',
  },
]

function ChatPage() {
  const [messages, setMessages] = useState(DEMO_MESSAGES)
  const [input, setInput] = useState('')
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function send() {
    const text = input.trim()
    if (!text) return
    setMessages((m) => [...m, { id: crypto.randomUUID(), role: 'user', text }])
    setInput('')
    window.setTimeout(() => {
      setMessages((m) => [
        ...m,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          text:
            'This is a demo reply. Connect the chat backend when ready — your message was received safely. धन्यवाद!',
        },
      ])
    }, 400)
  }

  return (
    <div className="flex flex-col">
      <PageHeader
        eyebrow="Help"
        title="Assistant"
        description="Ask in English, हिंदी, తెలుగు, or other languages. Replies are demo-only until the API is wired."
      />

      <Card
        className="mt-4 flex min-h-[min(520px,calc(100dvh-13rem))] flex-col overflow-hidden p-0"
        padding={false}
      >
        <div
          className="flex-1 space-y-4 overflow-y-auto bg-gradient-to-b from-stone-50/90 to-white px-4 py-5"
          role="log"
          aria-live="polite"
        >
          {messages.map((msg) => (
            <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[min(92%,28rem)] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-soft ${
                  msg.role === 'user'
                    ? 'rounded-br-md bg-primary-600 text-white'
                    : 'rounded-bl-md border border-stone-100 bg-white text-stone-800'
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>
        <div className="border-t border-stone-100 bg-white/95 p-3 backdrop-blur">
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), send())}
              placeholder="Ask about crops, soil, or weather…"
              className="min-h-12 flex-1 rounded-2xl border border-stone-200 bg-white px-4 py-3 text-sm text-stone-900 shadow-sm placeholder:text-stone-400 focus:border-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500/25"
              aria-label="Message"
            />
            <Button onClick={send} disabled={!input.trim()} size="lg">
              Send
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default ChatPage
