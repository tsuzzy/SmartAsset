# SmartAsset Documentation

## Overview

SmartAsset is an AI-powered asset management platform that provides comprehensive portfolio analysis, investment recommendations, and financial insights using advanced machine learning and natural language processing.

## Features

- **Portfolio Management**: Create and manage investment portfolios
- **Asset Tracking**: Track stocks, bonds, ETFs, and other financial instruments
- **AI-Powered Analysis**: Get intelligent insights and recommendations
- **Risk Assessment**: Comprehensive risk analysis and metrics
- **Performance Tracking**: Monitor portfolio performance over time

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
Currently, authentication is placeholder. Future versions will include JWT-based authentication.

### Endpoints

#### Assets
- `GET /assets/` - Get all assets
- `GET /assets/{asset_id}` - Get specific asset
- `POST /assets/` - Create new asset
- `PUT /assets/{asset_id}` - Update asset
- `DELETE /assets/{asset_id}` - Delete asset

#### Portfolios
- `GET /portfolios/` - Get all portfolios
- `GET /portfolios/{portfolio_id}` - Get specific portfolio
- `POST /portfolios/` - Create new portfolio
- `PUT /portfolios/{portfolio_id}` - Update portfolio
- `DELETE /portfolios/{portfolio_id}` - Delete portfolio
- `GET /portfolios/{portfolio_id}/performance` - Get portfolio performance

#### Analysis
- `POST /analysis/portfolio` - Analyze portfolio with AI
- `POST /analysis/asset` - Analyze specific asset
- `POST /analysis/recommendations` - Get investment recommendations
- `GET /analysis/market-sentiment` - Get market sentiment

## Development

### Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (copy `env.example` to `.env`)
4. Run database migrations: `alembic upgrade head`
5. Start the development server: `uvicorn app.main:app --reload`

### Testing

Run tests with pytest:
```bash
pytest
```

### Code Quality

Format code with black:
```bash
black app/ tests/
```

Check types with mypy:
```bash
mypy app/
```

## Architecture

The application follows a clean architecture pattern:

- **API Layer**: FastAPI endpoints and request/response handling
- **Service Layer**: Business logic and AI integration
- **Model Layer**: Database models and data access
- **Schema Layer**: Pydantic models for validation

## Database Schema

### Assets
- Basic asset information (name, symbol, type)
- Financial metrics (price, P/E ratio, beta, etc.)
- Market data (volume, market cap, etc.)

### Portfolios
- Portfolio metadata and settings
- Risk tolerance and investment goals
- Performance tracking

### Portfolio Assets
- Asset holdings within portfolios
- Quantity and cost basis
- Allocation percentages

### Transactions
- Buy/sell transactions
- Dividend payments
- Cash deposits/withdrawals

## AI Integration

The platform integrates with OpenAI's GPT models through LangChain for:

- Portfolio analysis and insights
- Investment recommendations
- Market sentiment analysis
- Risk assessment

## Deployment

### Docker

Build and run with Docker Compose:
```bash
docker-compose up --build
```

### Production

For production deployment:
1. Set appropriate environment variables
2. Use a production database (PostgreSQL)
3. Configure proper logging
4. Set up monitoring and alerting
5. Use a reverse proxy (nginx)
6. Enable HTTPS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 