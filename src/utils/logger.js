/**
 * Frontend logging system for DOIT
 * Logs all user actions and sends them to backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class Logger {
  constructor() {
    this.logs = []
    this.sendToBackend = true
  }

  /**
   * Format timestamp
   */
  getTimestamp() {
    const now = new Date()
    return now.toISOString().split('T').join(' ').split('.')[0]
  }

  /**
   * Log info level
   */
  info(message, data = {}) {
    const log = {
      timestamp: this.getTimestamp(),
      level: 'INFO',
      message,
      data,
      source: 'FRONTEND'
    }
    this.logs.push(log)
    console.log(`[${log.timestamp}] INFO | ${message}`, data)
    return log
  }

  /**
   * Log error level
   */
  error(message, error = null, data = {}) {
    const log = {
      timestamp: this.getTimestamp(),
      level: 'ERROR',
      message,
      error: error ? error.toString() : null,
      data,
      source: 'FRONTEND'
    }
    this.logs.push(log)
    console.error(`[${log.timestamp}] ERROR | ${message}`, error, data)
    return log
  }

  /**
   * Log warning level
   */
  warning(message, data = {}) {
    const log = {
      timestamp: this.getTimestamp(),
      level: 'WARNING',
      message,
      data,
      source: 'FRONTEND'
    }
    this.logs.push(log)
    console.warn(`[${log.timestamp}] WARNING | ${message}`, data)
    return log
  }

  /**
   * Log user actions (clicks, form submissions, etc)
   */
  logAction(action, component, details = {}) {
    const log = {
      timestamp: this.getTimestamp(),
      level: 'ACTION',
      message: `USER ACTION`,
      action,
      component,
      details,
      source: 'FRONTEND'
    }
    this.logs.push(log)
    console.log(`[${log.timestamp}] ACTION | ${action} in ${component}`, details)
    return log
  }

  /**
   * Log API calls
   */
  logAPI(method, endpoint, data = {}, response = null) {
    const log = {
      timestamp: this.getTimestamp(),
      level: 'API',
      message: `API CALL`,
      method,
      endpoint,
      data,
      response,
      source: 'FRONTEND'
    }
    this.logs.push(log)
    console.log(`[${log.timestamp}] API | ${method} ${endpoint}`, { data, response })
    return log
  }

  /**
   * Log navigation
   */
  logNavigation(from, to) {
    const log = {
      timestamp: this.getTimestamp(),
      level: 'NAVIGATION',
      message: `PAGE NAVIGATION`,
      from,
      to,
      source: 'FRONTEND'
    }
    this.logs.push(log)
    console.log(`[${log.timestamp}] NAVIGATION | ${from} → ${to}`)
    return log
  }

  /**
   * Get all logs
   */
  getLogs() {
    return this.logs
  }

  /**
   * Get last N logs
   */
  getLastLogs(n = 50) {
    return this.logs.slice(-n)
  }

  /**
   * Export logs as JSON
   */
  exportJSON() {
    return JSON.stringify(this.logs, null, 2)
  }

  /**
   * Export logs as CSV
   */
  exportCSV() {
    const headers = ['Timestamp', 'Level', 'Message', 'Data']
    const rows = this.logs.map(log => [
      log.timestamp,
      log.level,
      log.message,
      JSON.stringify(log.data)
    ])
    
    const csv = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n')
    
    return csv
  }

  /**
   * Download logs file
   */
  downloadLogs(format = 'json') {
    const content = format === 'json' ? this.exportJSON() : this.exportCSV()
    const filename = `doit-logs-${new Date().toISOString().split('T')[0]}.${format}`
    
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    this.info(`Logs downloaded`, { format, filename })
  }

  /**
   * Clear logs
   */
  clearLogs() {
    this.logs = []
    console.log('Logs cleared')
  }

  /**
   * Send logs to backend for server-side storage (optional)
   */
  async sendToBackendServer() {
    if (!this.sendToBackend || this.logs.length === 0) return
    
    try {
      const response = await fetch(`${API_URL}/api/logs/frontend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ logs: this.logs })
      })
      
      if (response.ok) {
        this.info('Logs sent to backend successfully')
      }
    } catch (error) {
      this.error('Failed to send logs to backend', error)
    }
  }

  /**
   * Get size of logs in memory
   */
  getSize() {
    const json = JSON.stringify(this.logs)
    return (new Blob([json]).size / 1024).toFixed(2) // KB
  }
}

// Create singleton instance
export const logger = new Logger()

// Export for use in components
export default logger
