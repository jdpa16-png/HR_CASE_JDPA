# 📊 Happy Robot - Frontend Dashboard

The Happy Robot Frontend is a high-performance React application built with Vite. It provides real-time visibility into carrier negotiations by transforming raw API data into actionable logistics intelligence.

## ✨ Key Features
**1. Real-Time Analytics Dashboard**
* **Dynamic KPIs**: Instant calculation of Success Rates, Total Closed Deals, and Negotiation Efficiency.
* **Evolution Chart**: A dual-axis line/area chart (using Recharts) that tracks:
  * *Left Axis*: Total Load Volume (Line).
  * *Right Axis*: Success Percentage (Line).
* **Origin Success Matrix**: Diagram chart showing performance by city.

**2. Data Integrity & Security**
*  ***API Key Interceptor***: Uses Axios interceptors to automatically attach the ```x-api-key``` to every outgoing request.
*  ***Environment Parity***: Configured to switch between local development and production Railway environments seamlessly.

**3. Interactive Log Explorer**
*  A searchable and sortable table of all call extractions.
*  **Visual Tags***: Sentiment and deal status are color-coded (Green for success, Red for failure) to allow for quick auditing.

---
## 🛠️ Tech Stack

| Tool | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance Python framework for building APIs with auto-generated docs. |
| **ORM** | [SQLModel](https://sqlmodel.tiangolo.com/) | Combines SQLAlchemy and Pydantic for type-safe database interactions. |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Relational database for persistent storage, hosted on Railway. |
| **Security** | [API Key Auth](https://fastapi.tiangolo.com/tutorial/dependencies/setting-up-dependencies/) | Dependency-based security layer for endpoint protection. |
| **Deployment** | [Railway](https://railway.app/) | Infrastructure-as-code platform for cloud deployment and CI/CD. |

---
## 🏗️ Project Structure

```text
frontend/
├── 📁 src/
│   ├── 📁 components/      # Reusable UI (Charts, KPI Cards, Log Tables)
│   ├── ⚛️ App.jsx          # Main orchestrator: fetches data & manages state
│   ├── 🎨 index.css        # Global styles & Tailwind CSS directives
│   └── 🚀 main.jsx         # Application entry point
├── 📁 node_modules/        # Project dependencies (ignored by Git)
├── 📄 .gitignore           # Specifies files to exclude from version control
├── 🐳 dockerfile           # Container configuration for production parity
├── 🛠️ eslint.config.js     # JavaScript linting & code quality rules
├── 🌐 index.html           # Main HTML document
├── 📦 package-lock.json    # Deterministic dependency tree
├── 📦 package.json         # Project metadata, scripts, and dependencies
├── 📖 README.md            # Frontend documentation
└── ⚙️ vite.config.js       # Vite build & environment configuration
```
---
## ⚙️ Environment Variables
Create a `.env` file in the root of the frontend folder:
```env
# Production URL from Railway
VITE_API_URL=https://fde-happyrobbot-production.up.railway.app
# Security key matching the backend
VITE_INTERNAL_API_KEY=your_secret_api_key
```
---
## 🚀 Local Development
*  Navigate to the directory:
```
cd frontend
```
*  Install dependencies:
```
npm install
```
*  Start the development server:
```
npm run dev
```
* Access the UI:
  Open ```http://localhost:5173``` in your browser.
