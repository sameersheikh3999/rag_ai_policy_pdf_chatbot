import { useState, useRef, useEffect } from 'react'
import Message from './Message'
import SourcesPanel from './SourcesPanel'
import { apiClient } from '../config/api'

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      content: 'Welcome to the AI Policy Analyzer! Ask me any questions about education policies. I analyze Pakistan PDFs and global sources to provide comprehensive, evidence-based answers with citations.',
      sources: []
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [includeWebSearch, setIncludeWebSearch] = useState(true)
  const [currentSources, setCurrentSources] = useState([])
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = input
    setInput('')
    setMessages(prev => [...prev, { type: 'user', content: userMessage }])
    setLoading(true)
    setCurrentSources([])

    try {
      const response = await apiClient.chat(userMessage, includeWebSearch)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let assistantContent = ''
      let sources = []

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n').filter(line => line.trim())

        for (const line of lines) {
          try {
            const json = JSON.parse(line)
            if (json.type === 'content') {
              assistantContent += json.data
              setMessages(prev => {
                const newMessages = [...prev]
                if (newMessages[newMessages.length - 1]?.type !== 'assistant') {
                  newMessages.push({ type: 'assistant', content: assistantContent, sources: [] })
                } else {
                  newMessages[newMessages.length - 1].content = assistantContent
                }
                return newMessages
              })
            } else if (json.type === 'sources') {
              sources = json.data
              setCurrentSources(sources)
            }
          } catch (e) {
            console.error('Parse error:', e)
          }
        }
      }

      setMessages(prev => {
        const newMessages = [...prev]
        if (newMessages[newMessages.length - 1]?.type === 'assistant') {
          newMessages[newMessages.length - 1].sources = sources
        }
        return newMessages
      })

    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [
        ...prev,
        {
          type: 'assistant',
          content: `Error: ${error.message}. Make sure the backend is running.`,
          sources: []
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-slate-900 to-slate-950">
      {/* Header */}
      <div className="border-b border-slate-700/50 bg-slate-900/50 backdrop-blur px-8 py-4">
        <h2 className="text-xl font-bold text-white">Chat & Ask Questions</h2>
        <p className="text-sm text-slate-400 mt-1">Get insights from education policy documents</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className="animate-fadeIn">
            <Message type={msg.type} content={msg.content} />
            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-3">
                <SourcesPanel sources={msg.sources} />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gradient-to-r from-blue-900/40 to-purple-900/40 border border-blue-700/50 text-slate-200 rounded-xl p-5 max-w-xs backdrop-blur">
              <div className="flex items-center space-x-3">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
                <span className="text-sm">Analyzing your question...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Section */}
      <div className="border-t border-slate-700/50 bg-slate-900/50 backdrop-blur p-8 space-y-4">
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 cursor-pointer group">
            <input
              type="checkbox"
              checked={includeWebSearch}
              onChange={(e) => setIncludeWebSearch(e.target.checked)}
              className="w-4 h-4 rounded border-slate-600 text-blue-500 bg-slate-800 cursor-pointer"
            />
            <span className="text-sm text-slate-300 group-hover:text-slate-200 transition-colors flex items-center gap-2">
              <span>🌐</span> Include web search
            </span>
          </label>
        </div>

        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about education policies..."
            className="flex-1 px-6 py-3 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-xl hover:from-blue-700 hover:to-blue-600 disabled:from-slate-700 disabled:to-slate-600 disabled:cursor-not-allowed font-medium transition-all duration-300 shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 flex items-center gap-2"
          >
            <span>Send</span>
            <span>→</span>
          </button>
        </form>
      </div>
    </div>
  )
}
