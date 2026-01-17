# GradientX System Design Book

1. AWS Free Tier Reality Check

What's Free (12 months)

| Service     | Free Tier Limit              | Our Usage       | Verdict               |
|-------------|------------------------------|-----------------|-----------------------|
| EC2         | 750 hrs/mo t2.micro          | API server      | ✅ Tight but workable |
| RDS         | 750 hrs/mo db.t2.micro, 20GB | Database        | ✅ Works for MVP      |
| S3          | 5GB storage, 20k GET, 2k PUT | File storage    | ✅ Sufficient         |
| Lambda      | 1M requests, 400k GB-sec     | Background jobs | ✅ Generous           |
| API Gateway | 1M API calls                 | REST API        | ✅ Generous           |
| DynamoDB    | 25GB, 25 read/write units    | Alternative DB  | ✅ Option             |
| CloudWatch  | 10 metrics, 5GB logs         | Monitoring      | ✅ Basic monitoring   |
| Cognito     | 50k MAU                      | Auth            | ✅ More than enough   |

What's NOT Free (Key Constraints)

| Service             | Issue             | Alternative                    |
|---------------------|-------------------|--------------------------------|
| Bedrock             | No free tier      | Self-host open-source LLM      |
| SageMaker endpoints | Expensive         | EC2 with vLLM/Ollama           |
| ElastiCache         | No free tier      | Redis on EC2 or skip initially |
| NAT Gateway         | ~$32/mo minimum   | Use public subnets for MVP     |
| ALB                 | Limited free tier | Use API Gateway or single EC2  |
| ECS Fargate         | No free tier      | Use EC2 directly               |

Revised AWS Architecture (Free Tier Optimized)

┌─────────────────────────────────────────────────────────────────┐
│              AWS FREE TIER ARCHITECTURE                          │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │    Route 53      │ ← $0.50/mo per hosted zone
                    │  (or use free    │   (or use Cloudflare free)
                    │   Cloudflare)    │
                    └────────┬─────────┘
                            │
                    ┌────────▼─────────┐
                    │   API Gateway    │ ← FREE: 1M requests/mo
                    │   (REST API)     │
                    └────────┬─────────┘
                            │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
    ┌──────────────┐ ┌────────────┐ ┌────────────┐
    │   Lambda     │ │   Lambda   │ │   Lambda   │
    │  (API Logic) │ │  (Workers) │ │  (Scheduled│
    │              │ │            │ │   Tasks)   │
    └──────────────┘ └────────────┘ └────────────┘
            │              │              │
            └──────────────┼──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   RDS Postgres  │ │       S3        │ │    DynamoDB     │
│   (db.t2.micro) │ │   (Files, UI)   │ │  (Sessions,     │
│   FREE 750hr/mo │ │   FREE 5GB      │ │   Cache)        │
└─────────────────┘ └─────────────────┘ │   FREE 25GB     │
                                        └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  LLM INFERENCE (Self-Hosted)                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Option A: EC2 t2.micro + Ollama (CPU, very slow)          ││
│  │  Option B: EC2 Spot g4dn.xlarge (~$0.16/hr when needed)    ││
│  │  Option C: External GPU (RunPod/Vast.ai ~$0.20/hr)         ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND HOSTING                                                │
│  ┌─────────────────┐                                            │
│  │  S3 + CloudFront│ ← Static Next.js export                    │
│  │  (or Vercel     │   CloudFront: 1TB free first year          │
│  │   free tier)    │   Vercel: 100GB bandwidth free             │
│  └─────────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  AUTH                          │  SECRETS                        │
│  ┌─────────────────┐          │  ┌─────────────────┐            │
│  │    Cognito      │          │  │ SSM Parameter   │            │
│  │  FREE 50k MAU   │          │  │ Store (free)    │            │
│  └─────────────────┘          │  └─────────────────┘            │
└─────────────────────────────────────────────────────────────────┘

Cost Breakdown (Free Tier + Minimal Paid)

