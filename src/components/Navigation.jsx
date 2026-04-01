import { useState } from 'react'
import '../styles/Navigation.css'

export default function Navigation({ onManagerClick }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1 className="brand-text">DOIT.</h1>
        </div>
        
        <button 
          className="hamburger" 
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`navbar-menu ${isOpen ? 'active' : ''}`}>
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How It Works</a></li>
          <li>
            <button 
              onClick={onManagerClick}
              className="btn btn-lime"
              style={{ marginTop: 0 }}
            >
              👔 Manager Mode
            </button>
          </li>
          <li><button className="btn btn-primary">Get Started</button></li>
        </ul>
      </div>
    </nav>
  )
}
