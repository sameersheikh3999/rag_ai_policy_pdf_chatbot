import { useState, useRef, useEffect } from 'react'
import SourcesPanel from './SourcesPanel'
import { apiClient } from '../config/api'

export default function PolicyEvaluator() {
  const [policyText, setPolicyText] = useState('')
  const [loading, setLoading] = useState(false)
  const [evaluation, setEvaluation] = useState(null)
  const [sources, setSources] = useState([])
  const [error, setError] = useState(null)
  const resultsRef = useRef(null)

  useEffect(() => {
    if (evaluation) {
      resultsRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [evaluation])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!policyText.trim()) return

    setLoading(true)
    setError(null)
    setEvaluation(null)

    try {
      const data = await apiClient.evaluatePolicy(policyText)
      setEvaluation(data.evaluation)
      setSources(data.sources || [])

    } catch (err) {
      console.error('Error:', err)
      setError(`Error evaluating policy: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const parseEvaluation = (text) => {
    const sections = []
    const lines = text.split('\n')
    let currentSection = null

    lines.forEach((line) => {
      if (line.startsWith('##')) {
        if (currentSection) sections.push(currentSection)
        currentSection = { title: line.replace(/##\s*/g, ''), content: [] }
      } else if (line.trim() && currentSection) {
        currentSection.content.push(line)
      }
    })

    if (currentSection) sections.push(currentSection)
    return sections.length > 0 ? sections : null
  }

  const sections = evaluation ? parseEvaluation(evaluation) : null

  return (
    <div className="flex flex-col h-full overflow-y-auto bg-gradient-to-b from-slate-900 to-slate-950">
      {/* Header */}
      <div className="border-b border-slate-700/50 bg-slate-900/50 backdrop-blur px-8 py-6">
        <h2 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
          Policy Evaluator & Standardization
        </h2>
        <p className="text-sm text-slate-400 mt-2">Submit your policy for comprehensive evaluation with comparisons, standardization, and best practice recommendations</p>
      </div>

      {/* Input Section */}
      <div className="border-b border-slate-700/50 bg-slate-900/30 p-8">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-3">
              Your Policy Proposal
            </label>
            <textarea
              value={policyText}
              onChange={(e) => setPolicyText(e.target.value)}
              placeholder="Describe your policy direction. Example: Implement universal basic education with focus on digital literacy, teacher capacity building, and equitable resource allocation to rural areas..."
              className="w-full h-48 px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all"
              disabled={loading}
            />
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-400">
            <span>🌐 Web search enabled</span>
            <span>•</span>
            <span>📊 Comparison analysis included</span>
            <span>•</span>
            <span>✅ Standardization framework applied</span>
          </div>
          <button
            type="submit"
            disabled={loading || !policyText.trim()}
            className="inline-flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-purple-600 to-purple-500 text-white rounded-xl hover:from-purple-700 hover:to-purple-600 disabled:from-slate-700 disabled:to-slate-600 disabled:cursor-not-allowed font-medium transition-all duration-300 shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50"
          >
            <span>⚡</span>
            <span>{loading ? 'Analyzing & Comparing...' : 'Evaluate & Standardize'}</span>
          </button>
        </form>
      </div>

      {/* Results Section */}
      <div className="flex-1 overflow-y-auto p-8 space-y-6">
        {error && (
          <div className="p-4 rounded-xl bg-red-900/30 border border-red-700 text-red-200 text-sm backdrop-blur-sm">
            <div className="flex items-start gap-3">
              <span className="text-lg flex-shrink-0">⚠️</span>
              <div>
                <p className="font-medium">Evaluation Error</p>
                <p className="text-xs mt-1 text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {loading && (
          <div className="flex justify-center items-center py-16">
            <div className="text-center">
              <div className="flex space-x-2 justify-center mb-6">
                <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-bounce"></div>
                <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-3 h-3 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
              <p className="text-slate-400 font-medium">Comparing your policy with global best practices...</p>
              <p className="text-slate-500 text-sm mt-2">Analyzing PDFs and web sources for standardization</p>
            </div>
          </div>
        )}

        {evaluation && (
          <div ref={resultsRef} className="space-y-6 animate-slideInUp">
            {/* Structured Analysis Cards */}
            {sections && sections.map((section, idx) => (
              <div key={idx} className="bg-gradient-to-br from-slate-800/50 to-slate-800/30 border border-slate-700/50 rounded-xl overflow-hidden">
                <div className="bg-gradient-to-r from-purple-600/30 to-blue-600/30 px-6 py-4 border-b border-slate-700/50">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    {idx === 0 && '📊'}
                    {idx === 1 && '📈'}
                    {idx === 2 && '🎯'}
                    {idx === 3 && '💪'}
                    {idx === 4 && '🚀'}
                    {section.title}
                  </h3>
                </div>
                <div className="p-6 space-y-3">
                  {section.content.map((line, lineIdx) => {
                    const trimmed = line.trim()
                    if (!trimmed) return null

                    if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
                      return (
                        <div key={lineIdx} className="flex gap-3 text-slate-300">
                          <span className="text-purple-400 font-bold flex-shrink-0">▸</span>
                          <span>{trimmed.slice(2)}</span>
                        </div>
                      )
                    }

                    if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
                      return (
                        <p key={lineIdx} className="font-semibold text-purple-300 mt-3 mb-1">
                          {trimmed.replace(/\*\*/g, '')}
                        </p>
                      )
                    }

                    return (
                      <p key={lineIdx} className="text-slate-300 leading-relaxed text-sm">
                        {trimmed}
                      </p>
                    )
                  })}
                </div>
              </div>
            ))}

            {/* Fallback for unstructured content */}
            {!sections && (
              <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 border border-purple-700/50 rounded-xl p-8 backdrop-blur">
                <h3 className="text-xl font-bold text-white mb-6">Policy Evaluation & Comparison</h3>
                <div className="prose prose-invert max-w-none text-slate-300 text-sm leading-relaxed space-y-4">
                  {evaluation.split('\n').map((line, idx) => {
                    if (!line.trim()) return null
                    if (line.startsWith('**')) {
                      return (
                        <p key={idx} className="font-semibold text-purple-300">
                          {line.replace(/\*\*/g, '')}
                        </p>
                      )
                    }
                    return <p key={idx}>{line}</p>
                  })}
                </div>
              </div>
            )}

            {/* Sources Panel */}
            {sources.length > 0 && (
              <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
                <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                  📚 Sources & References
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {sources.map((source, idx) => (
                    <div key={idx} className="bg-slate-700/30 border border-slate-600/50 rounded-lg p-3">
                      {source.type === 'pdf' ? (
                        <>
                          <p className="text-xs font-semibold text-purple-400">PDF Document</p>
                          <p className="text-sm text-slate-300">{source.metadata.filename}</p>
                          <p className="text-xs text-slate-500">Page {source.metadata.page}</p>
                        </>
                      ) : (
                        <>
                          <p className="text-xs font-semibold text-blue-400">Web Source</p>
                          <p className="text-sm text-slate-300 truncate">{source.title}</p>
                          {source.url && <a href={source.url} target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:text-blue-300">View</a>}
                        </>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <button
              onClick={() => {
                setEvaluation(null)
                setPolicyText('')
              }}
              className="inline-flex items-center gap-2 text-purple-400 hover:text-purple-300 font-medium transition-colors"
            >
              <span>↻</span> Evaluate another policy
            </button>
          </div>
        )}

        {!evaluation && !loading && !error && !policyText && (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="text-5xl mb-4">📋</div>
            <p className="text-slate-400 font-medium">Ready to evaluate your policy</p>
            <p className="text-slate-500 text-sm mt-2">Get comprehensive analysis with comparisons to best practices and standardization recommendations</p>
          </div>
        )}
      </div>
    </div>
  )
}
