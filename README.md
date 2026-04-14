# 🏥 SmartQueue Hospital — AI Queue Management System

A complete hospital queue management system with **Gemini AI** integration.

## ✅ Features
- Patient register / login / profile edit
- AI Symptom Checker (Gemini AI)
- MediBot AI Health Chat (Gemini AI)
- Token generation & queue tracking
- Appointment booking & management
- Doctor dashboard with AI queue insights
- Doctor can add medical records
- Token history for patients
- Search & filter doctors
- Admin panel (manage doctors & patients)
- Live IoT-style display board
- Fully responsive (mobile + tablet + desktop)
- Error pages (404 / 500)
- Auto-rotating Gemini API keys

---

## 🚀 Run Locally

```bash
pip install flask
python app.py
```

Open: http://127.0.0.1:5000

---

## 🌐 Deploy to Render (Free)

1. Push this folder to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Click Deploy

---

## 🔑 Login Credentials

| Role    | Email / Username         | Password    |
|---------|--------------------------|-------------|
| Admin   | admin                    | admin123    |
| Doctor  | anil@hospital.com        | doctor123   |
| Doctor  | priya@hospital.com       | doctor123   |
| Doctor  | rahul@hospital.com       | doctor123   |
| Doctor  | sunita@hospital.com      | doctor123   |
| Doctor  | vikram@hospital.com      | doctor123   |
| Patient | rajesh1@gmail.com        | patient123  |

---

## 🤖 Gemini API Keys

Edit `app.py` line ~10 to add your keys:

```python
GEMINI_KEYS = [
    "YOUR_KEY_1",
    "YOUR_KEY_2",   # Add more for higher quota
]
```

Get free keys at: https://aistudio.google.com/apikey

---

## 📁 Project Structure

```
smartqueue/
├── app.py                  # Main Flask app
├── requirements.txt        # Dependencies
├── Procfile                # For Render/Railway deploy
├── runtime.txt             # Python version
├── static/
│   └── style.css           # Responsive CSS
└── templates/
    ├── base.html           # Shared layout + mobile nav
    ├── home.html
    ├── patient_register.html
    ├── patient_login.html
    ├── patient_dashboard.html
    ├── patient_profile.html
    ├── patient_chat.html
    ├── symptom_checker.html
    ├── book_appointment.html
    ├── doctor_login.html
    ├── doctor_register.html
    ├── doctor_dashboard.html
    ├── add_record.html
    ├── admin_login.html
    ├── admin_dashboard.html
    ├── display.html
    ├── 404.html
    └── 500.html
```
