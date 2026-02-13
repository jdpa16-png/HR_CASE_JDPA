# 📊 Happy Robot - Frontend

The command center for logistics data, featuring interactive charts and a detailed call log table.

## ✨ Key Features
* **Dual-Axis Evolution Chart**: Tracks total load volume vs. success rate percentage.
* **Origin Success Matrix**: Vertical bar chart showing performance by city.
* **Live Call Table**: Searchable and sortable logs directly from the database.
* **Dynamic KPIs**: Real-time calculation of success rate and rate efficiency.

## ⚙️ Environment Variables
Create a `.env` file in the root of the frontend folder:
```env
VITE_API_URL=[https://your-backend-url.up.railway.app](https://your-backend-url.up.railway.app)
VITE_INTERNAL_API_KEY=your_secret_key
