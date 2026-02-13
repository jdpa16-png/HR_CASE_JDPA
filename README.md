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

---
## 🔄 How to Reproduce Your Deployment on Railway
### Step 1: Clone the Repository
If you haven't already cloned your repository, do so now:
```bash
git clone [https://github.com/jdpa16-png/PRUEBA_JDPA.git](https://github.com/jdpa16-png/HR_CASE_JDPA.git)
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
