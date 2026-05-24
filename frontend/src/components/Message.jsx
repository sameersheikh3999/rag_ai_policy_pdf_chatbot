export default function Message({ type, content }) {
  const isUser = type === 'user'

  return (
    <div className={`flex gap-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <span className="text-sm">🤖</span>
          </div>
        </div>
      )}

      <div
        className={`max-w-2xl rounded-xl p-4 ${
          isUser
            ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/20 ml-8'
            : 'bg-slate-800 text-slate-100 border border-slate-700 shadow-lg shadow-slate-950/50'
        }`}
      >
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
      </div>

      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center">
            <span className="text-sm">👤</span>
          </div>
        </div>
      )}
    </div>
  )
}
