# 🚗 Smart Parking Management System

A **Python + Flask-based Parking Management System** with **QR Code Receipts**.  
This project simulates a real-world parking lot billing system where vehicles can be added, removed, billed, and their receipts accessed via QR codes.  

When a bill is generated, a **QR code** is created and displayed. Scanning it opens a styled **receipt page** (Bootstrap-based) in the browser — even on a mobile phone.

---

## ✨ Features
- 🔹 Vehicle entry & removal
- 🔹 Tracks available parking slots
- 🔹 Billing with **auto-calculated charges + 18% GST**
- 🔹 **QR Code receipts** (scannable to open on mobile)
- 🔹 Live **Flask web server** serving digital receipts
- 🔹 Optionally accessible from any network using **ngrok**
- 🔹 Responsive **Bootstrap-styled GUI** for receipts

---

## 🛠 Tech Stack
- **Python 3**  
- **Flask** (backend web server)  
- **qrcode + Pillow** (QR code generation)  
- **pyngrok** (for public access without deployment)  
- **Bootstrap 5** (for clean receipt UI)

---
