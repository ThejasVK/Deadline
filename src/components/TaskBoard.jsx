import { useState, useEffect } from 'react'
import TaskCard from './TaskCard'
import { getTasks, addTask as apiAddTask, updateTask as apiUpdateTask, deleteTask as apiDeleteTask } from '../utils/api'
import '../styles/TaskBoard.css'

const USER_ID = 'test-user-1' // In production, get from auth

export default function TaskBoard({ userId = USER_ID }) {
  const [tasks, setTasks] = useState([])
  const [newTask, setNewTask] = useState('')
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasksFromBackend()
  }, [])

  const fetchTasksFromBackend = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await getTasks(userId)
      console.log('📦 Tasks fetched from backend:', response)
      setTasks(response)
    } catch (err) {
      console.error('❌ Error fetching tasks:', err)
      setError('Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  const addTask = async () => {
    if (newTask.trim()) {
      try {
        const newTaskObj = {
          user_id: userId,
          title: newTask,
          category: 'work',
          priority: 'medium',
          completed: false,
          status: 'not_started',
          progress: 0,
          due_date: null
        }
        const result = await apiAddTask(newTaskObj)
        console.log('✅ Task added:', result)
        setTasks([...tasks, result])
        setNewTask('')
      } catch (err) {
        console.error('❌ Error adding task:', err)
        setError('Failed to add task')
      }
    }
  }

  const toggleTask = async (id) => {
    const task = tasks.find(t => t.id === id)
    if (task) {
      try {
        const updatedTask = {
          completed: !task.completed,
          status: !task.completed ? 'completed' : 'not_started',
          progress: !task.completed ? 100 : 0
        }
        await apiUpdateTask(id, updatedTask)
        console.log('✅ Task toggled:', id)
        
        // Refetch tasks to ensure we have latest state from backend
        const refreshedTasks = await getTasks('test-user-1')
        setTasks(refreshedTasks)
      } catch (err) {
        console.error('❌ Error toggling task:', err)
        setError('Failed to update task')
      }
    }
  }

  const deleteTask = async (id) => {
    try {
      await apiDeleteTask(id)
      console.log('✅ Task deleted:', id)
      // Refetch tasks to ensure consistency
      const refreshedTasks = await getTasks('test-user-1')
      setTasks(refreshedTasks)
    } catch (err) {
      console.error('❌ Error deleting task:', err)
      setError('Failed to delete task')
    }
  }

  const updateTaskStatus = async (id, status, progress) => {
    try {
      await apiUpdateTask(id, { status, progress })
      console.log('✅ Task status updated:', id)
      // Refetch tasks to ensure consistency
      const refreshedTasks = await getTasks('test-user-1')
      setTasks(refreshedTasks)
    } catch (err) {
      console.error('❌ Error updating task status:', err)
      setError('Failed to update task status')
    }
  }

  const filteredTasks = filter === 'all' 
    ? tasks 
    : filter === 'completed' 
    ? tasks.filter(t => t.completed)
    : tasks.filter(t => !t.completed)

  return (
    <section className="taskboard" id="features">
      <div className="container">
        <div className="taskboard-header">
          <h2 className="h2">Your Tasks</h2>
          <p className="subtitle">Tackle your to-do list with AI-powered breakdowns</p>
        </div>

        {error && <div className="error-banner">⚠️ {error}</div>}
        {loading && <div className="loading-banner">⏳ Loading tasks...</div>}

        <div className="taskboard-input">
          <input
            type="text"
            placeholder="What needs to get done?"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTask()}
            className="task-input"
            disabled={loading}
          />
          <button onClick={addTask} className="btn btn-primary" disabled={loading}>
            Add Task
          </button>
        </div>

        <div className="taskboard-filters">
          {['all', 'active', 'completed'].map(f => (
            <button
              key={f}
              className={`filter-btn ${filter === f ? 'active' : ''}`}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)} ({
                f === 'all' ? tasks.length :
                f === 'completed' ? tasks.filter(t => t.completed).length :
                tasks.filter(t => !t.completed).length
              })
            </button>
          ))}
        </div>

        <div className="tasks-grid">
          {loading ? (
            <div className="empty-state">
              <p>⏳ Loading your tasks...</p>
            </div>
          ) : filteredTasks.length > 0 ? (
            filteredTasks.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onToggle={toggleTask}
                onDelete={deleteTask}
                onStatusChange={updateTaskStatus}
              />
            ))
          ) : (
            <div className="empty-state">
              <p>No {filter === 'all' ? 'tasks' : filter} tasks. You're all caught up! 🎉</p>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}
