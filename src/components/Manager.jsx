import { useState, useEffect } from 'react'
import { AlertCircle, Clock, CheckCircle2, AlertTriangle } from 'lucide-react'
import '../styles/Manager.css'

export default function Manager({ userId }) {
  const [managerView, setManagerView] = useState(null)
  const [warnings, setWarnings] = useState([])
  const [standup, setStandup] = useState('')
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')

  const API_URL = 'http://localhost:8000'

  useEffect(() => {
    fetchManagerData()
    // Refresh every 30 minutes
    const interval = setInterval(fetchManagerData, 30 * 60 * 1000)
    return () => clearInterval(interval)
  }, [userId])

  const fetchManagerData = async () => {
    setLoading(true)
    try {
      // Get manager overview
      const viewRes = await fetch(`${API_URL}/api/manager/tasks/${userId}`)
      const viewData = await viewRes.json()
      setManagerView(viewData.data)

      // Get warnings
      const warningRes = await fetch(`${API_URL}/api/manager/warnings/${userId}`)
      const warningData = await warningRes.json()
      setWarnings(warningData.warnings || [])

      // Get standup
      const standupRes = await fetch(`${API_URL}/api/manager/weekly-standup/${userId}`)
      const standupData = await standupRes.json()
      setStandup(standupData.standup)
    } catch (error) {
      console.error('Error fetching manager data:', error)
    }
    setLoading(false)
  }

  const fetchProgressReport = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/api/manager/progress-report/${userId}`)
      const data = await res.json()
      setReport(data.data)
    } catch (error) {
      console.error('Error fetching report:', error)
    }
    setLoading(false)
  }

  if (!managerView) {
    return <div className="manager-loading">📊 Loading manager dashboard...</div>
  }

  const stats = managerView.stats

  return (
    <section className="manager">
      <div className="container">
        {/* Manager Header */}
        <div className="manager-header">
          <h2 className="h2">👔 Manager Mode</h2>
          <p className="subtitle">Your AI manager tracks progress and keeps you accountable</p>
        </div>

        {/* Stats Cards */}
        <div className="manager-stats">
          <div className="stat-card total">
            <div className="stat-number">{stats.total}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
          <div className="stat-card completed">
            <div className="stat-number">{stats.completed}</div>
            <div className="stat-label">Completed</div>
          </div>
          <div className="stat-card in-progress">
            <div className="stat-number">{stats.in_progress}</div>
            <div className="stat-label">In Progress</div>
          </div>
          <div className="stat-card blocked">
            <div className="stat-number">{stats.blocked}</div>
            <div className="stat-label">Blocked</div>
          </div>
          {stats.overdue > 0 && (
            <div className="stat-card overdue">
              <div className="stat-number">{stats.overdue}</div>
              <div className="stat-label">Overdue! ⚠️</div>
            </div>
          )}
        </div>

        {/* Standup Message */}
        {standup && (
          <div className="standup-message">
            <div className="standup-icon">🎯</div>
            <div className="standup-text">
              <h3>Weekly Standup</h3>
              <p>{standup}</p>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="manager-tabs">
          <button
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            📋 Overview
          </button>
          <button
            className={`tab ${activeTab === 'warnings' ? 'active' : ''}`}
            onClick={() => setActiveTab('warnings')}
          >
            ⏰ Deadlines ({warnings.length})
          </button>
          <button
            className={`tab ${activeTab === 'report' ? 'active' : ''}`}
            onClick={() => {
              setActiveTab('report')
              if (!report) fetchProgressReport()
            }}
          >
            📊 Report
          </button>
        </div>

        {/* Tab Content */}
        <div className="manager-content">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="overview-section">
              {managerView.overdue.length > 0 && (
                <TaskGroup
                  title="🚨 OVERDUE - URGENT!"
                  tasks={managerView.overdue}
                  urgent={true}
                />
              )}

              {managerView.due_soon.length > 0 && (
                <TaskGroup
                  title="⏰ Due Soon (Next 3 Days)"
                  tasks={managerView.due_soon}
                  urgent={false}
                />
              )}

              {managerView.in_progress.length > 0 && (
                <TaskGroup
                  title="🔄 In Progress"
                  tasks={managerView.in_progress}
                  urgent={false}
                />
              )}

              {managerView.blocked.length > 0 && (
                <TaskGroup
                  title="🚫 Blocked - Need Help"
                  tasks={managerView.blocked}
                  urgent={true}
                />
              )}

              {managerView.completed.length > 0 && (
                <TaskGroup
                  title="✅ Completed - Great Work!"
                  tasks={managerView.completed}
                  completed={true}
                />
              )}
            </div>
          )}

          {/* Warnings Tab */}
          {activeTab === 'warnings' && (
            <div className="warnings-section">
              {warnings.length === 0 ? (
                <div className="empty-state">
                  <p>✨ No urgent deadlines! You're on track. Great job!</p>
                </div>
              ) : (
                warnings.map((warning) => (
                  <div key={warning.task_id} className="warning-card">
                    <div className={`warning-severity ${warning.is_overdue ? 'overdue' : 'urgent'}`}>
                      {warning.is_overdue ? '🚨' : '⏰'}
                    </div>
                    <div className="warning-details">
                      <h4>{warning.task_title}</h4>
                      <p className="days-remaining">
                        {warning.is_overdue
                          ? `${Math.abs(warning.days_remaining)} days overdue`
                          : `${warning.days_remaining} days left`}
                      </p>
                      <p className="warning-message">"{warning.warning}"</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Report Tab */}
          {activeTab === 'report' && (
            <div className="report-section">
              {!report ? (
                <button onClick={fetchProgressReport} className="btn btn-primary" disabled={loading}>
                  {loading ? 'Generating...' : 'Generate Report'}
                </button>
              ) : (
                <div className="report-card">
                  <h3>📊 Progress Report</h3>
                  <div className="report-stats">
                    <div className="stat">
                      <span>Total</span>
                      <strong>{report.stats.total_tasks}</strong>
                    </div>
                    <div className="stat">
                      <span>Completed</span>
                      <strong>{report.stats.completed}</strong>
                    </div>
                    <div className="stat">
                      <span>In Progress</span>
                      <strong>{report.stats.in_progress}</strong>
                    </div>
                    <div className="stat">
                      <span>Rate</span>
                      <strong>{report.stats.completion_rate}</strong>
                    </div>
                  </div>
                  <div className="report-text">
                    <p>{report.report}</p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Refresh Button */}
        <div className="manager-actions">
          <button
            onClick={fetchManagerData}
            className="btn btn-secondary"
            disabled={loading}
          >
            {loading ? '⏳ Refreshing...' : '🔄 Refresh'}
          </button>
        </div>
      </div>
    </section>
  )
}

// Task Group Component
function TaskGroup({ title, tasks, urgent = false, completed = false }) {
  return (
    <div className={`task-group ${urgent ? 'urgent' : ''} ${completed ? 'completed' : ''}`}>
      <h3 className="group-title">{title}</h3>
      <div className="tasks-list">
        {tasks.map((task) => (
          <div key={task.id} className="manager-task-item">
            <div className="task-icon">
              {completed ? '✅' : urgent ? '⚠️' : '📌'}
            </div>
            <div className="task-details">
              <h4>{task.title}</h4>
              <div className="task-info">
                <span className={`priority ${task.priority}`}>{task.priority}</span>
                <span className="progress">{task.progress}% done</span>
                {task.due_date && (
                  <span className="due-date">
                    📅 {new Date(task.due_date).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
