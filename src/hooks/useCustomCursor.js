import { useEffect, useRef } from 'react'

export default function useCustomCursor() {
  const cursorRef = useRef(null)
  const positionRef = useRef({ x: 0, y: 0 })

  useEffect(() => {
    const cursor = cursorRef.current

    const handleMouseMove = (e) => {
      positionRef.current = { x: e.clientX, y: e.clientY }

      if (cursor) {
        cursor.style.left = `${e.clientX - 10}px`
        cursor.style.top = `${e.clientY - 10}px`
      }
    }

    const handleMouseDown = () => {
      if (cursor) {
        cursor.classList.add('big')
      }
    }

    const handleMouseUp = () => {
      if (cursor) {
        cursor.classList.remove('big')
      }
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mousedown', handleMouseDown)
    document.addEventListener('mouseup', handleMouseUp)

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mousedown', handleMouseDown)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [])

  return cursorRef
}
