import '../styles/Hero.css'

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-left">
        <span className="hero-tag">Accountability Powered by AI</span>
        <h1 className="hero-title">
          Stop <span className="scratch">procrastinating</span>.
          <br />
          Start <span className="accent">doing</span>.
        </h1>
        <p className="hero-description">
          Get AI-powered accountability reminders, task breakdowns, and motivation 
          delivered exactly when you need them. Built for people who procrastinate.
        </p>
        <div className="hero-cta">
          <button className="btn btn-primary">Start Free</button>
          <button className="btn btn-secondary">Watch Demo</button>
        </div>
      </div>
      <div className="hero-right">
        <div className="hero-illustration">
          <div className="illustration-box accent"></div>
          <div className="illustration-box pink"></div>
          <div className="illustration-box blue"></div>
        </div>
      </div>
    </section>
  )
}
