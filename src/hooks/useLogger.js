import { useEffect } from 'react'
import { logger } from '@/utils/logger'

/**
 * Hook to log component mount/unmount
 */
export function useLogger(componentName) {
  useEffect(() => {
    logger.logAction('COMPONENT_MOUNT', componentName)
    
    return () => {
      logger.logAction('COMPONENT_UNMOUNT', componentName)
    }
  }, [componentName])
}

/**
 * Hook to log user actions
 */
export function useLogAction(action, component, data = {}) {
  return () => {
    logger.logAction(action, component, data)
  }
}

/**
 * Hook to log API calls
 */
export function useLogAPI(method, endpoint) {
  return (data = {}, response = null) => {
    logger.logAPI(method, endpoint, data, response)
  }
}
