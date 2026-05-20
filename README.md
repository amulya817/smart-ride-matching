# 🚗 Smart Ride Matching

A smart ride-matching platform with AI-powered driver matching, real-time route optimization, fare calculation, and emergency SOS — built with Python (Streamlit) and React.

---

## 🌟 Features

- 🤖 **AI-Powered Driver Matching** — Intelligent matching engine using optimized algorithms
- 🗺️ **Live Route Map** — Real-time route visualization with Dijkstra's algorithm
- 💰 **Fare Engine** — Dynamic fare calculation based on distance and demand
- 🚨 **Emergency SOS** — One-click SOS alert system for rider safety
- 👤 **Driver Registration & Dashboard** — Full driver onboarding and management
- 📋 **Booking History** — Track all past and current rides
- 🛡️ **Admin Dashboard** — Platform-wide monitoring and control
- 🔐 **Authentication** — Secure login for riders and drivers

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend (Web) | React + Vite + TailwindCSS |
| Frontend (App) | Python Streamlit |
| Backend | Node.js + Express |
| AI / Algorithms | Python (Dijkstra, Matching Engine, GenAI) |
| Data | CSV-based storage |

---

## 📁 Project Structure

```
smart-ride-matching/
├── backend/                  # Node.js Express backend
│   ├── server.js
│   └── package.json
├── smart_ride_matching/      # Python Streamlit app
│   ├── app.py                # Main app entry point
│   ├── algorithms/           # Core matching & routing algorithms
│   ├── pages/                # Streamlit pages
│   ├── genai/                # AI/GenAI integration
│   ├── simulation/           # Driver & rider simulators
│   ├── config/               # App configuration
│   ├── data/                 # CSV data files
│   └── web-frontend/         # React web frontend
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm

---

### 1. Clone the repository
```bash
git clone https://github.com/amulya817/smart-ride-matching.git
cd smart-ride-matching
```

---

### 2. Run the Python Streamlit App

```bash
cd smart_ride_matching
pip install -r requirements.txt
streamlit run app.py
```

---

### 3. Run the Node.js Backend

```bash
cd backend
npm install
node server.js
```

---

### 4. Run the React Web Frontend

```bash
cd smart_ride_matching/web-frontend
npm install
npm run dev
```

---

## 📸 Pages & Modules

| Page | Description |
|------|-------------|
| 🏠 Home | Landing page with login |
| 🚗 Book Ride | Ride booking with smart matching |
| 🗺️ Live Route Map | Real-time route visualization |
| 🚨 Emergency SOS | Safety alert system |
| 📋 Booking History | Past ride records |
| 🧑‍✈️ Driver Registration | Onboard new drivers |
| 📊 Driver Dashboard | Driver stats and management |
| 👤 Profile | User profile management |
| 🛡️ Admin Dashboard | Admin control panel |

---

## 👩‍💻 Author

**Amulya B**  
📧 amulyabkrishna@gmail.com  
🔗 [GitHub](https://github.com/amulya817)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
