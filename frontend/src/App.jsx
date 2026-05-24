import { useState, useEffect } from 'react'
import ChatWindow from './components/ChatWindow'
import PolicyEvaluator from './components/PolicyEvaluator'
import './App.css'

export default function App() {
  const [mode, setMode] = useState('chat')
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDocuments()
    checkBackendHealth()
  }, [])

  const checkBackendHealth = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      const data = await response.json()
      if (!data.rag_ready) {
        setError('RAG pipeline not ready. Please run ingest.py first.')
      }
    } catch (err) {
      setError('Backend not responding. Make sure FastAPI is running on port 8000.')
    }
  }

  const fetchDocuments = async () => {
    try {
      const response = await fetch('http://localhost:8000/documents')
      const data = await response.json()
      setDocuments(data.documents || [])
      setLoading(false)
    } catch (err) {
      console.error('Error fetching documents:', err)
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* Sidebar */}
      <div className="w-72 bg-gradient-to-b from-slate-900 to-slate-950 border-r border-slate-700 shadow-2xl overflow-y-auto">
        <div className="p-8">
          {/* Logo/Title */}
          <div className="mb-8">
            <div className="inline-flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <span className="text-white font-bold text-lg">📋</span>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                PolicyAI
              </h1>
            </div>
            <p className="text-xs text-slate-400 ml-13">Intelligent policy analysis</p>
          </div>

          {/* Mode Toggle */}
          <div className="mb-8">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">Mode</h3>
            <div className="space-y-3 bg-slate-800/50 p-3 rounded-lg border border-slate-700">
              <button
                onClick={() => setMode('chat')}
                className={`w-full px-4 py-3 rounded-lg text-sm font-medium transition-all duration-300 flex items-center gap-2 justify-center ${
                  mode === 'chat'
                    ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/30 scale-105'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                <span>💬</span> Chat & Q&A
              </button>
              <button
                onClick={() => setMode('evaluate')}
                className={`w-full px-4 py-3 rounded-lg text-sm font-medium transition-all duration-300 flex items-center gap-2 justify-center ${
                  mode === 'evaluate'
                    ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white shadow-lg shadow-purple-500/30 scale-105'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                <span>📊</span> Evaluate Policy
              </button>
            </div>
          </div>

          {/* Documents Section */}
          <div>
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-4">
              📚 Documents ({documents.length})
            </h3>
            <div className="bg-slate-800/50 rounded-lg border border-slate-700 p-4 max-h-64 overflow-y-auto">
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                </div>
              ) : documents.length > 0 ? (
                <ul className="space-y-2">
                  {documents.map((doc, idx) => (
                    <li key={idx} className="group p-2 rounded hover:bg-slate-700/50 transition-colors cursor-pointer">
                      <div className="flex items-start gap-2">
                        <span className="text-blue-400 text-lg flex-shrink-0">📄</span>
                        <div className="min-w-0 flex-1">
                          <p className="text-xs font-medium text-slate-200 truncate group-hover:text-blue-400 transition-colors">
                            {doc.filename}
                          </p>
                          <p className="text-xs text-slate-500">{doc.pages.length} pages</p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-xs text-slate-500 text-center py-8">No documents loaded</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative overflow-hidden">
        {error && (
          <div className="mx-4 mt-4 p-4 rounded-lg bg-red-900/30 border border-red-700 text-red-200 text-sm backdrop-blur-sm">
            <div className="flex items-start gap-3">
              <span className="text-lg flex-shrink-0">⚠️</span>
              <div>
                <p className="font-medium">Connection Error</p>
                <p className="text-xs mt-1 text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {mode === 'chat' ? (
          <ChatWindow />
        ) : (
          <PolicyEvaluator />
        )}
      </div>
    </div>
  )
}
