import { useState, useEffect } from 'react'
import { logger } from '@/utils/logger'
import '@/styles/LogsViewer.css'

export default function LogsViewer() {
  const [logs, setLogs] = useState([])
  const [filter, setFilter] = useState('all')
  const [isOpen, setIsOpen] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    const interval = autoRefresh ? setInterval(() => {
      setLogs([...logger.getLogs()])
    }, 1000) : null

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [autoRefresh])

  const filteredLogs = filter === 'all' 
    ? logs 
    : logs.filter(log => log.level === filter)

  const downloadLogs = (format) => {
    logger.downloadLogs(format)
  }

  const clearLogs = () => {
    if (confirm('Clear all logs? This cannot be undone.')) {
      logger.clearLogs()
      setLogs([])
    }
  }

  if (!isOpen) {
    return (
      <button 
        className="logs-toggle-btn"
        onClick={() => setIsOpen(true)}
        title="Open Logs Viewer"
      >
        📋 Logs ({logs.length})
      </button>
    )
  }

  return (
    <div className="logs-viewer">
      <div className="logs-header">
        <h3>📋 Logs Viewer</h3>
        <button className="logs-close-btn" onClick={() => setIsOpen(false)}>✕</button>
      </div>

      <div className="logs-toolbar">
        <div className="logs-info">
          Total: {logs.length} | Size: {logger.getSize()}KB
        </div>

        <div className="logs-controls">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="logs-filter"
          >
            <option value="all">All Logs</option>
            <option value="INFO">Info</option>
            <option value="ACTION">Actions</option>
            <option value="API">API Calls</option>
            <option value="ERROR">Errors</option>
            <option value="WARNING">Warnings</option>
          </select>

          <label className="logs-auto-refresh">
            <input 
              type="checkbox" 
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
            />
            Auto-refresh
          </label>

          <button 
            className="logs-download-btn"
            onClick={() => downloadLogs('json')}
            title="Download as JSON"
          >
            ⬇️ JSON
          </button>

          <button 
            className="logs-download-btn"
            onClick={() => downloadLogs('csv')}
            title="Download as CSV"
          >
            ⬇️ CSV
          </button>

          <button 
            className="logs-clear-btn"
            onClick={clearLogs}
            title="Clear all logs"
          >
            🗑️ Clear
          </button>
        </div>
      </div>

      <div className="logs-content">
        {filteredLogs.length === 0 ? (
          <div className="logs-empty">No logs to display</div>
        ) : (
          filteredLogs.map((log, idx) => (
            <div key={idx} className={`log-entry log-${log.level.toLowerCase()}`}>
              <span className="log-time">{log.timestamp}</span>
              <span className="log-level">{log.level}</span>
              <span className="log-message">{log.message}</span>
              {log.action && <span className="log-action">{log.action}</span>}
              {log.component && <span className="log-component">{log.component}</span>}
              {Object.keys(log.data).length > 0 && (
                <span className="log-data">{JSON.stringify(log.data)}</span>
              )}
            </div>
          ))
        )}
      </div>

      <div className="logs-footer">
        <small>Showing {filteredLogs.length} of {logs.length} logs</small>
      </div>
    </div>
  )
}
