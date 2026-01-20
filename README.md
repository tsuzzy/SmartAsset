# SmartAsset

AI-powered financial advisor chatbot for users under Canadian tax system. Get personalized guidance on budgeting, taxes, TFSA, RRSP, and more.

## Features

- **AI Chat Assistant** - Natural language conversations about personal finance
- **Canadian Tax Guidance** - TFSA, RRSP, FHSA contribution limits and strategies
- **Budget Planning** - Personalized budgeting advice and expense tracking
- **Secure Authentication** - JWT-based auth with session management

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, TypeScript, TailwindCSS |
| Backend | FastAPI, Python 3.12 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| LLM | Ollama (local) with mock fallback |
| Auth | JWT (local) / AWS Cognito (prod) |

## Project Structure

```
SmartAsset/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # REST API endpoints
│   │   ├── core/           # Config, database, security
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic (LLM service)
│   ├── tests/
│   └── requirements.txt
│
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── hooks/             # Custom hooks (auth)
│   ├── lib/               # Utilities & API client
│   └── types/             # TypeScript types
│
├── docker-compose.yml
└── system_design.md       # Architecture documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- (Optional) [Ollama](https://ollama.ai/) for local LLM

### Option 1: Local Development

**Backend**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run server
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local

# Run dev server
npm run dev
```

### Option 2: Docker

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d
```

### Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/chat/sessions` | List chat sessions |
| POST | `/api/v1/chat/sessions` | Create new session |
| GET | `/api/v1/chat/sessions/{id}` | Get session with messages |
| PATCH | `/api/v1/chat/sessions/{id}` | Update session title |
| DELETE | `/api/v1/chat/sessions/{id}` | Delete session |
| POST | `/api/v1/chat/send` | Send message and get response |
| POST | `/api/v1/chat/send/stream` | Send message with streaming |

## Configuration

### Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./smartasset.db` |
| `SECRET_KEY` | JWT signing key | (required in production) |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | LLM model to use | `llama3.2` |
| `LLM_MOCK_MODE` | Use mock responses | `false` |

### Frontend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## Using Ollama

For AI responses, install and run Ollama:

```bash
# Install Ollama (macOS)
brew install ollama

# Pull a model
ollama pull llama3.2

# Run Ollama server
ollama serve
```

If Ollama is not available, the app falls back to mock responses for development.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
