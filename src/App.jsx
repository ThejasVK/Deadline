import { useState, useEffect } from 'react'
import Hero from './components/Hero'
import TaskBoard from './components/TaskBoard'
import Navigation from './components/Navigation'
import Manager from './components/Manager'
import LogsViewer from './components/LogsViewer'
import useCustomCursor from './hooks/useCustomCursor'
import { logger } from './utils/logger'

function App() {
  const [isClient, setIsClient] = useState(false)
  const [showManager, setShowManager] = useState(false)
  const cursorRef = useCustomCursor()
  const userId = 'test-user-1' // TODO: Replace with actual user ID from auth

  useEffect(() => {
    setIsClient(true)
    logger.info('App initialized', { userId })
  }, [])

  if (!isClient) return null

  return (
    <div className="app">
      <div ref={cursorRef} className="cursor"></div>
      <Navigation onManagerClick={() => {
        setShowManager(!showManager)
        logger.logAction('TOGGLE_MANAGER', 'Navigation', { showManager: !showManager })
      }} />
      <Hero />
      {showManager ? <Manager userId={userId} /> : <TaskBoard userId={userId} />}
      <LogsViewer />
    </div>
  )
}

export default App
