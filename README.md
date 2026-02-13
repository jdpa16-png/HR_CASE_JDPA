# 🤖 Happy Robot: Logistics Analytics Dashboard

A full-stack logistics monitoring solution that tracks carrier negotiations, success rates, and financial efficiency in real-time.

## 🏗️ Architecture
* **Frontend**: React + Vite + Tailwind CSS + Recharts.
* **Backend**: FastAPI + SQLModel (SQLAlchemy).
* **Database**: PostgreSQL (Hosted on Railway).
* **Security**: Global API Key Authentication & HTTPS.

## 🚀 Live Deployment
* **Dashboard**: https://fde-happyrobbot-production-ff33.up.railway.app/
* **API Documentation**: https://fde-happyrobbot-production.up.railway.app/docs
  
## 🛠️ Reproduction Steps
1. **Database**: Create a PostgreSQL instance on Railway.
2. **Backend**:
   - Set environment variables: `DATABASE_URL`, `INTERNAL_API_KEY`.
   - Deploy via Railway (builds automatically from Dockerfile/Nixpack).
3. **Frontend**:
   - Set environment variables: `VITE_API_URL` (include https://), `VITE_INTERNAL_API_KEY`.
   - Deploy via Railway.
