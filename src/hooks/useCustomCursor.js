import { useEffect, useRef } from 'react'

export default function useCustomCursor() {
  const cursorRef = useRef(null)

  useEffect(() => {
    const cursor = cursorRef.current
    
    if (!cursor) {
      console.error('❌ Cursor element not found')
      return
    }

    console.log('✅ Custom cursor hook initialized')
    
    // Make cursor visible immediately
    cursor.style.display = 'block'
    cursor.style.opacity = '1'
    cursor.style.visibility = 'visible'

    const moveCursor = (e) => {
      const x = e.clientX - 12 // 12 = half of 24px size
      const y = e.clientY - 12
      
      cursor.style.left = x + 'px'
      cursor.style.top = y + 'px'
      cursor.style.opacity = '1'
    }

    const makeClickBigger = () => {
      cursor.style.transform = 'scale(2)'
    }

    const makeClickSmallAgain = () => {
      cursor.style.transform = 'scale(1)'
    }

    // Use capture phase for immediate response
    document.addEventListener('mousemove', moveCursor, true)
    document.addEventListener('mousedown', makeClickBigger, true)
    document.addEventListener('mouseup', makeClickSmallAgain, true)

    // Hide cursor when leaving window
    const hideOnLeave = () => {
      cursor.style.opacity = '0'
    }

    const showOnEnter = () => {
      cursor.style.opacity = '1'
    }

    document.addEventListener('mouseleave', hideOnLeave, true)
    document.addEventListener('mouseenter', showOnEnter, true)

    return () => {
      document.removeEventListener('mousemove', moveCursor, true)
      document.removeEventListener('mousedown', makeClickBigger, true)
      document.removeEventListener('mouseup', makeClickSmallAgain, true)
      document.removeEventListener('mouseleave', hideOnLeave, true)
      document.removeEventListener('mouseenter', showOnEnter, true)
    }
  }, [])

  return cursorRef
}
