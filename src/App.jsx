import { useState, useEffect } from 'react'
import Hero from './components/Hero'
import TaskBoard from './components/TaskBoard'
import Navigation from './components/Navigation'

function App() {
  const [isClient, setIsClient] = useState(false)
  const userId = 'test-user-1'

  useEffect(() => {
    setIsClient(true)
  }, [])

  if (!isClient) return null

  return (
    <div className="app">
      <Navigation />
      <Hero />
      <TaskBoard userId={userId} />
    </div>
  )
}

export default App
