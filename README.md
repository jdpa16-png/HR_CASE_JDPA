# 🤖 Happy Robot: Logistics Analytics Dashboard

A full-stack logistics monitoring solution that tracks carrier negotiations, success rates, and financial efficiency in real-time.

## 🏗️ Architecture & Stack

The project is architected into three distinct instances for scalability and separation of concerns:

- **Frontend Instance**: React + Vite + Tailwind CSS + Recharts. 
- **Backend Instance**: FastAPI + SQLModel (SQLAlchemy).
- **Database Instance (BBDD)**: PostgreSQL for persistent, structured storage.
- **Security**: 
    - **Global API Key Authentication**: Every endpoint is protected via a mandatory `x-api-key` header.
    - **HTTPS**: Managed SSL termination provided by Railway.
    - **Data Sanitization**: Backend logic converts incoming frontend strings to native Boolean bits.


## 🚀 Live Deployment
* **Dashboard**: https://fde-happyrobbot-production-ff33.up.railway.app/
* **API Documentation**: https://fde-happyrobbot-production.up.railway.app/docs

## 🔄 How to Reproduce Locally (Docker)

To spin up all three instances (Front, End, and BBDD) locally with a single command:

1. **Ensure Docker and Docker Compose are installed.**
2. **Create ```.Env``` file is created with this variables** ```(INTERNAL_API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DATABASE_URL, VITE_INTERNAL_API_KEY, VITE_API_URL)```
4. **Run the build command:**
   ```bash
   docker-compose up --build
   ```
5. **Access the services:**
 - **Frontend**: ```http://localhost:80``` (Note that in case you dont add any post-call extraction the display will be: *Data loaded but summary is missing. Check backend*. In order to post one do it through -> *```POST Log_call_extraction```*
 - **Backend API**: ```http://localhost:8000/docs```
## ☁️ How to Reproduce Your Deployment on Railway
### Phase 1: Railway Infrastructure
1.- Create a New Project: In Railway, create an empty project.

2.- Add PostgreSQL: Click New → Database → Add PostgreSQL.

3.- Deploy Backend:
* Add a new service from your GitHub repo.
* **Crucial**: Go to Settings → General → Root Directory and set it to /backend.
* Set *Start Command*: python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT
    
4.- Deploy Frontend:
* Add another service from the same GitHub repo.
* **Crucial**: Go to Settings → General → Root Directory and set it to /frontend.
    
### Phase 2: ⚙️ Environment Variables (The "Handshake")
Explain that the services need to "talk" to each other via these variables:
* *Backend*
    * ```DATABASE_URL -> ${{PostgreSQL.DATABASE_URL}}```
    * ```INTERNAL_API_KEY -> Generated secret for security```
* *Frontend*
    * ```VITE_API_URL -> ${{Backend.RAILWAY_STATIC_URL}}```
