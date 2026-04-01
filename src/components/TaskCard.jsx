import { Trash2, CheckCircle2, Circle } from 'lucide-react'
import '../styles/TaskCard.css'

export default function TaskCard({ task, onToggle, onDelete }) {
  return (
    <div className={`task-card ${task.completed ? 'completed' : ''}`}>
      <div className="task-content">
        <button
          className="task-checkbox"
          onClick={() => onToggle(task.id)}
          aria-label="Toggle task"
        >
          {task.completed ? (
            <CheckCircle2 size={24} color="var(--lime)" />
          ) : (
            <Circle size={24} color="var(--lime)" />
          )}
        </button>
        <div className="task-info">
          <h3 className="task-title">{task.title}</h3>
          <div className="task-meta">
            <span className={`priority priority-${task.priority}`}>
              {task.priority}
            </span>
            <span className="category">{task.category}</span>
          </div>
        </div>
      </div>
      <button
        className="task-delete"
        onClick={() => onDelete(task.id)}
        aria-label="Delete task"
      >
        <Trash2 size={20} />
      </button>
    </div>
  )
}
