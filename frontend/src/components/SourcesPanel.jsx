export default function SourcesPanel({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="mt-4 ml-12 p-4 bg-slate-800/50 border border-slate-700 rounded-lg">
      <p className="text-xs font-semibold text-slate-300 mb-3 flex items-center gap-2">
        <span>📚</span> Sources Referenced
      </p>
      <ul className="space-y-2">
        {sources.map((source, idx) => (
          <li key={idx} className="flex items-start gap-3 p-2 rounded hover:bg-slate-700/30 transition-colors">
            <span className="text-blue-400 text-sm flex-shrink-0 mt-0.5">→</span>
            <div className="min-w-0 flex-1">
              <p className="text-xs font-medium text-slate-200 truncate">
                {source.filename}
              </p>
              {source.page && (
                <p className="text-xs text-slate-500 mt-0.5">Page {source.page}</p>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
