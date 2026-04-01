/**
 * Backend API Client
 * Communicates with Python FastAPI backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

console.log(`🔗 API URL: ${API_URL}`)

/**
 * Get all tasks for a user
 */
export const getTasks = async (userId) => {
  try {
    const response = await fetch(`${API_URL}/api/tasks/?user_id=${userId}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ GET /api/tasks/ - Response:', data)
    return data.data || []
  } catch (error) {
    console.error('❌ Error fetching tasks:', error)
    throw error
  }
}

/**
 * Create a new task
 */
export const addTask = async (task) => {
  try {
    const params = new URLSearchParams({
      user_id: task.user_id,
      title: task.title,
      description: task.description || '',
      priority: task.priority || 'medium',
      category: task.category || 'work'
    })
    
    const response = await fetch(`${API_URL}/api/tasks/?${params.toString()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ POST /api/tasks/ - Response:', data)
    return data.data || data
  } catch (error) {
    console.error('❌ Error adding task:', error)
    throw error
  }
}

/**
 * Update an existing task
 */
export const updateTask = async (taskId, updates) => {
  try {
    const params = new URLSearchParams()
    
    if (updates.title !== undefined) params.append('title', updates.title)
    if (updates.description !== undefined) params.append('description', updates.description)
    if (updates.priority !== undefined) params.append('priority', updates.priority)
    if (updates.completed !== undefined) params.append('completed', updates.completed)
    if (updates.category !== undefined) params.append('category', updates.category)
    if (updates.status !== undefined) params.append('status', updates.status)
    if (updates.progress !== undefined) params.append('progress', updates.progress)
    
    const response = await fetch(`${API_URL}/api/tasks/${taskId}?${params.toString()}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ PUT /api/tasks/:id - Response:', data)
    return data.data || data
  } catch (error) {
    console.error('❌ Error updating task:', error)
    throw error
  }
}

/**
 * Delete a task
 */
export const deleteTask = async (taskId) => {
  try {
    const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ DELETE /api/tasks/:id - Response:', data)
    return data
  } catch (error) {
    console.error('❌ Error deleting task:', error)
    throw error
  }
}

/**
 * Get task statistics
 */
export const getTaskStats = async (userId) => {
  try {
    const response = await fetch(`${API_URL}/api/tasks/stats/${userId}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ GET /api/tasks/stats/:id - Response:', data)
    return data.data || data
  } catch (error) {
    console.error('❌ Error fetching stats:', error)
    throw error
  }
}

/**
 * AI: Break down a task
 */
export const breakDownTask = async (taskTitle) => {
  try {
    const response = await fetch(`${API_URL}/api/ai/break-down`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ task_title: taskTitle })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ POST /api/ai/break-down - Response:', data)
    return data
  } catch (error) {
    console.error('❌ Error breaking down task:', error)
    throw error
  }
}

/**
 * AI: Get motivation
 */
export const getMotivation = async (taskTitle) => {
  try {
    const response = await fetch(`${API_URL}/api/ai/motivation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ task_title: taskTitle })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('✅ POST /api/ai/motivation - Response:', data)
    return data
  } catch (error) {
    console.error('❌ Error getting motivation:', error)
    throw error
  }
}
