# SmartAsset - AI-Powered Asset Management Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

SmartAsset is a comprehensive AI-powered asset management platform that provides intelligent portfolio analysis, investment recommendations, and financial insights using advanced machine learning and natural language processing.

## 🚀 Features

- **Portfolio Management**: Create and manage investment portfolios with real-time tracking
- **Asset Tracking**: Monitor stocks, bonds, ETFs, cryptocurrencies, and other financial instruments
- **AI-Powered Analysis**: Get intelligent insights and recommendations using OpenAI's GPT models
- **Risk Assessment**: Comprehensive risk analysis with advanced metrics (Sharpe ratio, VaR, etc.)
- **Performance Tracking**: Monitor portfolio performance with detailed analytics
- **Market Sentiment**: AI-driven market sentiment analysis
- **RESTful API**: Clean, well-documented API for integration

## 🏗️ Architecture

The application follows a clean, scalable architecture:

```
SmartAsset/
├── app/                    # Main application
│   ├── api/               # API endpoints
│   ├── core/              # Core configuration
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Utility scripts
└── alembic/               # Database migrations
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: OpenAI GPT, LangChain
- **Financial Analysis**: PyPortfolioOpt, Pandas, NumPy
- **Testing**: Pytest, TestClient
- **Deployment**: Docker, Docker Compose
- **Code Quality**: Black, MyPy, Flake8

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Docker (optional, for containerized deployment)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smartasset.git
   cd smartasset
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   python scripts/setup_db.py
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual services
docker-compose up db
docker-compose up api
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Key Endpoints

#### Assets
- `GET /assets/` - List all assets
- `GET /assets/{id}` - Get asset details
- `POST /assets/` - Create new asset
- `PUT /assets/{id}` - Update asset
- `DELETE /assets/{id}` - Delete asset

#### Portfolios
- `GET /portfolios/` - List all portfolios
- `GET /portfolios/{id}` - Get portfolio details
- `POST /portfolios/` - Create new portfolio
- `GET /portfolios/{id}/performance` - Get performance metrics

#### Analysis
- `POST /analysis/portfolio` - AI portfolio analysis
- `POST /analysis/asset` - AI asset analysis
- `POST /analysis/recommendations` - Investment recommendations
- `GET /analysis/market-sentiment` - Market sentiment

### Example Usage

```python
import requests

# Create an asset
asset_data = {
    "name": "Apple Inc.",
    "symbol": "AAPL",
    "asset_type": "stock",
    "current_price": 150.0,
    "currency": "USD"
}

response = requests.post("http://localhost:8000/api/v1/assets/", json=asset_data)
print(response.json())

# Analyze portfolio
analysis_request = {
    "portfolio_id": 1,
    "analysis_type": "comprehensive"
}

response = requests.post("http://localhost:8000/api/v1/analysis/portfolio", json=analysis_request)
print(response.json())
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_assets.py

# Run with verbose output
pytest -v
```

## 🔧 Development

### Code Quality

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Type checking
mypy app/

# Linting
flake8 app/ tests/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## 📊 Database Schema

### Core Tables

- **assets**: Financial instruments (stocks, bonds, ETFs, etc.)
- **portfolios**: Investment portfolios
- **portfolio_assets**: Asset holdings within portfolios
- **transactions**: Buy/sell transactions and cash flows

### Key Features

- Comprehensive asset metadata
- Portfolio performance tracking
- Transaction history
- Risk metrics calculation
- AI analysis results storage

## 🤖 AI Integration

SmartAsset leverages OpenAI's GPT models through LangChain for:

- **Portfolio Analysis**: Intelligent insights and recommendations
- **Risk Assessment**: AI-driven risk evaluation
- **Market Sentiment**: Real-time sentiment analysis
- **Investment Recommendations**: Personalized investment advice

## 🚀 Deployment

### Production Checklist

- [ ] Set production environment variables
- [ ] Configure production database
- [ ] Set up proper logging
- [ ] Configure reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key

# Optional
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [OpenAI](https://openai.com/) for AI capabilities
- [LangChain](https://langchain.com/) for AI integration
- [PyPortfolioOpt](https://pyportfolioopt.readthedocs.io/) for portfolio optimization

## 📞 Support

- **Documentation**: [docs/README.md](docs/README.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/smartasset/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/smartasset/discussions)

---

**SmartAsset** - Making intelligent investment decisions accessible to everyone.
