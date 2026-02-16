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

---

## 🚀 Live Deployment
* **Dashboard**: https://fde-happyrobbot-production-ff33.up.railway.app/
* **API Documentation**: https://fde-happyrobbot-production.up.railway.app/docs

---
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
 - **Backend API**: ```http://localhost:8000```
---
## ☁️ How to Reproduce Your Deployment on Railway
### Step 1: Clone the Repository
If you haven't already cloned your repository, do so now:
```bash
git clone https://github.com/jdpa16-png/HR_CASE_JDPA.git
cd HR_CASE_JDPA
```

### Step 2: Install Railway CLI
To deploy and manage your project on Railway, you'll need to install the Railway CLI.

Using cURL (for macOS/Linux):
Run the following command to download and install the Railway CLI:
 ```bash
bash <(curl -fsSL cli.new)
```
Using Homebrew (macOS/Linux):
```bash
brew install railway
```

### Step 3: Initialize a New Railway Project
To initialize a new project with Railway, run:
```bash
railway init
```
This will:
* Ask you for a project name and setup details.
* Create a configuration file in your project directory.

### Step 4: Link to an Existing Railway Project
If you’ve already created a project on Railway and want to link your local project, use:
``` bash
railway link
```

### Step 5: Deploy Your App
Once your project is set up and linked, you can deploy it with:
``` bash
railway up
```
 ---
### ⚙️ Configuration & Customization
If your app requires environment variables, set them in the Railway dashboard:
   1. Select your project and go to Settings > Variables.
   2. Add the following required variables:
      * ```DATABASE_URL```: Connection string for your PostgreSQL instance.
      * ```INTERNAL_API_KEY```: Secret key used for API authentication.
      * ```VITE_API_URL```: Full URL of your backend (e.g., https://backend.up.railway.app).
      * ```VITE_INTERNAL_API_KEY```: Matches INTERNAL_API_KEY for frontend requests.
