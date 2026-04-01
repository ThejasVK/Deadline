// Ollama integration for AI-powered features
// This will help break down tasks and provide motivation

const OLLAMA_API_URL = import.meta.env.VITE_OLLAMA_URL || 'http://localhost:11434'
const MODEL = 'llama2' // You can change this to any model you have installed

/**
 * Break down a task into smaller subtasks using Ollama
 * @param {string} taskDescription - The main task to break down
 * @returns {Promise<string[]>} - Array of subtasks
 */
export const breakDownTask = async (taskDescription) => {
  try {
    const response = await fetch(`${OLLAMA_API_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: MODEL,
        prompt: `Break down this task into 3-5 smaller, actionable subtasks. Task: "${taskDescription}". 
        
        Format your response as a numbered list with just the subtasks, no extra text.`,
        stream: false,
        temperature: 0.7,
      }),
    })

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`)
    }

    const data = await response.json()
    const subtasks = data.response
      .split('\n')
      .filter(line => line.trim().match(/^\d+\./))
      .map(line => line.replace(/^\d+\.\s*/, '').trim())

    return subtasks.length > 0 ? subtasks : [taskDescription]
  } catch (error) {
    console.error('Error breaking down task:', error)
    // Fallback: return the original task if API fails
    return [taskDescription]
  }
}

/**
 * Get motivation/encouragement from Ollama
 * @param {string} taskTitle - The task to get motivation for
 * @returns {Promise<string>} - Motivational message
 */
export const getMotivation = async (taskTitle) => {
  try {
    const response = await fetch(`${OLLAMA_API_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: MODEL,
        prompt: `Give a short, punchy motivational message for someone feeling lazy about doing this task: "${taskTitle}". 
        Keep it to one sentence, be funny but genuine. Don't be preachy.`,
        stream: false,
        temperature: 0.8,
      }),
    })

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`)
    }

    const data = await response.json()
    return data.response.trim()
  } catch (error) {
    console.error('Error getting motivation:', error)
    return "You've got this! Just start with the first small step. 💪"
  }
}

/**
 * Generate a task completion reminder
 * @param {string} taskTitle - The task that needs a reminder
 * @returns {Promise<string>} - Reminder message
 */
export const generateReminder = async (taskTitle) => {
  try {
    const response = await fetch(`${OLLAMA_API_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: MODEL,
        prompt: `Create a gentle but firm reminder for someone to complete this task: "${taskTitle}". 
        Make it personal, understanding that they might be procrastinating. One sentence.`,
        stream: false,
        temperature: 0.7,
      }),
    })

    if (!response.ok) {
      throw new Error(`Ollama API error: ${response.statusText}`)
    }

    const data = await response.json()
    return data.response.trim()
  } catch (error) {
    console.error('Error generating reminder:', error)
    return `Don't forget: ${taskTitle} is still waiting for you!`
  }
}

export const checkOllamaConnection = async () => {
  try {
    const response = await fetch(`${OLLAMA_API_URL}/api/tags`)
    return response.ok
  } catch {
    return false
  }
}
