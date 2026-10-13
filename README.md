# DOIT. - Get Unstuck

A productivity app built for people who procrastinate. Get AI-powered accountability, task breakdowns, and motivation delivered exactly when you need them.

## Tech Stack

- **Frontend**: React + Vite
- **Backend**: Python FastAPI (task CRUD, AI and "manager mode" routes), SQLAlchemy on PostgreSQL
- **AI**: Groq-hosted LLM for task breakdowns, motivation and reminders (Ollama supported for local runs)
- **Logging**: structured request and AI-call logs with a viewer in the app

## How it works

1. You add a task you've been putting off.
2. The AI breaks it into small, concrete next steps.
3. "Manager mode" checks progress, flags tasks going stale, and asks for an update, like a manager who actually helps.

## Docs

Setup and design notes live in [`docs/`](docs/): [getting started](docs/GETTING_STARTED.md), [backend setup](docs/BACKEND_SETUP.md), [Postgres setup](docs/POSTGRES_SETUP.md), [manager mode architecture](docs/MANAGER_ARCHITECTURE.md), [logging](docs/LOGGING_GUIDE.md).

## Project Structure

```
doit/
├── src/
│   ├── components/          # React components
│   │   ├── Hero.jsx
│   │   ├── Navigation.jsx
│   │   ├── TaskBoard.jsx
│   │   └── TaskCard.jsx
│   ├── pages/              # Page components (future)
│   ├── styles/             # CSS files
│   │   ├── index.css       # Global styles
│   │   ├── Hero.css
│   │   ├── Navigation.css
│   │   ├── TaskBoard.css
│   │   └── TaskCard.css
│   ├── utils/              # Utility functions
│   │   ├── supabase.js     # Supabase client & helpers
│   │   └── ollama.js       # Ollama AI integration
│   ├── App.jsx             # Main App component
│   └── main.jsx            # React entry point
├── index.html              # HTML template
├── vite.config.js          # Vite configuration
├── package.json            # Dependencies
├── .env.local              # Local environment variables
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn
- Ollama installed and running (for AI features)
- Supabase account (free tier works)

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Set up environment variables**
   - Copy `.env.example` to `.env.local`
   - Add your Supabase URL and key
   - Add your Ollama URL (default: `http://localhost:11434`)
   ```bash
   cp .env.example .env.local
   ```

3. **Start Ollama** (optional, for AI features)
   ```bash
   ollama serve
   ```
   Then in another terminal:
   ```bash
   ollama pull llama2  # or another model
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```
   Opens at `http://localhost:3000`

## Features (Planned)

- ✅ Task management UI
- ⏳ Supabase integration
- ⏳ AI task breakdown (Ollama)
- ⏳ Motivation reminders
- ⏳ Progress tracking
- ⏳ User authentication
- ⏳ Mobile app

## Development Workflow

This project is built step-by-step. Each feature will be added gradually.

### Current Step
1. Basic UI structure with React + Vite ✅
2. Task board component ✅
3. Connect to Supabase (next)
4. Integrate Ollama for AI features
5. Add authentication
6. Deploy to Vercel

## Color Palette

- **Lime**: `#C8F135` - Primary accent
- **Black**: `#0e0e0e` - Background
- **White**: `#f5f2ea` - Text
- **Pink**: `#FF4D8D` - Accent
- **Orange**: `#FF6B2B` - Accent
- **Blue**: `#1E3AFF` - Accent
- **Yellow**: `#FFE500` - Accent
- **Purple**: `#7B2FBE` - Accent

## Typography

- **Headlines**: Bebas Neue
- **Body**: Instrument Serif
- **UI**: Space Mono

## Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## Next Steps

1. Set up Supabase database schema
2. Create authentication pages (login/signup)
3. Integrate Ollama task breakdown
4. Add user profile page
5. Set up deployment on Vercel

## Resources

- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [Supabase Docs](https://supabase.com/docs)
- [Ollama Docs](https://ollama.ai)
- [Vercel Docs](https://vercel.com/docs)

## License

MIT

---

**Built by someone who knows the pain of procrastination.** 🚀
