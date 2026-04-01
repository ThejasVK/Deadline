import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY

if (!supabaseUrl || !supabaseKey) {
  console.warn('Supabase credentials not configured')
}

export const supabase = createClient(supabaseUrl || '', supabaseKey || '')

// Helper functions for common operations
export const getTasks = async (userId) => {
  try {
    const { data, error } = await supabase
      .from('tasks')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    return data
  } catch (error) {
    console.error('Error fetching tasks:', error)
    return []
  }
}

export const addTask = async (userId, task) => {
  try {
    const { data, error } = await supabase
      .from('tasks')
      .insert([{ ...task, user_id: userId }])
      .select()
    
    if (error) throw error
    return data[0]
  } catch (error) {
    console.error('Error adding task:', error)
    return null
  }
}

export const updateTask = async (taskId, updates) => {
  try {
    const { data, error } = await supabase
      .from('tasks')
      .update(updates)
      .eq('id', taskId)
      .select()
    
    if (error) throw error
    return data[0]
  } catch (error) {
    console.error('Error updating task:', error)
    return null
  }
}

export const deleteTask = async (taskId) => {
  try {
    const { error } = await supabase
      .from('tasks')
      .delete()
      .eq('id', taskId)
    
    if (error) throw error
    return true
  } catch (error) {
    console.error('Error deleting task:', error)
    return false
  }
}
