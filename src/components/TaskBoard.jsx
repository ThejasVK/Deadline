import { useState } from 'react'
import TaskCard from './TaskCard'
import '../styles/TaskBoard.css'

export default function TaskBoard({ userId = 'test-user-1' }) {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Design landing page', category: 'work', priority: 'high', completed: false, status: 'in_progress', progress: 50, due_date: '2026-04-05' },
    { id: 2, title: 'Review project requirements', category: 'work', priority: 'medium', completed: false, status: 'not_started', progress: 0, due_date: '2026-04-10' },
    { id: 3, title: 'Exercise for 30 mins', category: 'health', priority: 'medium', completed: true, status: 'completed', progress: 100 },
  ])
  const [newTask, setNewTask] = useState('')
  const [filter, setFilter] = useState('all')

  const addTask = () => {
    if (newTask.trim()) {
      setTasks([
        ...tasks,
        {
          id: Date.now(),
          title: newTask,
          category: 'work',
          priority: 'medium',
          completed: false,
          status: 'not_started',
          progress: 0,
          due_date: null
        },
      ])
      setNewTask('')
    }
  }

  const toggleTask = (id) => {
    setTasks(tasks.map(task => 
      task.id === id ? { 
        ...task, 
        completed: !task.completed,
        status: !task.completed ? 'completed' : 'not_started',
        progress: !task.completed ? 100 : 0
      } : task
    ))
  }

  const deleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id))
  }

  const updateTaskStatus = (id, status, progress) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, status, progress } : task
    ))
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

        <div className="taskboard-input">
          <input
            type="text"
            placeholder="What needs to get done?"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addTask()}
            className="task-input"
          />
          <button onClick={addTask} className="btn btn-primary">
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
          {filteredTasks.length > 0 ? (
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