| Component                         | Monthly Cost |
|-----------------------------------|--------------|
| AWS Free Tier services            | $0           |
| Route 53 (1 zone)                 | $0.50        |
| LLM inference (spot GPU, 20hr/mo) | ~$3-5        |
| Or: External GPU (RunPod)         | ~$5-10       |
| Total MVP                         | ~$5-15/month |

  ---
  2. Trading Sandbox Feature

  Feature Overview

  ┌─────────────────────────────────────────────────────────────────┐
  │                    TRADING SANDBOX FEATURES                      │
  ├─────────────────────────────────────────────────────────────────┤
  │                                                                 │
  │  📊 Real Market Data                                            │
  │     • Real-time/delayed stock quotes                            │
  │     • Historical price data                                     │
  │     • Market indices, sectors                                   │
  │     • Canadian + US markets                                     │
  │                                                                 │
  │  💰 Virtual Portfolio                                           │
  │     • Start with virtual cash (e.g., $100,000)                 │
  │     • Buy/sell stocks, ETFs                                     │
  │     • Track positions, P&L                                      │
  │     • Transaction history                                       │
  │                                                                 │
  │  📈 Trading Simulation                                          │
  │     • Market orders, limit orders                               │
  │     • Order book simulation                                     │
  │     • Realistic fills with slippage                            │
  │     • Trading hours enforcement                                 │
  │                                                                 │
  │  🤖 AI Analysis                                                 │
  │     • Stock analysis with reasoning                             │
  │     • Portfolio health assessment                               │
  │     • Risk analysis                                             │
  │     • "What if" scenario modeling                               │
  │     • Learning suggestions based on trades                      │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  Market Data Sources (Free/Cheap Options)

  | Provider                 | Free Tier       | Data Quality  | Best For                 |
  |--------------------------|-----------------|---------------|--------------------------|
  | Yahoo Finance (yfinance) | Unlimited*      | Good, delayed | Historical data, quotes  |
  | Alpha Vantage            | 25 req/day      | Good          | Daily data, fundamentals |
  | Finnhub                  | 60 req/min      | Good          | Real-time US stocks      |
  | Polygon.io               | 5 API calls/min | Excellent     | If you need more         |
  | IEX Cloud                | 50k msg/mo      | Excellent     | Real-time, reliable      |
  | TMX (Canadian)           | Limited         | Official      | TSX/TSX-V stocks         |

  Recommendation: Start with Yahoo Finance (yfinance) for historical + Finnhub free for real-time US. Add Alpha Vantage for fundamentals.

  Trading Sandbox Architecture

  ┌─────────────────────────────────────────────────────────────────┐
  │                 TRADING SANDBOX ARCHITECTURE                     │
  └─────────────────────────────────────────────────────────────────┘

       ┌─────────────────────────────────────────────────────────┐
       │                      FRONTEND                           │
       │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
       │  │  Portfolio  │  │   Trading   │  │    Charts   │     │
       │  │  Dashboard  │  │   Panel     │  │  (TradingView│    │
       │  │             │  │             │  │   Lightweight)│    │
       │  └─────────────┘  └─────────────┘  └─────────────┘     │
       │                         │                               │
       │  ┌─────────────────────────────────────────────────┐   │
       │  │              AI Analysis Sidebar                 │   │
       │  │  "Based on your trade, here's my analysis..."   │   │
       │  └─────────────────────────────────────────────────┘   │
       └─────────────────────────────────────────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                         API LAYER                                │
  ├─────────────────────────────────────────────────────────────────┤
  │                                                                 │
  │  /api/market                    /api/trading                    │
  │  ├── GET /quotes/:symbol        ├── POST /orders                │
  │  ├── GET /historical/:symbol    ├── GET /orders                 │
  │  ├── GET /search                ├── DELETE /orders/:id          │
  │  └── WS /stream                 └── GET /positions              │
  │                                                                 │
  │  /api/portfolio                 /api/analysis                   │
  │  ├── GET /summary               ├── POST /analyze-stock         │
  │  ├── GET /holdings              ├── POST /analyze-portfolio     │
  │  ├── GET /performance           ├── POST /analyze-trade         │
  │  └── GET /history               └── GET /insights               │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
            ▼                    ▼                    ▼
  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
  │  MARKET DATA     │ │  TRADING ENGINE  │ │  AI ANALYSIS     │
  │  SERVICE         │ │                  │ │  SERVICE         │
  │                  │ │  • Order matching│ │                  │
  │  • Data fetchers │ │  • Position mgmt │ │  • Stock analysis│
  │  • Cache layer   │ │  • P&L calc      │ │  • Risk metrics  │
  │  • Aggregation   │ │  • Trade history │ │  • Recommendations│
  │                  │ │                  │ │                  │
  └──────────────────┘ └──────────────────┘ └──────────────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 │
                                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │                        DATA LAYER                                │
  ├─────────────────────────────────────────────────────────────────┤
  │                                                                 │
  │  PostgreSQL                          Redis/DynamoDB             │
  │  ┌─────────────────────────┐        ┌─────────────────────┐    │
  │  │ • users                 │        │ • quote_cache       │    │
  │  │ • portfolios            │        │ • session_data      │    │
  │  │ • positions             │        │ • rate_limiting     │    │
  │  │ • orders                │        │                     │    │
  │  │ • transactions          │        │                     │    │
  │  │ • price_history_cache   │        │                     │    │
  │  └─────────────────────────┘        └─────────────────────┘    │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  Trading Sandbox Data Models

  ┌─────────────────────────────────────────────────────────────────┐
  │                    KEY DATA ENTITIES                             │
  └─────────────────────────────────────────────────────────────────┘

  Portfolio
  ├── id
  ├── user_id
  ├── name (e.g., "Learning Portfolio")
  ├── initial_cash: Decimal (e.g., 100000.00)
  ├── current_cash: Decimal
  ├── created_at
  └── is_active

  Position
  ├── id
  ├── portfolio_id
  ├── symbol (e.g., "AAPL", "TSX:RY")
  ├── quantity: Decimal
  ├── avg_cost_basis: Decimal
  ├── current_price: Decimal (cached)
  ├── unrealized_pnl: Decimal (computed)
  └── updated_at

  Order
  ├── id
  ├── portfolio_id
  ├── symbol
  ├── side: BUY | SELL
  ├── order_type: MARKET | LIMIT | STOP
  ├── quantity: Decimal
  ├── limit_price: Decimal (nullable)
  ├── status: PENDING | FILLED | CANCELLED | REJECTED
  ├── filled_quantity: Decimal
  ├── filled_price: Decimal
  ├── created_at
  └── executed_at

  Transaction
  ├── id
  ├── portfolio_id
  ├── order_id
  ├── symbol
  ├── side: BUY | SELL
  ├── quantity: Decimal
  ├── price: Decimal
  ├── total_value: Decimal
  ├── fees: Decimal (simulated)
  └── executed_at

  MarketDataCache
  ├── symbol
  ├── price: Decimal
  ├── change: Decimal
  ├── change_percent: Decimal
  ├── volume: BigInt
  ├── updated_at
  └── source

  AI Analysis Features for Trading

  | Analysis Type      | Input                    | AI Output                                                |
  |--------------------|--------------------------|----------------------------------------------------------|
  | Pre-trade Analysis | Symbol + intended action | Risk assessment, recent news sentiment, technical levels |
  | Post-trade Review  | Completed trade          | Was timing good? Alternatives? Learning points           |
  | Portfolio Health   | All positions            | Diversification score, sector exposure, risk metrics     |
  | What-if Scenarios  | Hypothetical trades      | Impact on portfolio, risk changes                        |
  | Daily Digest       | Portfolio + market       | Key movers affecting you, opportunities, risks           |

  ---
  3. Unified Architecture (Chatbot + Trading Sandbox)

  Combined System Design

  ┌─────────────────────────────────────────────────────────────────┐
  │                    SMARTASSET UNIFIED PLATFORM                   │
  └─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────┐
  │                         FRONTEND (Next.js)                       │
  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
  │  │  Dashboard │ │  Chatbot  │ │  Trading  │ │    Tax    │       │
  │  │           │ │           │ │  Sandbox  │ │  Center   │       │
  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
  │  ┌───────────┐ ┌───────────┐ ┌───────────┐                     │
  │  │  Budget   │ │  Expenses │ │  Settings │                     │
  │  │  Tracker  │ │  Upload   │ │           │                     │
  │  └───────────┘ └───────────┘ └───────────┘                     │
  └─────────────────────────────────────────────────────────────────┘
                                 │
                      ┌──────────┴──────────┐
                      │    API Gateway      │
                      │    + Auth (Cognito) │
                      └──────────┬──────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
          ▼                      ▼                      ▼
  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
  │   FINANCIAL  │      │   TRADING    │      │     LLM      │
  │   CORE       │      │   ENGINE     │      │   SERVICE    │
  │              │      │              │      │              │
  │ • Expenses   │      │ • Orders     │      │ • Chat       │
  │ • Budgets    │      │ • Positions  │      │ • Analysis   │
  │ • Tax calc   │      │ • Market data│      │ • Insights   │
  │ • Statements │      │ • P&L        │      │ • RAG        │
  └──────────────┘      └──────────────┘      └──────────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                      ┌──────────┴──────────┐
                      │     SHARED DATA     │
                      │                     │
                      │  PostgreSQL + S3    │
                      │  + DynamoDB cache   │
                      └─────────────────────┘

  Shared Components

  | Component           | Used By                             | Purpose              |
  |---------------------|-------------------------------------|----------------------|
  | User Profile        | All modules                         | Single user identity |
  | LLM Service         | Chatbot + Trading AI                | Unified AI interface |
  | Notification System | Budget alerts + Trade notifications | Push/email alerts    |
  | Auth Layer          | All modules                         | Cognito JWT          |
  | Analytics           | All modules                         | Usage tracking       |

  Database Schema Integration

  ┌─────────────────────────────────────────────────────────────────┐
  │                   UNIFIED DATABASE SCHEMA                        │
  └─────────────────────────────────────────────────────────────────┘

  CORE (Shared)
  ├── users
  ├── user_profiles
  ├── notifications
  └── chat_history

  FINANCIAL MODULE
  ├── bank_accounts
  ├── transactions
  ├── categories
  ├── budgets
  ├── budget_alerts
  ├── tax_profiles
  ├── tax_documents
  ├── tfsa_rrsp_tracking
  └── expense_statements

  TRADING MODULE
  ├── portfolios
  ├── positions
  ├── orders
  ├── trade_transactions
  ├── watchlists
  ├── price_alerts
  └── trade_analysis_logs

  AI/ML MODULE
  ├── embeddings
  ├── rag_documents
  ├── conversation_context
  └── user_preferences

  ---
  4. Revised Tech Stack Summary

  | Layer         | Technology                                        | Notes                        |
  |---------------|---------------------------------------------------|------------------------------|
  | Frontend      | Next.js 14 + TypeScript + TailwindCSS + shadcn/ui | SSG for performance          |
  | Charts        | TradingView Lightweight Charts (free)             | Professional trading charts  |
  | Backend       | Python FastAPI (Lambda compatible)                | ML ecosystem                 |
  | Database      | PostgreSQL (RDS free tier)                        | + pgvector when needed       |
  | Cache         | DynamoDB (free tier)                              | Replace Redis initially      |
  | Auth          | AWS Cognito                                       | 50k MAU free                 |
  | Storage       | S3                                                | Statements, documents        |
  | LLM           | Ollama + Llama 3.1 / Mistral                      | Self-hosted, CPU or spot GPU |
  | Market Data   | yfinance + Finnhub + Alpha Vantage                | Free tiers combined          |
  | Hosting       | Lambda + API Gateway OR EC2 t2.micro              | Free tier                    |
  | Frontend Host | Vercel (free) or S3 + CloudFront                  | Easiest option               |

  ---
  5. Development Phases (Revised)

  ┌─────────────────────────────────────────────────────────────────┐
  │                     DEVELOPMENT PHASES                           │
  └─────────────────────────────────────────────────────────────────┘

  PHASE 1: Foundation (MVP)
  ├── User auth (Cognito)
  ├── Basic chatbot UI
  ├── Simple LLM integration (Ollama local dev)
  ├── PostgreSQL schema
  └── Deploy to AWS free tier

  PHASE 2: Financial Core
  ├── Expense tracking (manual entry)
  ├── Budget management
  ├── Statement upload & parsing
  ├── Canadian tax calculator (TFSA/RRSP/FHSA limits)
  └── Budget alerts

  PHASE 3: AI Enhancement
  ├── RAG with financial knowledge base
  ├── Fine-tune on financial Q&A
  ├── Personalized insights
  └── Proactive suggestions

  PHASE 4: Trading Sandbox
  ├── Market data integration
  ├── Virtual portfolio system
  ├── Order execution simulation
  ├── Trading AI analysis
  └── Performance tracking

  PHASE 5: Advanced Features
  ├── Tax filing assistant
  ├── Advanced trading strategies
  ├── Mobile app (React Native)
  └── Upgrade to paid LLM (Bedrock/Claude)

  ---
  What would you like to explore next?

  1. Database schema details — Full schema for all modules
  2. API design — Endpoint specifications
  3. LLM fine-tuning strategy — Data sources, training pipeline
  4. Trading engine logic — Order matching, P&L calculations
  5. Canadian tax rules — TFSA/RRSP/FHSA contribution logic
  6. UI/UX wireframes — Screen layouts and user flows