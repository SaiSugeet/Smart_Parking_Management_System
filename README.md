# 🅿️ Smart Parking Management System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

<p align="center">
  <b>A real-time, web-based parking management solution built with Python and Streamlit.</b><br/>
  Handles vehicle entry, space tracking, automated billing, and QR-coded receipts — all from a clean browser interface.
</p>

---

## 📌 Overview

Manual parking management is inefficient — staff errors, no real-time visibility, and paper receipts that get lost. This system replaces that with a lightweight, interactive web app that any attendant can use from a browser.

**Smart Parking Management System** enables parking lot operators to:
- Register and track vehicles in real time
- Monitor available slots for two-wheelers and four-wheelers separately
- Automatically calculate parking charges with 18% GST
- Generate scannable QR code receipts on the spot

Built as part of an internship project to demonstrate full-cycle software development: from requirement analysis to a deployable, production-style web application.

---

## 🧠 Features

- **Vehicle Registration** — Validates Indian vehicle number format (e.g. `KA-08-AS-2345`) before entry
- **Dual Vehicle Type Support** — Independent slot tracking for two-wheelers (100 slots) and four-wheelers (200 slots)
- **Live Space Dashboard** — Sidebar shows real-time slot availability with color-coded status (green / orange / red)
- **Smart Billing Engine** — Computes hourly charges + 18% GST automatically
- **QR Code Receipt** — Generates a scannable QR code encoding the full receipt details; downloadable as PNG
- **Search & Filter** — Filter parked vehicles by number plate or owner name
- **Session Reset** — One-click reset to clear all records for a new shift
- **Responsive Layout** — Works on desktop and tablet browsers

---

## 🏗️ How It Works

```
User Action (Browser)
        │
        ▼
  Streamlit Frontend
  ┌─────────────────────────────────────────────┐
  │  Tab 1: Vehicle Entry  → Validates & stores │
  │  Tab 2: Remove Vehicle → Frees up slot      │
  │  Tab 3: View Records   → Searchable table   │
  │  Tab 4: Generate Bill  → Calculates & QR    │
  └─────────────────────────────────────────────┘
        │
        ▼
  st.session_state (in-memory store)
  ┌────────────────────────────────┐
  │  vehicles[]  — active records  │
  │  tw_used     — slots occupied  │
  │  fw_used     — slots occupied  │
  └────────────────────────────────┘
        │
        ▼
  QR Code Generator (qrcode + Pillow)
  → Encodes receipt text → Renders inline via st.image()
  → Downloadable as PNG
```

All data lives in Streamlit's `session_state` — no external database required. The app is fully self-contained and stateless across sessions, making it trivially deployable.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend / UI** | Streamlit 1.32+ |
| **Language** | Python 3.10+ |
| **QR Generation** | `qrcode[pil]` |
| **Image Processing** | Pillow (PIL) |
| **Data Display** | Pandas |
| **Deployment** | Streamlit Community Cloud |

---

## 📊 System Capacity & Metrics

| Metric | Value |
|--------|-------|
| Two-Wheeler Slots | 100 |
| Four-Wheeler Slots | 200 |
| Two-Wheeler Rate | ₹30 / hour |
| Four-Wheeler Rate | ₹60 / hour |
| GST Applied | 18% |
| Max Billing Duration | 720 hours |
| Vehicle No. Validation | Indian RTO format regex |
| QR Code Generation | < 1 second (approx.) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- `pip` package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SaiSugeet/Smart_Parking_Management_System.git
cd Smart_Parking_Management_System

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 🌐 Deployment

### Local

Follow the installation steps above. The app runs entirely locally — no external services or API keys required.

### Streamlit Community Cloud (Free)

1. Push the repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New app** → select your repository
4. Set **Main file path** to `app.py`
5. Click **Deploy** — your app will be live in ~2 minutes

> No server configuration needed. Streamlit Cloud handles everything.

---

## 📂 Project Structure

```
Smart_Parking_Management_System/
│
├── app.py              # Main Streamlit application (entry point)
├── park.py             # Original CLI version (v1 — reference only)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable reference (capacity, rates)
└── README.md           # Project documentation
```

---

## 🎯 Use Cases

- **Shopping mall / plaza parking lots** — Attendant-operated entry/exit desk
- **Office building parking** — Employee vehicle tracking by shift
- **Events & venues** — Temporary parking with instant billing
- **College campus parking** — Low-cost, no-infrastructure solution

---

## 📌 Future Improvements

- [ ] **Persistent Storage** — SQLite or Firebase integration so data survives restarts
- [ ] **Authentication** — Admin login to protect billing and reset functions
- [ ] **Export Reports** — Download daily/monthly records as CSV or PDF
- [ ] **Entry Timestamp Auto-Billing** — Calculate charges automatically from entry time
- [ ] **License Plate Recognition** — Camera-based auto-entry using OpenCV
- [ ] **Multi-Floor Support** — Track slots across multiple parking levels

---

## 🤝 Contributing

Contributions are welcome. To contribute:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# Open a Pull Request
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with Python & Streamlit &nbsp;|&nbsp; 
  <a href="https://github.com/SaiSugeet/Smart_Parking_Management_System">GitHub</a>
</p>
