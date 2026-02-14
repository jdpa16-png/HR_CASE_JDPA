# ⚙️ Happy Robot: Backend API Instance
The Happy Robot Backend is a high-performance REST API built with FastAPI and SQLModel. It serves as the bridge between raw logistics call extractions and the PostgreSQL database, ensuring data integrity through strict type validation and secure authentication.

## 🚀 Key Features
- **Global Security Middleware**: Implements a mandatory `verify_api_key` dependency across all sensitive endpoints, requiring a valid `x-api-key` header for access.
- **Relational Data Modeling**: Utilizes **SQLModel** to define a unified schema for both API validation (Pydantic) and database persistence (SQLAlchemy), reducing code redundancy and potential schema drift.
- **Performance Optimized Ingestion**: Supports both individual and bulk ingestion of call logs to handle high-volume data streams from multiple extraction sources.
- **Real-Time Analytics Engine**: Features specialized endpoints that perform on-the-fly aggregations for KPIs like Success Rate and Rate Efficiency Ratio.
- **Automated Data Sanitization**: Includes a logic layer that intercepts string-based flags (e.g., "true", "1", "yes") from the frontend and casts them into native PostgreSQL `BOOLEAN` types to ensure 100% accuracy in success rate calculations.
  

## 🛠️ Tech Stack

| Tool | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance Python framework for building APIs with auto-generated docs. |
| **ORM** | [SQLModel](https://sqlmodel.tiangolo.com/) | Combines SQLAlchemy and Pydantic for type-safe database interactions. |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Relational database for persistent storage, hosted on Railway. |
| **Security** | [API Key Auth](https://fastapi.tiangolo.com/tutorial/dependencies/setting-up-dependencies/) | Dependency-based security layer for endpoint protection. |
| **Deployment** | [Railway](https://railway.app/) | Infrastructure-as-code platform for cloud deployment and CI/CD. |

## 🏗️ Project Structure
```text
backend/
├── 📁 .venv/               # Virtual environment for local development
├── 📁 data/               # Persistent data storage / Local DB files
├── 📁 src/
│   ├── 🐍 __init__.py      # Python package initializer
│   ├── 🐍 main.py          # FastAPI entry point & security middleware
│   ├── 🐍 models.py        # SQLModel schemas for database tab
│   └── 🐍 utils.py         # Helper functions for data sanitization
├── 🐳 Dockerfile           # Production container configuration
├── ⚙️ pyproject.toml       # Python project metadata and dependencies
└── 📄 uv.lock              # Fast, reproducible dependency lockfile
```

## 🔒 Security Implementation

The system implements a multi-layer security approach to protect sensitive logistics data.

* **API Key Protection:** All sensitive backend endpoints are protected via a custom dependency that validates a mandatory x-api-key header.

* **Encrypted Transit:** In production, the application is served exclusively over HTTPS, with SSL/TLS termination managed by the Railway platform.

* **Environment Isolation:** Sensitive credentials (database strings and API keys) are never hardcoded and are managed strictly through environment varia*bles.

* **CORS Policy:** The backend is configured with CORSMiddleware to strictly limit cross-origin requests to only authorized frontend domains.


 ## ⚙️ Environment Variables
```
# PostgreSQL connection string
DATABASE_URL=postgresql://user:pass@host:port/db
# Secret key for backend authentication
INTERNAL_API_KEY=your_secret_key_here
```


## 🚀 Backend Local Setup

1. Install and Configure Environment Variable
2. Synchronize Dependencies with uv:
3. Run the Uvicorn Server:
* Execute this command to start the server. Note that we point to src.main:app because your main.py is inside the src folder.
