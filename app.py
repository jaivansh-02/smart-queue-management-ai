# ═══════════════════════════════════════════════════════════════════════════════
#  SmartQueue Hospital — app.py
#  Complete unified IST time system — single source of truth
# ═══════════════════════════════════════════════════════════════════════════════
from dotenv import load_dotenv
import os

load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3, hashlib, json, random, os, time, secrets, re, base64, threading
import smtplib, urllib.request, urllib.error, urllib.parse
from groq import Groq
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone
from translations import LANGUAGES, RTL_LANGUAGES, TRANSLATIONS, t, get_lang

# ═══════════════════════════════════════════════════════════════════════════════
#  ████████╗██╗███╗   ███╗███████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
#  ╚══██╔══╝██║████╗ ████║██╔════╝    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
#     ██║   ██║██╔████╔██║█████╗      ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
#     ██║   ██║██║╚██╔╝██║██╔══╝      ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
#     ██║   ██║██║ ╚═╝ ██║███████╗    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
#  ═══════════════════════════════════════════════════════════════════════════════
#
#  DESIGN RULES (NEVER BREAK THESE):
#
#  1. IST = UTC+5:30.  We use stdlib timezone — no pytz, no zoneinfo import needed.
#
#  2. now_ist()        → ALWAYS use this for "current time". Never datetime.now().
#
#  3. ist_str_now()    → IST string "2026-03-22 22:30:15" to store in DB created_at.
#                        NEVER rely on SQLite CURRENT_TIMESTAMP (it stores UTC).
#
#  4. parse_ist_str(s) → Read a DB-stored IST string back to an aware datetime.
#                        Use ONLY this to parse created_at from DB.
#                        DO NOT call .replace(tzinfo=IST) on a UTC value.
#
#  5. fmt_dt(dt)       → Format any aware datetime → human "22 Mar 2026, 10:30 PM IST".
#                        All strings shown to user MUST come from this ONE function.
#
#  6. calc_meeting_time(appointment_date_str, wait_mins)
#                      → THE ONLY place that computes estimated meeting time.
#                        Formula: appointment_date at 09:00 AM IST + (wait_mins)
#                        This ensures: after-hours token on 22nd → meeting on 23rd at 9:XX AM
#
#  7. token_appointment_info() → returns (appt_date_str, is_next_day)
#                        Determines which day the token is for, based on IST clock.
#
#  8. Templates NEVER compute or format time. They only display pre-computed strings
#     passed from the backend. No date slicing, no JS date math for display.
# ═══════════════════════════════════════════════════════════════════════════════

# ── IST timezone (UTC+5:30) — pure stdlib, zero extra dependencies ────────────
_IST = timezone(timedelta(hours=5, minutes=30))

# ─────────────────────────────────────────────────────────────────────────────
#  CORE TIME FUNCTIONS  ← all time logic lives here, nowhere else
# ─────────────────────────────────────────────────────────────────────────────

def now_ist() -> datetime:
    """
    Return the current moment as a timezone-aware datetime in IST.
    This is the SINGLE source of truth for "what time is it now".
    """
    return datetime.now(_IST)


def ist_str_now() -> str:
    """
    Return the current IST time as a DB-storable string.
    Format: 'YYYY-MM-DD HH:MM:SS'  (no timezone suffix — always IST by convention)
    Use this for every explicit created_at insert. Never use CURRENT_TIMESTAMP.
    """
    return now_ist().strftime('%Y-%m-%d %H:%M:%S')


def parse_ist_str(db_str: str) -> datetime:
    """
    Parse a DB-stored IST string (written by ist_str_now()) back to an aware datetime.

    Handles two formats that may exist in the database:
      • New rows  → '2026-03-22 22:30:15'   (stored by ist_str_now(), IS already IST)
      • Old rows  → '2026-03-22 17:00:15'   (stored by SQLite CURRENT_TIMESTAMP, IS UTC)

    Detection rule: if the stored time looks like it was written during midnight–05:29 IST
    it would be < 00:00 UTC which is impossible — but we can't perfectly distinguish
    old UTC rows from new IST rows without a migration. The pragmatic production-safe
    approach: add a migration column `ist_stored` to mark new rows, OR simply delete
    hospital.db and start fresh (recommended — seed data re-generates automatically).
    After fresh start ALL rows are IST. This function treats all stored strings as IST.

    If you have old data: delete hospital.db and restart. Takes 5 seconds.
    """
    if not db_str:
        return now_ist()
    try:
        s = str(db_str).strip()[:19]          # take first 19 chars: YYYY-MM-DD HH:MM:SS
        naive = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        return naive.replace(tzinfo=_IST)     # attach IST — this string IS IST
    except (ValueError, TypeError):
        return now_ist()


def fmt_dt(dt: datetime, include_date: bool = True) -> str:
    """
    THE SINGLE formatter for all user-visible datetimes.
    Input:  any timezone-aware datetime (should be in IST)
    Output: '22 Mar 2026, 10:30 PM IST'
    If include_date=False: '10:30 PM IST'

    Never call strftime directly anywhere else in the codebase.
    """
    if dt is None:
        return '—'
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_IST)          # safety: treat naive as IST
    if include_date:
        return dt.strftime('%d %b %Y, %I:%M %p IST')
    else:
        return dt.strftime('%I:%M %p IST')


def fmt_date(date_str: str) -> str:
    """
    Format a YYYY-MM-DD date string to '22 Mar 2026'.
    Used for displaying appointment_date cleanly.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %b %Y')
    except (ValueError, TypeError):
        return date_str or '—'


def token_appointment_info() -> tuple:
    """
    Determine which calendar day a new token belongs to, based on IST clock.

    Returns: (appointment_date_str, is_next_day)
      appointment_date_str → 'YYYY-MM-DD'  (the day the token is for)
      is_next_day          → True if hospital is closed and token goes to tomorrow

    Logic:
      • hour < HOSPITAL_OPEN_HOUR  → same day  (early morning, hospital opens later)
      • HOSPITAL_OPEN_HOUR ≤ hour < HOSPITAL_CLOSE_HOUR → same day (open hours)
      • hour ≥ HOSPITAL_CLOSE_HOUR → next day  (hospital closed for today)
    """
    n = now_ist()
    if n.hour >= HOSPITAL_CLOSE_HOUR:
        return (n + timedelta(days=1)).strftime('%Y-%m-%d'), True
    return n.strftime('%Y-%m-%d'), False


def calc_meeting_time(appt_date_str: str, wait_mins: int) -> datetime:
    now = now_ist()

    try:
        appt_dt = datetime.strptime(appt_date_str, '%Y-%m-%d').replace(tzinfo=_IST)

        today_open = now.replace(hour=HOSPITAL_OPEN_HOUR, minute=0, second=0, microsecond=0)
        today_close = now.replace(hour=HOSPITAL_CLOSE_HOUR, minute=0, second=0, microsecond=0)

        if today_open <= now < today_close:
            return now + timedelta(minutes=wait_mins)

        next_day = appt_dt.replace(hour=HOSPITAL_OPEN_HOUR, minute=0, second=0, microsecond=0)
        return next_day + timedelta(minutes=wait_mins)

    except:
        return now + timedelta(minutes=wait_mins)


def is_hospital_open() -> bool:
    """True if current IST time is within hospital working hours."""
    return HOSPITAL_OPEN_HOUR <= now_ist().hour < HOSPITAL_CLOSE_HOUR


# ─────────────────────────────────────────────────────────────────────────────
#  APP CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DB_PATH = os.getenv('DB_PATH') or 'hospital.db'
DEPARTMENTS = ['General OPD', 'Cardiology', 'Orthopedic', 'Dermatology', 'Neurology']

GMAIL_ADDRESS  = os.getenv('GMAIL_ADDRESS')
GMAIL_APP_PASS = os.getenv('GMAIL_APP_PASS')
TWILIO_SID     = os.getenv('TWILIO_SID')
TWILIO_TOKEN   = os.getenv('TWILIO_TOKEN')
TWILIO_WA_FROM = os.getenv('TWILIO_WA_FROM')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

HOSPITAL_OPEN_HOUR  = 9    # 9:00 AM IST
HOSPITAL_CLOSE_HOUR = 21   # 9:00 PM IST
MINS_PER_TOKEN      = 5    # each token takes ~5 minutes

app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(t=t, LANGUAGES=LANGUAGES, RTL_LANGUAGES=RTL_LANGUAGES)

# Expose fmt_date as a Jinja filter (for templates that display appointment dates)
app.jinja_env.filters['fmt_date'] = fmt_date

@app.before_request
def set_language():
    if 'lang' not in session:
        session['lang'] = 'en'

@app.route('/set_lang/<lang>')
def set_lang(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
        session.modified = True
    return redirect(request.referrer or '/')

# ─────────────────────────────── DATABASE ────────────────────────────────────
def get_db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def hp(p): return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    conn = get_db(); c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
            age INTEGER DEFAULT 0, gender TEXT DEFAULT '', phone TEXT DEFAULT '',
            city TEXT DEFAULT '', blood_group TEXT DEFAULT '', lang TEXT DEFAULT 'en');
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
            department TEXT NOT NULL, qualification TEXT DEFAULT '',
            gender TEXT DEFAULT '', phone TEXT DEFAULT '', experience_years INTEGER DEFAULT 0,
            status TEXT DEFAULT 'approved');
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL, doctor_id INTEGER NOT NULL,
            department TEXT NOT NULL, token_number INTEGER NOT NULL,
            status TEXT DEFAULT "waiting", symptom TEXT DEFAULT '',
            appointment_date TEXT DEFAULT '',
            created_at TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER, doctor_id INTEGER, department TEXT,
            appointment_type TEXT, date TEXT, time TEXT,
            status TEXT DEFAULT "Scheduled", fee_inr INTEGER DEFAULT 500,
            notes TEXT DEFAULT '', created_at TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER, doctor_id INTEGER, department TEXT,
            diagnosis TEXT, medicines_prescribed TEXT,
            blood_pressure TEXT, pulse_bpm INTEGER, temperature_f REAL,
            weight_kg INTEGER, visit_date TEXT, followup_date TEXT,
            notes TEXT DEFAULT '', created_at TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS otp_store (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            identifier  TEXT NOT NULL, otp TEXT NOT NULL,
            purpose     TEXT NOT NULL, temp_data TEXT DEFAULT '',
            expires_at  INTEGER NOT NULL, used INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL, role TEXT NOT NULL,
            message TEXT NOT NULL, created_at TEXT DEFAULT '');
    ''')
    for col_sql in [
        "ALTER TABLE patients ADD COLUMN lang TEXT DEFAULT 'en'",
        "ALTER TABLE doctors ADD COLUMN status TEXT DEFAULT 'approved'",
        "ALTER TABLE tokens ADD COLUMN appointment_date TEXT DEFAULT ''",
        "ALTER TABLE otp_store ADD COLUMN temp_data TEXT DEFAULT ''",
    ]:
        try: c.execute(col_sql)
        except: pass
    try:
        cols = [r[1] for r in c.execute('PRAGMA table_info(otp_store)').fetchall()]
        if 'identifier' not in cols or 'temp_data' not in cols:
            c.execute('DROP TABLE IF EXISTS otp_store')
            c.execute('''CREATE TABLE otp_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT NOT NULL, otp TEXT NOT NULL,
                purpose TEXT NOT NULL, temp_data TEXT DEFAULT '',
                expires_at INTEGER NOT NULL, used INTEGER DEFAULT 0)''')
    except: pass
    conn.commit(); conn.close()
    seed_dataset()

# ─────────────────────────────── SEED ────────────────────────────────────────
def seed_dataset():
    conn = get_db()
    if conn.execute('SELECT COUNT(*) FROM doctors').fetchone()[0] >= 20:
        conn.close(); return
    print("  ⏳ Seeding dataset...")
    random.seed(42); c = conn.cursor()
    DOCS = [
        (1,'Dr. Anil Sharma',   'anil@hospital.com',   'General OPD','MBBS, MD',         'Male',  '9811001001',15),
        (2,'Dr. Meena Joshi',   'meena@hospital.com',  'General OPD','MBBS, DNB',         'Female','9811001002',10),
        (3,'Dr. Suresh Patel',  'suresh@hospital.com', 'General OPD','MBBS',              'Male',  '9811001003', 8),
        (4,'Dr. Kavita Reddy',  'kavita@hospital.com', 'General OPD','MBBS, MD',          'Female','9811001004',12),
        (5,'Dr. Priya Mehta',   'priya@hospital.com',  'Cardiology', 'MBBS, MD, DM',      'Female','9811002001',18),
        (6,'Dr. Rajesh Nair',   'rajesh@hospital.com', 'Cardiology', 'MBBS, MD, DM',      'Male',  '9811002002',20),
        (7,'Dr. Anita Kapoor',  'anita@hospital.com',  'Cardiology', 'MBBS, DNB Cardio',  'Female','9811002003',14),
        (8,'Dr. Rahul Verma',   'rahul@hospital.com',  'Orthopedic', 'MBBS, MS Ortho',    'Male',  '9811003001',16),
        (9,'Dr. Deepak Singh',  'deepak@hospital.com', 'Orthopedic', 'MBBS, DNB Ortho',   'Male',  '9811003002',11),
        (10,'Dr. Pooja Sharma', 'pooja@hospital.com',  'Orthopedic', 'MBBS, MS Ortho',    'Female','9811003003', 9),
        (11,'Dr. Vikash Kumar', 'vikash@hospital.com', 'Orthopedic', 'MBBS, MS',          'Male',  '9811003004',13),
        (12,'Dr. Sunita Rao',   'sunita@hospital.com', 'Dermatology','MBBS, MD Derma',    'Female','9811004001',17),
        (13,'Dr. Amit Tiwari',  'amit@hospital.com',   'Dermatology','MBBS, DVD',         'Male',  '9811004002', 7),
        (14,'Dr. Ritu Agarwal', 'ritu@hospital.com',   'Dermatology','MBBS, MD Derma',    'Female','9811004003',12),
        (15,'Dr. Vikram Das',   'vikram@hospital.com', 'Neurology',  'MBBS, MD, DM Neuro','Male',  '9811005001',22),
        (16,'Dr. Neha Gupta',   'neha@hospital.com',   'Neurology',  'MBBS, DM Neuro',    'Female','9811005002',15),
        (17,'Dr. Sanjay Mishra','sanjay@hospital.com', 'Neurology',  'MBBS, MD, DM',      'Male',  '9811005003',19),
        (18,'Dr. Pallavi Jain', 'pallavi@hospital.com','Neurology',  'MBBS, DNB Neuro',   'Female','9811005004',10),
        (19,'Dr. Kiran Shah',   'kiran@hospital.com',  'Neurology',  'MBBS, DM',          'Male',  '9811005005',13),
        (20,'Dr. Smita Kulkarni','smita@hospital.com', 'Neurology',  'MBBS, MD, DM Neuro','Female','9811005006',16),
    ]
    for d in DOCS:
        try: c.execute('INSERT OR REPLACE INTO doctors(id,name,email,password,department,qualification,gender,phone,experience_years,status) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (d[0],d[1],d[2],hp('doctor123'),d[3],d[4],d[5],d[6],d[7],'approved'))
        except: pass
    FM=['Rajesh','Suresh','Anil','Vikram','Deepak','Sanjay','Amit','Rahul','Rohit','Manish','Dinesh','Ganesh','Ramesh','Naresh','Mahesh','Akash','Vikas','Arjun','Nitin','Kapil']
    FF=['Priya','Sunita','Meena','Kavita','Anita','Ritu','Neha','Pooja','Sonia','Rekha','Usha','Geeta','Seema','Nisha','Pallavi','Anjali','Divya','Swati','Shreya','Komal']
    LN=['Sharma','Verma','Patel','Singh','Kumar','Gupta','Joshi','Rao','Nair','Mehta','Agarwal','Tiwari','Jain','Das','Mishra','Kapoor','Reddy','Shah','Kulkarni','Pillai']
    CITIES=['Mumbai','Delhi','Bangalore','Hyderabad','Chennai','Kolkata','Jaipur','Pune','Ahmedabad','Surat']
    BLOODS=['A+','A-','B+','B-','O+','O-','AB+','AB-']
    for i in range(1,101):
        g=random.choice(['Male','Female']); fn=random.choice(FM if g=='Male' else FF); ln=random.choice(LN)
        try: c.execute('INSERT OR REPLACE INTO patients(id,name,email,password,age,gender,phone,city,blood_group) VALUES(?,?,?,?,?,?,?,?,?)',
                       (i,f'{fn} {ln}',f'{fn.lower()}{i}@gmail.com',hp('patient123'),random.randint(18,75),g,f'98{random.randint(10000000,99999999)}',random.choice(CITIES),random.choice(BLOODS)))
        except: pass
    SYM={'General OPD':['Fever','Cold','Weakness','Stomach pain','Headache','Vomiting','Diabetes checkup','BP checkup'],
         'Cardiology':['Chest pain','Shortness of breath','Palpitations','High BP','Irregular heartbeat','Dizziness'],
         'Orthopedic':['Back pain','Knee pain','Shoulder injury','Fracture followup','Joint pain','Slip disc'],
         'Dermatology':['Skin rash','Acne','Hair loss','Eczema','Psoriasis','Fungal infection'],
         'Neurology':['Severe headache','Migraine','Numbness','Memory loss','Epilepsy followup','Tremors']}
    DDMAP={'General OPD':[1,2,3,4],'Cardiology':[5,6,7],'Orthopedic':[8,9,10,11],'Dermatology':[12,13,14],'Neurology':[15,16,17,18,19,20]}
    STAT=['waiting','waiting','called','completed','completed','completed','completed']
    tctr={i:0 for i in range(1,21)}; base=now_ist()
    for i in range(1,201):
        dept=random.choice(DEPARTMENTS); did=random.choice(DDMAP[dept]); tctr[did]+=1
        # Seed tokens: use IST times via ist_str_now equivalent
        cr=(base-timedelta(hours=random.randint(0,47),minutes=random.randint(0,59))).strftime('%Y-%m-%d %H:%M:%S')
        appt_d = base.strftime('%Y-%m-%d')  # seed: all today for simplicity
        try: c.execute('INSERT OR REPLACE INTO tokens(id,patient_id,doctor_id,department,token_number,status,symptom,created_at,appointment_date) VALUES(?,?,?,?,?,?,?,?,?)',
                       (i,random.randint(1,100),did,dept,tctr[did],random.choice(STAT),random.choice(SYM[dept]),cr,appt_d))
        except: pass
    ATYPES=['OPD Visit','Follow-up','Emergency','Consultation','Routine Checkup']
    ATIMES=['09:00','09:30','10:00','10:30','11:00','11:30','14:00','14:30','15:00','16:00']
    ASTATS=['Scheduled','Completed','Cancelled','No-Show']
    DDEPT={d[0]:d[3] for d in DOCS}
    for i in range(1,151):
        did=random.randint(1,20); adate=(base+timedelta(days=random.randint(0,14))).strftime('%Y-%m-%d')
        try: c.execute('INSERT OR REPLACE INTO appointments(id,patient_id,doctor_id,department,appointment_type,date,time,status,fee_inr,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (i,random.randint(1,100),did,DDEPT[did],random.choice(ATYPES),adate,random.choice(ATIMES),random.choice(ASTATS),random.choice([200,300,500,700,1000,1500]),ist_str_now()))
        except: pass
    DIAG={'General OPD':['Viral Fever','Hypertension','Type 2 Diabetes','Gastritis','Anemia','Vitamin D Deficiency'],
          'Cardiology':['Hypertensive Heart Disease','Coronary Artery Disease','Atrial Fibrillation','Heart Failure','Angina Pectoris'],
          'Orthopedic':['Lumbar Disc Herniation','Osteoarthritis Knee','Rotator Cuff Tear','Plantar Fasciitis','Cervical Spondylosis'],
          'Dermatology':['Contact Dermatitis','Psoriasis Vulgaris','Androgenic Alopecia','Tinea Corporis','Acne Vulgaris'],
          'Neurology':['Tension Headache','Migraine','Diabetic Neuropathy','Carpal Tunnel Syndrome','Essential Tremor']}
    MEDS={'General OPD':['Paracetamol 500mg','Azithromycin 500mg','Amlodipine 5mg','Metformin 500mg','Pantoprazole 40mg'],
          'Cardiology':['Aspirin 75mg','Atorvastatin 40mg','Metoprolol 50mg','Ramipril 5mg','Clopidogrel 75mg'],
          'Orthopedic':['Diclofenac 50mg','Pregabalin 75mg','Calcium+Vit D3','Etoricoxib 60mg','Methyl B12'],
          'Dermatology':['Clobetasol cream','Cetirizine 10mg','Isotretinoin 20mg','Ketoconazole shampoo','Tacrolimus ointment'],
          'Neurology':['Amitriptyline 25mg','Gabapentin 300mg','Sumatriptan 50mg','Levodopa 100mg','Topiramate 50mg']}
    for i in range(1,151):
        did=random.randint(1,20); dept=DDEPT[did]; meds=', '.join(random.sample(MEDS[dept],random.randint(1,3)))
        vd=(base-timedelta(days=random.randint(0,10))).strftime('%Y-%m-%d'); fd=(base+timedelta(days=random.randint(14,30))).strftime('%Y-%m-%d')
        try: c.execute('INSERT OR REPLACE INTO medical_records(id,patient_id,doctor_id,department,diagnosis,medicines_prescribed,blood_pressure,pulse_bpm,temperature_f,weight_kg,visit_date,followup_date,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (i,random.randint(1,100),did,dept,random.choice(DIAG[dept]),meds,
                        f'{random.randint(110,150)}/{random.randint(70,95)}',random.randint(62,105),
                        round(random.uniform(97.0,102.5),1),random.randint(45,95),vd,fd,ist_str_now()))
        except: pass
    conn.commit(); conn.close()
    conn2 = get_db()
    print(f"  ✅ Seeded: {conn2.execute('SELECT COUNT(*) FROM doctors').fetchone()[0]} doctors | "
          f"{conn2.execute('SELECT COUNT(*) FROM patients').fetchone()[0]} patients | "
          f"{conn2.execute('SELECT COUNT(*) FROM tokens').fetchone()[0]} tokens")
    conn2.close()

# ─────────────────────────────── AI (GROQ) ────────────────────────────────────
def gemini(prompt, system=None):
    """Groq LLM: llama-3.1-8b-instant primary, llama-3.1-70b-versatile fallback."""
    PRIMARY_MODEL  = "llama-3.1-8b-instant"
    FALLBACK_MODEL = "llama-3.1-70b-versatile"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        resp = client.chat.completions.create(messages=messages, model=PRIMARY_MODEL, max_tokens=1024, temperature=0.7)
        return resp.choices[0].message.content
    except Exception as e_primary:
        print(f"  ⚠️  Primary AI failed: {e_primary}")
    try:
        resp = client.chat.completions.create(messages=messages, model=FALLBACK_MODEL, max_tokens=1024, temperature=0.7)
        return resp.choices[0].message.content
    except Exception as e_fallback:
        print(f"  ⚠️  Fallback AI failed: {e_fallback}")
        return "I'm having trouble connecting right now. Please try again in a moment."

def format_bot_response(text):
    """Convert **bold** / *italic* / `code` markdown → safe HTML."""
    if not text: return text
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*\n]+?)\*',  r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+?)`',
                  r'<code style="background:rgba(0,0,0,.06);padding:1px 5px;border-radius:3px;">\1</code>', text)
    return text

# ─────────────────────────────── EMAIL ───────────────────────────────────────
def send_email(to_email, subject, html_body, lang='en'):
    if not to_email: return False
    if not GMAIL_ADDRESS or 'your_gmail' in GMAIL_ADDRESS:
        print('  ⚠️  Email not configured — skipping'); return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = f'SmartQueue Hospital <{GMAIL_ADDRESS}>'
        msg['To']      = to_email
        dir_attr = 'rtl' if lang in RTL_LANGUAGES else 'ltr'
        full_html = f"""
        <div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto;background:#f4f7f9;padding:20px;border-radius:12px;direction:{dir_attr};">
          <div style="background:linear-gradient(135deg,#1a5f7a,#2d8fb3);padding:20px;border-radius:10px;text-align:center;margin-bottom:20px;">
            <h2 style="color:white;margin:0;">🏥 SmartQueue Hospital</h2>
            <p style="color:rgba(255,255,255,.7);font-size:12px;margin:4px 0 0;">All times shown in IST (Indian Standard Time)</p>
          </div>
          <div style="background:white;padding:24px;border-radius:10px;line-height:1.8;color:#1c2b35;">{html_body}</div>
          <p style="text-align:center;color:#6b8290;font-size:12px;margin-top:16px;">SmartQueue Hospital Management System</p>
        </div>"""
        msg.attach(MIMEText(full_html, 'html', 'utf-8'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as srv:
            srv.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
            srv.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        print(f'  ✅ Email sent to {to_email}')
        return True
    except Exception as e:
        print(f'  ⚠️  Email failed: {e}'); return False

def send_whatsapp(phone, message):
    if not TWILIO_SID or 'your_twilio' in TWILIO_SID:
        print("  ⚠️  WhatsApp not configured — skipping"); return False
    if not phone: return False
    try:
        phone = str(phone).strip().replace(' ','').replace('-','').replace('(','').replace(')','')
        if phone.startswith('00'):   phone = '+' + phone[2:]
        if not phone.startswith('+'):
            phone = '+91' + phone if len(phone)==10 else '+' + phone.lstrip('0')
        to_wa = 'whatsapp:' + phone
        url   = f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json'
        data  = urllib.parse.urlencode({'From': TWILIO_WA_FROM, 'To': to_wa, 'Body': message}).encode()
        creds = base64.b64encode(f'{TWILIO_SID}:{TWILIO_TOKEN}'.encode()).decode()
        req   = urllib.request.Request(url, data=data,
                    headers={'Authorization': f'Basic {creds}',
                             'Content-Type': 'application/x-www-form-urlencoded'}, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read())
            if res.get('sid'): print(f"  ✅ WhatsApp sent to {phone}"); return True
            print(f"  ⚠️  WhatsApp response: {res}"); return False
    except Exception as e:
        print(f"  ⚠️  WhatsApp failed: {e}"); return False

# ─────────────────────────────── NOTIFICATIONS ───────────────────────────────
def notify_token_generated(patient, doctor, token_number, dept, wait_mins,
                            generated_str, meet_time_str, is_next_day=False):
    """
    Send token generation email + WhatsApp.
    All time strings are pre-formatted by the caller using fmt_dt().
    This function only builds the message and sends — no time logic here.
    """
    lang = (patient.get('lang') or 'en')
    if lang not in ['en','hi','fr','es','de','ar','bn','mr']: lang = 'en'
    next_note = ""
    if is_next_day:
        next_note = "<p style='color:#e8734a;font-weight:600;'>📅 Hospital is closed — appointment scheduled for <strong>tomorrow morning</strong>.</p>"
    subject = t('email_token_subject', lang).replace('{}', str(token_number))
    body = f"""
        <h3 style="color:#1a5f7a;">{t('email_token_ready', lang)}</h3>
        <p>{t('email_dear', lang)} <strong>{patient['name']}</strong>,</p>
        {next_note}
        <p>{t('email_token_body', lang)}</p>
        <div style="background:#e8f4f8;padding:16px;border-radius:8px;margin:16px 0;text-align:center;">
          <div style="font-size:52px;font-weight:800;color:#1a5f7a;">#{token_number}</div>
        </div>
        <table style="width:100%;border-collapse:collapse;">
          <tr><td style="padding:8px;color:#6b8290;">{t('doctor',lang)}</td><td style="padding:8px;font-weight:600;">{doctor['name']}</td></tr>
          <tr style="background:#f4f7f9;"><td style="padding:8px;color:#6b8290;">{t('department',lang)}</td><td style="padding:8px;">{dept}</td></tr>
          <tr><td style="padding:8px;color:#6b8290;">🕐 Generated (IST)</td><td style="padding:8px;font-weight:600;">{generated_str}</td></tr>
          <tr style="background:#f4f7f9;"><td style="padding:8px;color:#6b8290;">⏱ Est. Wait</td><td style="padding:8px;">~{wait_mins} {t('mins',lang)}</td></tr>
          <tr style="background:#e8f7f0;"><td style="padding:8px;color:#1e7a4e;font-weight:700;">📅 Est. Meeting Time (IST)</td>
              <td style="padding:8px;font-weight:700;color:#1e7a4e;">{meet_time_str}</td></tr>
        </table>
        <p style="margin-top:16px;">{t('email_stay_nearby',lang)}</p>"""
    wa_msg = (
        f"🏥 *SmartQueue Hospital*\n──────────────────\n"
        f"🎫 *Token #{token_number} Generated!*\n\n"
        f"👨‍⚕️ Doctor: {doctor['name']}\n🏢 Dept: {dept}\n"
        f"🕐 Generated: {generated_str}\n"
        f"⏱ Est. wait: ~{wait_mins} mins\n📅 Est. meeting: {meet_time_str}\n\n"
        f"Please stay nearby. You will be reminded before your turn."
        + ("\n\n📅 *Scheduled for TOMORROW MORNING* (after closing time)" if is_next_day else "")
    )
    if patient.get('email'): send_email(patient['email'], subject, body, lang)
    if patient.get('phone'): send_whatsapp(patient['phone'], wa_msg)

def notify_token_called(patient, doctor, token_number, dept):
    lang = patient.get('lang','en') or 'en'
    subject = t('email_called_subject', lang).replace('{}', str(token_number))
    body = f"""
        <h3 style="color:#e8734a;">{t('email_your_turn',lang)}</h3>
        <p>{t('email_dear',lang)} <strong>{patient['name']}</strong>,</p>
        <p style="font-size:18px;font-weight:600;color:#e8734a;">🔔 Token <strong>#{token_number}</strong></p>
        <div style="background:#fef3ee;padding:16px;border-radius:8px;margin:16px 0;border-left:4px solid #e8734a;">
          <p style="margin:0;font-weight:600;">{t('email_proceed_now',lang)}</p>
          <p style="margin:8px 0 0;color:#6b8290;">{t('department',lang)}: {dept} — {doctor['name']}</p>
        </div>
        <p style="color:#d94040;font-weight:600;">⚠️ {t('email_dont_miss',lang)}</p>"""
    wa_msg = (f"🏥 *SmartQueue Hospital*\n──────────────────\n"
              f"🔔 *TOKEN #{token_number} — YOUR TURN!*\n\n"
              f"👨‍⚕️ Please go to {doctor['name']} NOW\n🏢 Department: {dept}\n\n"
              f"⚠️ Arrive within 5 minutes or your token may be skipped.")
    if patient.get('email'): send_email(patient['email'], subject, body, lang)
    if patient.get('phone'): send_whatsapp(patient['phone'], wa_msg)

def notify_token_completed(patient, doctor, token_number):
    lang = patient.get('lang','en') or 'en'
    subject = t('email_complete_subject', lang)
    body = f"""
        <h3 style="color:#2e9e6b;">{t('email_visit_done',lang)}</h3>
        <p>{t('email_dear',lang)} <strong>{patient['name']}</strong>,</p>
        <p>{t('email_visit_thanks',lang)}</p>
        <div style="background:#e8f7f0;padding:16px;border-radius:8px;margin:16px 0;border-left:4px solid #2e9e6b;">
          <p style="margin:0;font-size:1.1rem;">{t('email_get_well',lang)}</p>
        </div>
        <p style="color:#6b8290;font-size:14px;">{t('email_follow_advice',lang)}</p>"""
    wa_msg = (f"🏥 *SmartQueue Hospital*\n──────────────────\n"
              f"✅ *Visit Completed — Token #{token_number}*\n\n"
              f"Thank you for visiting SmartQueue Hospital.\nDoctor: {doctor['name']}\n\n"
              f"💊 Please follow your doctor's advice. Get well soon! 💚")
    if patient.get('email'): send_email(patient['email'], subject, body, lang)
    if patient.get('phone'): send_whatsapp(patient['phone'], wa_msg)

def notify_appointment_booked(patient, doctor, appt_type, adate, atime, notes=''):
    lang = patient.get('lang','en') or 'en'
    subject = f"📅 Appointment Confirmed — {doctor['name']} on {adate}"
    body = f"""
        <h3 style='color:#e8734a;'>✅ Appointment Confirmed!</h3>
        <p>Dear <strong>{patient['name']}</strong>,</p>
        <div style='background:linear-gradient(135deg,#fef3ee,#fddbc8);border-radius:12px;padding:20px;margin:20px 0;'>
          <table style='width:100%;border-collapse:collapse;'>
            <tr><td style='padding:8px;color:#8a4a2a;font-weight:600;'>👨‍⚕️ Doctor</td><td style='padding:8px;font-weight:700;'>{doctor['name']}</td></tr>
            <tr style='background:rgba(255,255,255,.5);'><td style='padding:8px;color:#8a4a2a;font-weight:600;'>🏢 Department</td><td style='padding:8px;'>{doctor['department']}</td></tr>
            <tr><td style='padding:8px;color:#8a4a2a;font-weight:600;'>📋 Type</td><td style='padding:8px;'>{appt_type}</td></tr>
            <tr style='background:rgba(255,255,255,.5);'><td style='padding:8px;color:#8a4a2a;font-weight:600;'>📅 Date</td><td style='padding:8px;font-weight:700;color:#e8734a;'>{adate}</td></tr>
            <tr><td style='padding:8px;color:#8a4a2a;font-weight:600;'>🕐 Time (IST)</td><td style='padding:8px;font-weight:700;color:#e8734a;'>{atime}</td></tr>
            {f"<tr style='background:rgba(255,255,255,.5);'><td style='padding:8px;color:#8a4a2a;font-weight:600;'>📝 Notes</td><td style='padding:8px;'>{notes}</td></tr>" if notes else ''}
          </table>
        </div>
        <p style='color:#6b8290;font-size:13px;'>Please arrive 10 minutes before your appointment time.</p>"""
    wa_msg = (f"🏥 *SmartQueue Hospital*\n──────────────────\n"
              f"📅 *Appointment Confirmed!*\n\n"
              f"👨‍⚕️ Doctor: {doctor['name']}\n🏢 Dept: {doctor['department']}\n"
              f"📋 Type: {appt_type}\n📅 Date: {adate}\n🕐 Time: {atime} IST\n\n"
              f"Please arrive 10 minutes early. ✅")
    try:
        if patient.get('email'): send_email(patient['email'], subject, body, lang)
    except Exception as e:
        print(f"  ⚠️  Appt email error: {e}")
    try:
        if patient.get('phone'): send_whatsapp(patient['phone'], wa_msg)
    except Exception as e:
        print(f"  ⚠️  Appt WhatsApp error: {e}")

# ─────────────────────────────── REMINDERS ───────────────────────────────────
def schedule_reminder(reminder_type, patient, doctor_name, dept,
                      token_number=None, wait_minutes=None,
                      appt_date=None, appt_time=None):
    """
    Schedule background reminder. Never blocks the request.
    Token:       fires (wait_minutes - 3) minutes after token generated.
    Appointment: fires 60 minutes before appointment (IST-aware).
    """
    def _token_reminder():
        try:
            lang=patient.get('lang','en') or 'en'; name=patient.get('name','Patient')
            email=patient.get('email',''); phone=patient.get('phone','')
            subject=f"⏰ Reminder: Token #{token_number} — Almost Your Turn!"
            body=f"""<h3 style='color:#e8734a;'>⏰ Almost Your Turn!</h3>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Your token <strong>#{token_number}</strong> will be called very soon!</p>
                <div style='background:#fef3ee;padding:16px;border-radius:8px;margin:16px 0;border-left:4px solid #e8734a;'>
                  <p style='margin:0;font-weight:600;'>🏃 Please head to <strong>{dept}</strong> department now.</p>
                  <p style='margin:8px 0 0;color:#6b8290;'>Doctor: {doctor_name}</p>
                </div>
                <p style='color:#d94040;font-weight:600;'>⚠️ Arrive within 5 minutes or your token may be skipped.</p>"""
            wa_msg=(f"🏥 *SmartQueue Hospital — REMINDER*\n──────────────────\n"
                    f"⏰ *Token #{token_number} — Almost Your Turn!*\n\n"
                    f"🏃 Please go to *{dept}* department NOW\n👨‍⚕️ Doctor: {doctor_name}\n\n"
                    f"⚠️ Arrive within 5 minutes or your token may be skipped.")
            if email: send_email(email, subject, body, lang)
            if phone: send_whatsapp(phone, wa_msg)
            print(f"  ✅ Token reminder sent → {name}")
        except Exception as e:
            print(f"  ⚠️  Token reminder error: {e}")

    def _appointment_reminder():
        try:
            lang=patient.get('lang','en') or 'en'; name=patient.get('name','Patient')
            email=patient.get('email',''); phone=patient.get('phone','')
            subject=f"⏰ Appointment Reminder — {doctor_name} at {appt_time} IST"
            body=f"""<h3 style='color:#1a5f7a;'>📅 Appointment in 1 Hour!</h3>
                <p>Dear <strong>{name}</strong>,</p>
                <p>Your appointment is in approximately <strong>1 hour</strong> (IST).</p>
                <div style='background:#e8f4f8;padding:16px;border-radius:8px;margin:16px 0;'>
                  <table style='width:100%;border-collapse:collapse;'>
                    <tr><td style='padding:6px;color:#6b8290;'>👨‍⚕️ Doctor</td><td style='padding:6px;font-weight:600;'>{doctor_name}</td></tr>
                    <tr><td style='padding:6px;color:#6b8290;'>📅 Date</td><td style='padding:6px;'>{appt_date}</td></tr>
                    <tr><td style='padding:6px;color:#6b8290;'>🕐 Time (IST)</td><td style='padding:6px;font-weight:700;color:#1a5f7a;'>{appt_time}</td></tr>
                    <tr><td style='padding:6px;color:#6b8290;'>🏢 Dept</td><td style='padding:6px;'>{dept}</td></tr>
                  </table>
                </div>
                <p style='color:#6b8290;font-size:13px;'>Please arrive 10 minutes early and bring relevant documents.</p>"""
            wa_msg=(f"🏥 *SmartQueue Hospital — REMINDER*\n──────────────────\n"
                    f"📅 *Appointment in ~1 Hour!*\n\n"
                    f"👨‍⚕️ Doctor: {doctor_name}\n🏢 Dept: {dept}\n"
                    f"📅 Date: {appt_date}\n🕐 Time: {appt_time} IST\n\nPlease arrive 10 minutes early. ✅")
            if email: send_email(email, subject, body, lang)
            if phone: send_whatsapp(phone, wa_msg)
            print(f"  ✅ Appointment reminder sent → {name}")
        except Exception as e:
            print(f"  ⚠️  Appointment reminder error: {e}")

    try:
        if reminder_type == 'token' and wait_minutes is not None:
            delay = max(0, (int(wait_minutes) - 3) * 60)
            t_obj = threading.Timer(delay, _token_reminder)
            t_obj.daemon = True; t_obj.start()
            print(f"  ⏰ Token reminder in {delay//60}m {delay%60}s")

        elif reminder_type == 'appointment' and appt_date and appt_time:
            try:
                appt_dt   = datetime.strptime(f"{appt_date} {appt_time}", "%Y-%m-%d %H:%M").replace(tzinfo=_IST)
                remind_dt = appt_dt - timedelta(minutes=60)
                delay     = (remind_dt - now_ist()).total_seconds()
                if delay > 0:
                    t_obj = threading.Timer(delay, _appointment_reminder)
                    t_obj.daemon = True; t_obj.start()
                    print(f"  ⏰ Appt reminder at {fmt_dt(remind_dt)}")
                else:
                    print("  ℹ️  Appointment < 60 min away — reminder skipped")
            except ValueError as ve:
                print(f"  ⚠️  Appt reminder parse error: {ve}")
    except Exception as e:
        print(f"  ⚠️  schedule_reminder error: {e}")

# ─────────────────────────────── OTP HELPERS ─────────────────────────────────
def generate_otp(): return str(random.randint(100000, 999999))

def save_otp(identifier, otp, purpose, temp_data=''):
    conn = get_db()
    conn.execute('DELETE FROM otp_store WHERE identifier=? AND purpose=?', (identifier, purpose))
    conn.execute('INSERT INTO otp_store(identifier,otp,purpose,temp_data,expires_at) VALUES(?,?,?,?,?)',
                 (identifier, otp, purpose, temp_data, int(time.time())+600))
    conn.commit(); conn.close()

def verify_otp(identifier, otp_input, purpose):
    conn = get_db()
    row  = conn.execute(
        'SELECT * FROM otp_store WHERE identifier=? AND purpose=? AND used=0 ORDER BY id DESC LIMIT 1',
        (identifier, purpose)).fetchone()
    if not row:   conn.close(); return 'invalid', ''
    if int(time.time()) > row['expires_at']: conn.close(); return 'expired', ''
    if str(row['otp']).strip() != str(otp_input).strip(): conn.close(); return 'invalid', ''
    conn.execute('UPDATE otp_store SET used=1 WHERE id=?', (row['id'],))
    conn.commit(); conn.close()
    return 'ok', row['temp_data'] or ''

def send_otp_email(to_email, otp, lang='en'):
    subject = t('otp_email_subject', lang)
    body = f"""
        <h3 style='color:#e8734a;text-align:center;'>{t('otp_email_title',lang)}</h3>
        <p>{t('otp_email_body',lang)}</p>
        <div style='background:linear-gradient(135deg,#e8734a,#f0956d);border-radius:12px;padding:28px;text-align:center;margin:20px 0;'>
          <div style='font-size:11px;color:rgba(255,255,255,.8);text-transform:uppercase;letter-spacing:3px;margin-bottom:10px;'>Your OTP Code</div>
          <div style='font-size:54px;font-weight:900;letter-spacing:14px;color:white;font-family:monospace;'>{otp}</div>
          <div style='font-size:12px;color:rgba(255,255,255,.7);margin-top:10px;'>⏱ Valid for 10 minutes only</div>
        </div>
        <p style='color:#d94040;font-weight:600;font-size:13px;'>⚠️ {t('otp_email_warning',lang)}</p>
        <p style='color:#6b8290;font-size:12px;'>{t('otp_email_ignore',lang)}</p>"""
    send_email(to_email, subject, body, lang)

# ─────────────────────────────── ERROR PAGES ─────────────────────────────────
@app.errorhandler(404)
def not_found(e): return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    import traceback; err=traceback.format_exc()
    print("\n=== 500 ERROR ===\n", err, "\n=================\n")
    return render_template('500.html', error=str(e), trace=err), 500

# ─────────────────────────────── FORGOT PASSWORD ─────────────────────────────
@app.route('/patient/forgot_password', methods=['GET','POST'])
def forgot_password():
    lang = session.get('lang','en')
    try:
        if request.method == 'POST':
            step  = request.form.get('step','email')
            email = request.form.get('email','').strip().lower()
            if step == 'email':
                conn = get_db(); pat = conn.execute('SELECT * FROM patients WHERE email=?',(email,)).fetchone(); conn.close()
                if not pat: flash(t('email_not_found',lang),'error'); return render_template('forgot_password.html',step='email',lang=lang)
                otp = generate_otp(); save_otp(email,otp,'forgot_pwd')
                send_otp_email(email,otp,pat['lang'] if pat['lang'] else lang)
                session['fp_email'] = email; flash(t('otp_sent_msg',lang),'success')
                return render_template('forgot_password.html',step='otp',email=email,lang=lang)
            elif step == 'otp':
                fp_email = session.get('fp_email',email)
                result,_ = verify_otp(fp_email,request.form.get('otp','').strip(),'forgot_pwd')
                if result=='expired': flash(t('otp_expired',lang),'error'); return render_template('forgot_password.html',step='email',lang=lang)
                if result=='invalid': flash(t('otp_invalid',lang),'error'); return render_template('forgot_password.html',step='otp',email=fp_email,lang=lang)
                session['fp_verified'] = True
                return render_template('forgot_password.html',step='newpwd',email=fp_email,lang=lang)
            elif step == 'newpwd':
                if not session.get('fp_verified'): flash('Session expired.','error'); return redirect(url_for('forgot_password'))
                fp_email = session.get('fp_email','')
                pwd1     = request.form.get('password',''); pwd2 = request.form.get('confirm_password','')
                if not pwd1 or len(pwd1)<6: flash('Password must be at least 6 characters.','error'); return render_template('forgot_password.html',step='newpwd',email=fp_email,lang=lang)
                if pwd1!=pwd2: flash(t('pwd_mismatch',lang),'error'); return render_template('forgot_password.html',step='newpwd',email=fp_email,lang=lang)
                conn=get_db(); conn.execute('UPDATE patients SET password=? WHERE email=?',(hp(pwd1),fp_email)); conn.commit(); conn.close()
                session.pop('fp_email',None); session.pop('fp_verified',None)
                flash(t('pwd_reset_success',lang),'success'); return redirect(url_for('patient_login'))
        return render_template('forgot_password.html',step='email',lang=lang)
    except Exception as e:
        import traceback; print(traceback.format_exc())
        flash('An error occurred. Please try again.','error')
        return render_template('forgot_password.html',step='email',lang=lang)

@app.route('/patient/resend_otp', methods=['POST'])
def resend_otp():
    lang=session.get('lang','en'); fp_email=session.get('fp_email','')
    purpose=request.form.get('purpose','forgot_pwd')
    if not fp_email: return redirect(url_for('patient_login'))
    conn=get_db(); pat=conn.execute('SELECT * FROM patients WHERE email=?',(fp_email,)).fetchone(); conn.close()
    if pat:
        otp=generate_otp(); save_otp(fp_email,otp,purpose)
        send_otp_email(fp_email,otp,pat['lang'] or lang); flash(t('otp_sent_msg',lang),'success')
    return redirect(url_for('otp_login' if purpose=='mobile_login' else 'forgot_password'))

@app.route('/patient/otp_login', methods=['GET','POST'])
def otp_login():
    lang=session.get('lang','en')
    if request.method=='POST':
        step=request.form.get('step','mobile')
        phone=request.form.get('phone','').strip().replace(' ','').replace('-','')
        if phone.startswith('+91'): phone=phone[3:]
        if phone.startswith('0'):   phone=phone[1:]
        if step=='mobile':
            if len(phone)!=10 or not phone.isdigit():
                flash('Please enter a valid 10-digit mobile number.','error')
                return render_template('otp_login.html',step='mobile',lang=lang)
            conn=get_db(); pat=conn.execute('SELECT * FROM patients WHERE phone=?',(phone,)).fetchone(); conn.close()
            if not pat: flash(t('mobile_not_found',lang),'error'); return render_template('otp_login.html',step='mobile',lang=lang)
            otp=generate_otp(); save_otp(phone,otp,'mobile_login')
            send_otp_email(pat['email'],otp,pat['lang'] or lang)
            session.update({'otp_phone':phone,'otp_pat_id':pat['id'],'fp_email':pat['email']})
            flash(f"{t('otp_sent_msg',lang)} ({pat['email']})","success")
            return render_template('otp_login.html',step='otp',phone=phone,lang=lang)
        elif step=='otp':
            otp_phone=session.get('otp_phone',phone)
            result=verify_otp(otp_phone,request.form.get('otp','').strip(),'mobile_login')
            if result=='expired': flash(t('otp_expired',lang),'error'); return render_template('otp_login.html',step='mobile',lang=lang)
            if result=='invalid': flash(t('otp_invalid',lang),'error'); return render_template('otp_login.html',step='otp',phone=otp_phone,lang=lang)
            conn=get_db(); pat=conn.execute('SELECT * FROM patients WHERE id=?',(session.get('otp_pat_id'),)).fetchone(); conn.close()
            if not pat: flash('Patient not found.','error'); return redirect(url_for('patient_login'))
            session.pop('otp_phone',None); session.pop('otp_pat_id',None)
            session.update({'patient_id':pat['id'],'patient_name':pat['name'],'role':'patient','lang':pat['lang'] or 'en'})
            flash(f"Welcome back, {pat['name']}!",'success')
            return redirect(url_for('patient_dashboard'))
    return render_template('otp_login.html',step='mobile',lang=lang)

# ─────────────────────────────── HOME ────────────────────────────────────────
@app.route('/')
def home():
    conn=get_db()
    stats={'doctors':conn.execute('SELECT COUNT(*) FROM doctors').fetchone()[0],
           'patients':conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0],
           'tokens':conn.execute('SELECT COUNT(*) FROM tokens').fetchone()[0]}
    conn.close()
    return render_template('home.html',stats=stats)

# ─────────────────────────────── PATIENT AUTH ────────────────────────────────
@app.route('/patient/register', methods=['GET','POST'])
def patient_register():
    lang=session.get('lang','en')
    if request.method=='POST':
        n=request.form['name'].strip(); e=request.form['email'].strip().lower(); p=request.form['password']
        if not n or not e or not p: flash('Name, email and password are required.','error'); return render_template('patient_register.html')
        if len(p)<6: flash('Password must be at least 6 characters.','error'); return render_template('patient_register.html')
        conn=get_db()
        if conn.execute('SELECT id FROM patients WHERE email=?',(e,)).fetchone():
            conn.close(); flash('Email already registered. Please login.','error'); return render_template('patient_register.html')
        conn.close()
        temp_data=json.dumps({'name':n,'email':e,'password':hp(p),
            'age':request.form.get('age','0') or '0','gender':request.form.get('gender',''),
            'phone':request.form.get('phone',''),'city':request.form.get('city',''),
            'blood_group':request.form.get('blood_group',''),'lang':lang})
        otp=generate_otp(); save_otp(e,otp,'register',temp_data)
        send_otp_email(e,otp,lang); session['reg_email']=e
        flash(f'A 6-digit OTP has been sent to {e}. Check your inbox!','success')
        return redirect(url_for('verify_register_otp'))
    return render_template('patient_register.html')

@app.route('/patient/verify_email', methods=['GET','POST'])
def verify_register_otp():
    lang=session.get('lang','en'); email=session.get('reg_email','')
    if not email: flash('Session expired. Please register again.','error'); return redirect(url_for('patient_register'))
    if request.method=='POST':
        action=request.form.get('action','verify')
        if action=='resend':
            conn=get_db(); row=conn.execute('SELECT temp_data FROM otp_store WHERE identifier=? AND purpose=? ORDER BY id DESC LIMIT 1',(email,'register')).fetchone(); conn.close()
            td=row['temp_data'] if row else '{}'; otp=generate_otp(); save_otp(email,otp,'register',td)
            send_otp_email(email,otp,lang); flash('New OTP sent!','success')
            return render_template('verify_otp.html',email=email,purpose='register',lang=lang)
        result,tdata=verify_otp(email,request.form.get('otp','').strip(),'register')
        if result=='expired': flash(t('otp_expired',lang),'error'); session.pop('reg_email',None); return redirect(url_for('patient_register'))
        if result=='invalid': flash(t('otp_invalid',lang),'error'); return render_template('verify_otp.html',email=email,purpose='register',lang=lang)
        try: td=json.loads(tdata) if tdata else {}
        except: td={}
        if not td: flash('Session data lost. Please register again.','error'); session.pop('reg_email',None); return redirect(url_for('patient_register'))
        conn=get_db()
        try:
            conn.execute('INSERT INTO patients(name,email,password,age,gender,phone,city,blood_group,lang) VALUES(?,?,?,?,?,?,?,?,?)',
                         (td['name'],td['email'],td['password'],int(td.get('age',0) or 0),td.get('gender',''),td.get('phone',''),td.get('city',''),td.get('blood_group',''),td.get('lang','en')))
            conn.commit(); session.pop('reg_email',None)
            flash('✅ Email verified! Account created. Please login.','success')
            return redirect(url_for('patient_login'))
        except sqlite3.IntegrityError: flash('Email already registered.','error'); return redirect(url_for('patient_login'))
        finally: conn.close()
    return render_template('verify_otp.html',email=email,purpose='register',lang=lang)

@app.route('/verify_otp', methods=['GET','POST'])
def verify_otp_page(): return redirect(url_for('verify_register_otp'))

@app.route('/patient/login', methods=['GET','POST'])
def patient_login():
    if request.method=='POST':
        e,p=request.form['email'].strip().lower(),request.form['password']
        conn=get_db(); row=conn.execute('SELECT * FROM patients WHERE email=? AND password=?',(e,hp(p))).fetchone(); conn.close()
        if row:
            session.update({'patient_id':row['id'],'patient_name':row['name'],'role':'patient','lang':row['lang'] or 'en'})
            return redirect(url_for('patient_dashboard'))
        flash('Invalid email or password.','error')
    return render_template('patient_login.html')

@app.route('/patient/logout')
def patient_logout(): session.clear(); return redirect(url_for('home'))

@app.route('/patient/profile', methods=['GET','POST'])
def patient_profile():
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    pid=session['patient_id']; conn=get_db()
    if request.method=='POST':
        n=request.form['name'].strip(); chosen_lang=request.form.get('lang',session.get('lang','en'))
        conn.execute('UPDATE patients SET name=?,age=?,gender=?,phone=?,city=?,blood_group=?,lang=? WHERE id=?',
            (n,request.form.get('age',0) or 0,request.form.get('gender',''),request.form.get('phone',''),
             request.form.get('city',''),request.form.get('blood_group',''),chosen_lang,pid))
        conn.commit(); session['patient_name']=n; session['lang']=chosen_lang; flash('Profile updated!','success')
    patient=conn.execute('SELECT * FROM patients WHERE id=?',(pid,)).fetchone(); conn.close()
    return render_template('patient_profile.html',patient=patient)

# ═══════════════════════════════════════════════════════════════════════════════
#  PATIENT DASHBOARD  ←  ALL time display pre-computed here, nothing in template
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/patient/dashboard')
def patient_dashboard():
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    pid=session['patient_id']; conn=get_db()

    active = conn.execute(
        'SELECT t.*,d.name as doctor_name FROM tokens t '
        'JOIN doctors d ON t.doctor_id=d.id '
        'WHERE t.patient_id=? AND t.status IN ("waiting","called")', (pid,)
    ).fetchone()

    queue_info = None
    if active:
        # Extract appointment date from the active token
        appt_date_str = active['appointment_date'] or now_ist().strftime('%Y-%m-%d')
        
        # How many tokens are ahead in queue (waiting and have lower token number)
        ahead = conn.execute(
            'SELECT COUNT(*) FROM tokens WHERE doctor_id=? AND status="waiting" AND token_number<?',
            (active['doctor_id'], active['token_number'])
        ).fetchone()[0]

        # Position = ahead + 1 (1-based: if 0 ahead, you are position 1)
        position  = ahead + 1
        wait_mins = ahead * MINS_PER_TOKEN   # minutes until this patient's turn

        # ── generated time: read from DB, parse as IST, format ───────────────
        # parse_ist_str() handles the IST string written by ist_str_now()
        generated_dt  = parse_ist_str(active['created_at'])
        generated_str = fmt_dt(generated_dt)

        # ── meeting time: ALWAYS based on appointment_date + position ─────────
        # calc_meeting_time uses appointment_date (the actual day of the visit)
        # so after-hours tokens correctly show TOMORROW 9:XX AM
        meet_dt = calc_meeting_time(appt_date_str, wait_mins)

        now = now_ist()

        # 🔥 FINAL FIX: prevent past meeting time
        if meet_dt < now:
             meet_dt = now + timedelta(minutes=5)

        meet_str = fmt_dt(meet_dt)

        # ── token history: pre-format all timestamps so template just displays ─
        queue_info = {
            'token':      active,
            'position':   position,
            'wait_time':  wait_mins,
            'generated':  generated_str,   # e.g. "22 Mar 2026, 10:30 PM IST"
            'meet_time':  meet_str,         # e.g. "23 Mar 2026, 09:05 AM IST"
            'appt_date_display': fmt_date(appt_date_str),  # e.g. "23 Mar 2026"
        }

    doctors    = conn.execute('SELECT * FROM doctors ORDER BY department,name').fetchall()
    my_records = conn.execute(
        'SELECT mr.*,d.name as doctor_name FROM medical_records mr '
        'JOIN doctors d ON mr.doctor_id=d.id WHERE mr.patient_id=? '
        'ORDER BY mr.visit_date DESC LIMIT 5', (pid,)
    ).fetchall()
    my_appts   = conn.execute(
        'SELECT a.*,d.name as doctor_name FROM appointments a '
        'JOIN doctors d ON a.doctor_id=d.id WHERE a.patient_id=? '
        'ORDER BY a.date DESC LIMIT 5', (pid,)
    ).fetchall()

    # Pre-format token history timestamps — template ONLY does {{ tk.gen_str }}
    raw_hist = conn.execute(
        'SELECT t.*,d.name as doctor_name FROM tokens t '
        'JOIN doctors d ON t.doctor_id=d.id WHERE t.patient_id=? '
        'ORDER BY t.created_at DESC LIMIT 10', (pid,)
    ).fetchall()
    conn.close()

    # Build pre-formatted token history list
    token_hist = []
    for tk in raw_hist:
        gen_dt  = parse_ist_str(tk['created_at'])
        appt_d  = tk['appointment_date'] or gen_dt.strftime('%Y-%m-%d')
        token_hist.append({
            'token_number':  tk['token_number'],
            'doctor_name':   tk['doctor_name'],
            'department':    tk['department'],
            'status':        tk['status'],
            'gen_str':       fmt_dt(gen_dt),               # "22 Mar 2026, 10:30 PM IST"
            'appt_date_str': fmt_date(appt_d),             # "23 Mar 2026"
        })

    return render_template(
        'patient_dashboard.html',
        active_token=active,
        queue_info=queue_info,
        doctors=doctors,
        departments=DEPARTMENTS,
        my_records=my_records,
        my_appts=my_appts,
        token_hist=token_hist,
        show_feedback=session.pop('show_feedback', False),
    )

# ═══════════════════════════════════════════════════════════════════════════════
#  TOKEN GENERATION  ←  Single source of truth for all time values
# ═══════════════════════════════════════════════════════════════════════════════
@app.route('/patient/generate_token', methods=['POST'])
def generate_token():
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    pid, did = session['patient_id'], request.form['doctor_id']
    conn = get_db()

    if conn.execute('SELECT id FROM tokens WHERE patient_id=? AND status IN ("waiting","called")',(pid,)).fetchone():
        flash('You already have an active token.','error'); conn.close(); return redirect(url_for('patient_dashboard'))

    doc = conn.execute('SELECT * FROM doctors WHERE id=?',(did,)).fetchone()
    if not doc: flash('Invalid doctor.','error'); conn.close(); return redirect(url_for('patient_dashboard'))

    last = conn.execute('SELECT MAX(token_number) FROM tokens WHERE doctor_id=?',(did,)).fetchone()[0]
    tnum = (last or 0) + 1

    # ── Step 1: Determine appointment date (IST-aware) ────────────────────────
    appt_date, is_next_day = token_appointment_info()

    # ── Step 2: Get current IST time string for created_at ───────────────────
    created_at_ist = ist_str_now()   # e.g. "2026-03-22 22:30:15"  — stored IST

    # ── Step 3: Insert token with explicit IST created_at ────────────────────
    conn.execute(
        'INSERT INTO tokens(patient_id,doctor_id,department,token_number,status,appointment_date,created_at) '
        'VALUES(?,?,?,?,?,?,?)',
        (pid, did, doc['department'], tnum, 'waiting', appt_date, created_at_ist)
    )
    conn.commit()

    # ── Step 4: Compute queue position for this new token ────────────────────
    ahead = conn.execute(
        'SELECT COUNT(*) FROM tokens WHERE doctor_id=? AND status="waiting" AND token_number<?',
        (did, tnum)
    ).fetchone()[0]
    position  = ahead + 1
    wait_mins = ahead * MINS_PER_TOKEN

    # ── Step 5: Compute generated_str and meet_time_str — THE SINGLE PLACE ───
    generated_dt  = parse_ist_str(created_at_ist)   # parse what we just stored
    generated_str = fmt_dt(generated_dt)             # "22 Mar 2026, 10:30 PM IST"

    meet_dt       = calc_meeting_time(appt_date, wait_mins)   # uses appointment_date
    meet_time_str = fmt_dt(meet_dt)                          # "23 Mar 2026, 09:05 AM IST"

    # ── Step 6: Fetch patient, send notification (same strings as dashboard) ──
    patient = conn.execute('SELECT * FROM patients WHERE id=?',(pid,)).fetchone()
    conn.close()

    if patient:
        patient_dict = {k: patient[k] for k in patient.keys()}
        doc_dict     = {k: doc[k] for k in doc.keys()}
        print(f"  📧 Token #{tnum} | generated={generated_str} | meeting={meet_time_str}")
        # Email/WhatsApp: exact same strings as what dashboard will show
        notify_token_generated(
            patient_dict, doc_dict, tnum, doc['department'],
            wait_mins, generated_str, meet_time_str, is_next_day=is_next_day
        )
        if wait_mins > 3:
            schedule_reminder('token', patient_dict, doc_dict['name'],
                              doc['department'], token_number=tnum, wait_minutes=wait_mins)
    else:
        print("  ⚠️  Patient not found for notification")

    if is_next_day:
        flash(
            f'Token #{tnum} generated! Hospital is closed — '
            f'your appointment is tomorrow ({fmt_date(appt_date)}). '
            f'Est. meeting: {meet_time_str}',
            'info'
        )
    else:
        flash(f'Token #{tnum} generated for {doc["name"]}! Est. meeting: {meet_time_str}', 'success')

    session['show_feedback'] = True
    return redirect(url_for('patient_dashboard'))

# ─────────────────────────────── APPOINTMENT BOOKING ─────────────────────────
@app.route('/patient/book_appointment', methods=['GET','POST'])
def book_appointment():
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    pid=session['patient_id']; conn=get_db()
    if request.method=='POST':
        did  =request.form.get('doctor_id','')
        adate=request.form.get('date','').strip()
        atime=request.form.get('time','').strip()
        atype=request.form.get('appointment_type','').strip()
        notes=request.form.get('notes','').strip()
        doc  =conn.execute('SELECT * FROM doctors WHERE id=?',(did,)).fetchone()
        if not doc:
            flash('Invalid doctor.','error')
        else:
            conn.execute(
                'INSERT INTO appointments(patient_id,doctor_id,department,appointment_type,date,time,status,notes,created_at) VALUES(?,?,?,?,?,?,?,?,?)',
                (pid,did,doc['department'],atype,adate,atime,'Scheduled',notes,ist_str_now())
            )
            conn.commit()
            try:
                patient=conn.execute('SELECT * FROM patients WHERE id=?',(pid,)).fetchone()
                if patient:
                    pd={k:patient[k] for k in patient.keys()}; dd={k:doc[k] for k in doc.keys()}
                    notify_appointment_booked(pd,dd,atype,adate,atime,notes)
                    schedule_reminder('appointment',pd,doc['name'],doc['department'],appt_date=adate,appt_time=atime)
            except Exception as e:
                print(f"  ⚠️  Appointment notification error: {e}")
            conn.close()
            flash(f"Appointment booked with {doc['name']} on {adate} at {atime}!",'success')
            return redirect(url_for('patient_dashboard'))
    doctors    =conn.execute('SELECT * FROM doctors ORDER BY department,name').fetchall()
    conn.close()
    departments=list(set([d['department'] for d in doctors]))
    today      =now_ist().strftime('%Y-%m-%d')
    times      =['09:00','09:30','10:00','10:30','11:00','11:30','12:00',
                 '14:00','14:30','15:00','15:30','16:00','16:30','17:00','18:00','18:30','19:00','19:30','20:00','20:30']
    return render_template('book_appointment.html',doctors=doctors,departments=departments,today=today,times=times)

@app.route('/patient/cancel_appointment/<int:appt_id>', methods=['POST'])
def cancel_appointment(appt_id):
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    conn=get_db()
    conn.execute('UPDATE appointments SET status="Cancelled" WHERE id=? AND patient_id=?',(appt_id,session['patient_id']))
    conn.commit(); conn.close(); flash('Appointment cancelled.','info')
    return redirect(url_for('patient_dashboard'))

# ─────────────────────────────── AI SYMPTOM CHECKER ──────────────────────────
@app.route('/patient/symptom_checker')
def symptom_checker():
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    return render_template('symptom_checker.html',departments=DEPARTMENTS)

@app.route('/api/ai/check_symptoms', methods=['POST'])
def api_check_symptoms():
    if session.get('role')!='patient': return jsonify({'error':'Unauthorized'}),401
    try:
        symptoms=(request.get_json() or {}).get('symptoms','').strip()
        if not symptoms: return jsonify({'error':'No symptoms'}),400
        sys_p="""You are a hospital triage assistant.
Based on symptoms, suggest a department from ONLY: General OPD, Cardiology, Orthopedic, Dermatology, Neurology.
Respond ONLY in this exact JSON (no markdown):
{"department":"<dept>","reason":"<1-2 sentences>","urgency":"<Low/Medium/High>","tips":"<1-2 self-care tips>"}"""
        raw=gemini(f"Patient symptoms: {symptoms}",system=sys_p)
        try:
            clean=raw.strip()
            if clean.startswith('```'): clean=clean.split('```')[1]; clean=clean[4:] if clean.startswith('json') else clean
            result=json.loads(clean.strip())
        except:
            result={'department':'General OPD','reason':raw[:200],'urgency':'Medium','tips':'Please consult a doctor.'}
        conn=get_db()
        docs=conn.execute('SELECT id,name FROM doctors WHERE department=? ORDER BY name',(result.get('department','General OPD'),)).fetchall()
        conn.close()
        result['doctors']=[{'id':d['id'],'name':d['name']} for d in docs]
        return jsonify(result)
    except Exception as e:
        print(f"  ⚠️  Symptom check error: {e}")
        return jsonify({'error':'Unable to process. Please try again.'}),500

# ─────────────────────────────── AI CHAT ─────────────────────────────────────
@app.route('/patient/chat')
def patient_chat():
    if session.get('role')!='patient': return redirect(url_for('patient_login'))
    pid=session['patient_id']; conn=get_db()
    history=conn.execute('SELECT role,message FROM chat_history WHERE patient_id=? ORDER BY id',(pid,)).fetchall()
    conn.close()
    return render_template('patient_chat.html',history=history)

@app.route('/api/ai/chat', methods=['POST'])
def api_chat():
    if session.get('role')!='patient': return jsonify({'error':'Unauthorized'}),401
    try:
        pid=session['patient_id']; msg=(request.get_json() or {}).get('message','').strip()
        if not msg: return jsonify({'error':'Empty'}),400
        conn=get_db()
        conn.execute('INSERT INTO chat_history(patient_id,role,message,created_at) VALUES(?,?,?,?)',(pid,'user',msg,ist_str_now()))
        hist=conn.execute('SELECT role,message FROM chat_history WHERE patient_id=? ORDER BY id DESC LIMIT 10',(pid,)).fetchall()
        conn.commit()
        conv='\n'.join([f"{h['role'].upper()}: {h['message']}" for h in reversed(hist)])
        sys_p="""You are MediBot, a friendly hospital AI assistant at SmartQueue Hospital.

RESPONSE FORMAT RULES (strictly follow):
• Keep answers SHORT — maximum 4-6 bullet points or 3 sentences.
• Use bullet points (•) for lists, causes, symptoms, or steps.
• Never write long paragraphs.
• Bold important medical terms using **bold**.
• Always end with: "Consult a doctor for proper diagnosis."

EXAMPLE format for a health question:
**Chest Pain could indicate:**
• Heart-related issue (Cardiology)
• Acid reflux or gastritis
• Muscle strain

**Recommended:** Visit Cardiology or General OPD.
Consult a doctor for proper diagnosis.

Departments: General OPD, Cardiology, Orthopedic, Dermatology, Neurology.
Never diagnose definitively. Be warm, concise, and reassuring."""
        reply=gemini(conv,system=sys_p)
        formatted=format_bot_response(reply)
        conn.execute('INSERT INTO chat_history(patient_id,role,message,created_at) VALUES(?,?,?,?)',(pid,'assistant',reply,ist_str_now()))
        conn.commit(); conn.close()
        return jsonify({'reply':formatted})
    except Exception as e:
        print(f"  ⚠️  Chat error: {e}")
        return jsonify({'reply':"I'm having a connection issue. Please try again."}),200

@app.route('/api/ai/clear_chat', methods=['POST'])
def clear_chat():
    if session.get('role')!='patient': return jsonify({'error':'Unauthorized'}),401
    conn=get_db(); conn.execute('DELETE FROM chat_history WHERE patient_id=?',(session['patient_id'],)); conn.commit(); conn.close()
    return jsonify({'status':'cleared'})

# ─────────────────────────────── PRESCRIPTION ANALYSIS ───────────────────────
@app.route('/api/ai/analyze_prescription', methods=['POST'])
def analyze_prescription():
    if session.get('role')!='patient': return jsonify({'error':'Unauthorized'}),401
    try:
        medicine_name=request.form.get('medicine_name','').strip()
        image_file   =request.files.get('prescription_image')
        if medicine_name:
            prompt=f"""A patient wants to know about the medicine: "{medicine_name}"
Please explain clearly:
1. **What it is** — what this medicine is used to treat
2. **How to take it** — typical dose and timing (morning/night/with food etc.)
3. **Common side effects** — list 2-3 things to watch out for
4. **Important warnings** — when not to take it, or special precautions
5. **Storage** — how to store it properly
Keep it simple, friendly, and easy to understand. Always remind: Follow your doctor's prescription exactly."""
            sys_p="""You are MediBot, a helpful medical assistant. Explain medicines in simple, clear language.
Use **bold** for medicine names and key instructions. Always end with: "Please follow your doctor's instructions exactly." """
            reply=gemini(prompt,system=sys_p)
        elif image_file and image_file.filename:
            img_bytes=image_file.read()
            if len(img_bytes) > 5*1024*1024:
                return jsonify({'reply':'⚠️ Image too large. Please upload under 5MB.'}),200
            img_b64=base64.b64encode(img_bytes).decode('utf-8'); mime_type=image_file.content_type or 'image/jpeg'
            try:
                chat_resp=client.chat.completions.create(
                    messages=[{"role":"user","content":[
                        {"type":"image_url","image_url":{"url":f"data:{mime_type};base64,{img_b64}"}},
                        {"type":"text","text":"""Analyze this prescription image:
1. **Medicines listed** — name each medicine visible
2. **Dosage & Timing** — how much and when to take each
3. **Duration** — how many days if mentioned
4. **Special instructions** — any warnings or notes
5. **General advice** — basic care tips
Use **bold** for medicine names. Remind: Follow doctor's instructions exactly."""}
                    ]}],
                    model="meta-llama/llama-4-scout-17b-16e-instruct", max_tokens=1024,
                )
                reply=chat_resp.choices[0].message.content
            except Exception as vision_err:
                print(f"  ⚠️  Vision model error: {vision_err}")
                reply=("📋 I see you uploaded a prescription!\n\nMy image-reading feature needs an upgraded API plan. "
                       "However, you can **type any medicine name** and I'll explain it in detail!\n\n"
                       "💊 Try: *Paracetamol*, *Metformin*, *Amoxicillin*, etc.")
        else:
            return jsonify({'reply':'Please upload an image or type a medicine name.'}),200
        reply=format_bot_response(reply)
        return jsonify({'reply':reply})
    except Exception as e:
        print(f"  ⚠️  Prescription analysis error: {e}")
        return jsonify({'reply':'Sorry, could not analyze. Please type the medicine name instead.'})

# ─────────────────────────────── DOCTOR AUTH ─────────────────────────────────
@app.route('/doctor/register', methods=['GET','POST'])
def doctor_register():
    if request.method=='POST':
        n,e,p,d=request.form['name'].strip(),request.form['email'].strip().lower(),request.form['password'],request.form['department']
        if not all([n,e,p,d]): flash('All fields required.','error'); return render_template('doctor_register.html',departments=DEPARTMENTS)
        conn=get_db()
        try:
            conn.execute('INSERT INTO doctors(name,email,password,department,status) VALUES(?,?,?,?,?)',(n,e,hp(p),d,'pending'))
            conn.commit(); flash('✅ Registration submitted! Pending admin approval.','info')
            return redirect(url_for('doctor_login'))
        except sqlite3.IntegrityError: flash('Email already registered.','error')
        finally: conn.close()
    return render_template('doctor_register.html',departments=DEPARTMENTS)

@app.route('/doctor/login', methods=['GET','POST'])
def doctor_login():
    if request.method=='POST':
        e,p=request.form['email'].strip().lower(),request.form['password']
        conn=get_db(); doc=conn.execute('SELECT * FROM doctors WHERE email=? AND password=?',(e,hp(p))).fetchone(); conn.close()
        if not doc: flash('Invalid email or password.','error')
        elif doc['status']=='pending': flash('⏳ Your account is pending admin approval.','warning')
        elif doc['status']=='rejected': flash('❌ Your registration has been rejected. Contact administrator.','error')
        else:
            session.update({'doctor_id':doc['id'],'doctor_name':doc['name'],'doctor_dept':doc['department'],'role':'doctor'})
            return redirect(url_for('doctor_dashboard'))
    return render_template('doctor_login.html')

@app.route('/doctor/logout')
def doctor_logout(): session.clear(); return redirect(url_for('home'))

@app.route('/doctor/dashboard')
def doctor_dashboard():
    if session.get('role')!='doctor': return redirect(url_for('doctor_login'))
    did=session['doctor_id']; conn=get_db()
    waiting     =conn.execute('SELECT t.*,p.name as patient_name,p.age,p.gender FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.doctor_id=? AND t.status="waiting" ORDER BY t.token_number',(did,)).fetchall()
    current     =conn.execute('SELECT t.*,p.name as patient_name,p.age,p.gender,p.blood_group FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.doctor_id=? AND t.status="called" ORDER BY t.token_number LIMIT 1',(did,)).fetchone()
    done_today  =conn.execute('SELECT COUNT(*) FROM tokens WHERE doctor_id=? AND status="completed" AND DATE(created_at)=?',(did,now_ist().strftime('%Y-%m-%d'))).fetchone()[0]
    recent_rec  =conn.execute('SELECT mr.*,p.name as patient_name FROM medical_records mr JOIN patients p ON mr.patient_id=p.id WHERE mr.doctor_id=? ORDER BY mr.created_at DESC LIMIT 5',(did,)).fetchall()
    todays_appts=conn.execute('SELECT a.*,p.name as patient_name FROM appointments a JOIN patients p ON a.patient_id=p.id WHERE a.doctor_id=? AND a.date=? AND a.status="Scheduled" ORDER BY a.time',(did,now_ist().strftime('%Y-%m-%d'))).fetchall()
    conn.close()
    return render_template('doctor_dashboard.html',waiting=waiting,current=current,
                           completed_today=done_today,recent_records=recent_rec,todays_appts=todays_appts)

@app.route('/doctor/add_record', methods=['GET','POST'])
def add_record():
    if session.get('role')!='doctor': return redirect(url_for('doctor_login'))
    did=session['doctor_id']; conn=get_db()
    if request.method=='POST':
        pid=request.form['patient_id']; diag=request.form['diagnosis'].strip(); meds=request.form['medicines'].strip()
        bp=request.form.get('blood_pressure','').strip(); pulse=request.form.get('pulse','') or 0
        temp=request.form.get('temperature','') or 0; weight=request.form.get('weight','') or 0
        vdate=request.form.get('visit_date', now_ist().strftime('%Y-%m-%d'))
        fdate=request.form.get('followup_date',''); notes=request.form.get('notes','').strip()
        conn.execute('INSERT INTO medical_records(patient_id,doctor_id,department,diagnosis,medicines_prescribed,blood_pressure,pulse_bpm,temperature_f,weight_kg,visit_date,followup_date,notes,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (pid,did,session['doctor_dept'],diag,meds,bp,pulse,temp,weight,vdate,fdate,notes,ist_str_now()))
        conn.commit(); flash('Medical record saved!','success'); conn.close()
        return redirect(url_for('doctor_dashboard'))
    patients=conn.execute('SELECT id,name,age,gender FROM patients ORDER BY name').fetchall()
    today=now_ist().strftime('%Y-%m-%d'); conn.close()
    return render_template('add_record.html',patients=patients,today=today)

@app.route('/api/ai/queue_insights')
def queue_insights():
    if session.get('role')!='doctor': return jsonify({'error':'Unauthorized'}),401
    try:
        did=session['doctor_id']; conn=get_db()
        waiting=conn.execute('SELECT t.token_number,t.symptom,t.created_at,p.name as patient_name FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.doctor_id=? AND t.status="waiting" ORDER BY t.token_number',(did,)).fetchall()
        done   =conn.execute('SELECT COUNT(*) FROM tokens WHERE doctor_id=? AND status="completed" AND DATE(created_at)=?',(did,now_ist().strftime('%Y-%m-%d'))).fetchone()[0]
        conn.close()
        if not waiting: return jsonify({'insight':'✅ Queue is empty! Great work today.'})
        info  ='\n'.join([f"- #{w['token_number']}: {w['patient_name']} | {w['symptom']} | since {w['created_at'][:16]}" for w in waiting])
        prompt=f"Doctor: {session['doctor_name']} | Dept: {session['doctor_dept']}\nDone: {done} | Waiting: {len(waiting)}\n{info}\nGive a 3-4 sentence professional queue insight with workload summary and one practical tip."
        return jsonify({'insight':gemini(prompt),'count':len(waiting),'est_time':len(waiting)*MINS_PER_TOKEN})
    except Exception as e:
        return jsonify({'insight':f'Unable to get insights: {e}'})

@app.route('/doctor/call_next', methods=['POST'])
def call_next():
    if session.get('role')!='doctor': return redirect(url_for('doctor_login'))
    did=session['doctor_id']; conn=get_db()
    cur=conn.execute('SELECT t.*,p.name,p.email,p.phone,p.lang FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.doctor_id=? AND t.status="called" LIMIT 1',(did,)).fetchone()
    if cur:
        doc=conn.execute('SELECT * FROM doctors WHERE id=?',(did,)).fetchone()
        try: notify_token_completed({'name':cur['name'],'email':cur['email'],'phone':cur['phone'],'lang':cur['lang']},dict(doc),cur['token_number'])
        except Exception as e: print(f"  ⚠️  Complete notify error: {e}")
    conn.execute('UPDATE tokens SET status="completed" WHERE doctor_id=? AND status="called"',(did,))
    nxt=conn.execute('SELECT id FROM tokens WHERE doctor_id=? AND status="waiting" ORDER BY token_number LIMIT 1',(did,)).fetchone()
    if nxt:
        conn.execute('UPDATE tokens SET status="called" WHERE id=?',(nxt['id'],))
        ti=conn.execute('SELECT t.*,p.name,p.email,p.phone,p.lang FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.id=? LIMIT 1',(nxt['id'],)).fetchone()
        if ti:
            doc=conn.execute('SELECT * FROM doctors WHERE id=?',(did,)).fetchone()
            try: notify_token_called({'name':ti['name'],'email':ti['email'],'phone':ti['phone'],'lang':ti['lang']},dict(doc),ti['token_number'],ti['department'])
            except Exception as e: print(f"  ⚠️  Call notify error: {e}")
        flash('Next patient called!','success')
    else:
        flash('No more patients in queue.','info')
    conn.commit(); conn.close()
    return redirect(url_for('doctor_dashboard'))

@app.route('/doctor/complete_current', methods=['POST'])
def complete_current():
    if session.get('role')!='doctor': return redirect(url_for('doctor_login'))
    did=session['doctor_id']; conn=get_db()
    cur=conn.execute('SELECT t.*,p.name,p.email,p.phone,p.lang FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.doctor_id=? AND t.status="called" LIMIT 1',(did,)).fetchone()
    if cur:
        doc=conn.execute('SELECT * FROM doctors WHERE id=?',(did,)).fetchone()
        try: notify_token_completed({'name':cur['name'],'email':cur['email'],'phone':cur['phone'],'lang':cur['lang']},dict(doc),cur['token_number'])
        except Exception as e: print(f"  ⚠️  Complete notify error: {e}")
    conn.execute('UPDATE tokens SET status="completed" WHERE doctor_id=? AND status="called"',(did,))
    conn.commit(); conn.close(); flash('Patient completed.','success')
    return redirect(url_for('doctor_dashboard'))

# ─────────────────────────────── ADMIN ───────────────────────────────────────
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        u=request.form.get('username','').strip(); p=request.form.get('password','')
        if u==ADMIN_USERNAME and p==ADMIN_PASSWORD:
            session.update({'role':'admin','admin_name':'Administrator'}); return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.','error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout(): session.clear(); return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role')!='admin': return redirect(url_for('admin_login'))
    conn=get_db()
    today_ist = now_ist().strftime('%Y-%m-%d')
    stats={
        'total_doctors':   conn.execute('SELECT COUNT(*) FROM doctors WHERE status="approved"').fetchone()[0],
        'pending_doctors': conn.execute('SELECT COUNT(*) FROM doctors WHERE status="pending"').fetchone()[0],
        'total_patients':  conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0],
        'total_tokens':    conn.execute('SELECT COUNT(*) FROM tokens').fetchone()[0],
        'waiting':         conn.execute('SELECT COUNT(*) FROM tokens WHERE status="waiting"').fetchone()[0],
        'completed_today': conn.execute('SELECT COUNT(*) FROM tokens WHERE status="completed" AND DATE(created_at)=?',(today_ist,)).fetchone()[0],
        'appointments':    conn.execute('SELECT COUNT(*) FROM appointments WHERE status="Scheduled"').fetchone()[0],
    }
    doctors        =conn.execute('SELECT d.*,COUNT(t.id) as total_tokens FROM doctors d LEFT JOIN tokens t ON d.id=t.doctor_id GROUP BY d.id ORDER BY d.status DESC,d.department,d.name').fetchall()
    patients       =conn.execute('SELECT * FROM patients ORDER BY name LIMIT 50').fetchall()
    raw_tokens     =conn.execute('SELECT t.*,p.name as patient_name,d.name as doctor_name FROM tokens t JOIN patients p ON t.patient_id=p.id JOIN doctors d ON t.doctor_id=d.id ORDER BY t.created_at DESC LIMIT 20').fetchall()
    dept_stats     =conn.execute('SELECT department,COUNT(*) as cnt FROM tokens WHERE status="waiting" GROUP BY department').fetchall()
    pending_doctors=conn.execute('SELECT * FROM doctors WHERE status="pending" ORDER BY rowid DESC').fetchall()
    conn.close()
    # Pre-format timestamps for admin token list
    recent_tokens = []
    for tk in raw_tokens:
        recent_tokens.append({
            'id':           tk['id'],
            'token_number': tk['token_number'],
            'patient_name': tk['patient_name'],
            'doctor_name':  tk['doctor_name'],
            'department':   tk['department'],
            'status':       tk['status'],
            'created_ist':  fmt_dt(parse_ist_str(tk['created_at'])),  # pre-formatted
        })
    return render_template('admin_dashboard.html', stats=stats, doctors=doctors, patients=patients,
                           recent_tokens=recent_tokens, dept_stats=dept_stats, departments=DEPARTMENTS,
                           pending_doctors=pending_doctors)

@app.route('/admin/approve_doctor/<int:did>', methods=['POST'])
def admin_approve_doctor(did):
    if session.get('role')!='admin': return redirect(url_for('admin_login'))
    conn=get_db(); conn.execute('UPDATE doctors SET status="approved" WHERE id=?',(did,))
    doc=conn.execute('SELECT name FROM doctors WHERE id=?',(did,)).fetchone(); conn.commit(); conn.close()
    flash(f'✅ Dr. {doc["name"]} approved.','success'); return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject_doctor/<int:did>', methods=['POST'])
def admin_reject_doctor(did):
    if session.get('role')!='admin': return redirect(url_for('admin_login'))
    conn=get_db(); conn.execute('UPDATE doctors SET status="rejected" WHERE id=?',(did,))
    doc=conn.execute('SELECT name FROM doctors WHERE id=?',(did,)).fetchone(); conn.commit(); conn.close()
    flash(f'❌ Dr. {doc["name"]} rejected.','info'); return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_doctor/<int:did>', methods=['POST'])
def admin_delete_doctor(did):
    if session.get('role')!='admin': return redirect(url_for('admin_login'))
    conn=get_db(); conn.execute('DELETE FROM doctors WHERE id=?',(did,)); conn.commit(); conn.close()
    flash('Doctor removed.','success'); return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_patient/<int:pid>', methods=['POST'])
def admin_delete_patient(pid):
    if session.get('role')!='admin': return redirect(url_for('admin_login'))
    conn=get_db(); conn.execute('DELETE FROM patients WHERE id=?',(pid,)); conn.commit(); conn.close()
    flash('Patient removed.','success'); return redirect(url_for('admin_dashboard'))

# ─────────────────────────────── DISPLAY ─────────────────────────────────────
@app.route('/display')
def display(): return render_template('display.html',departments=DEPARTMENTS)

@app.route('/api/display_data')
def display_data():
    dept=request.args.get('dept',''); conn=get_db()
    docs=conn.execute('SELECT * FROM doctors WHERE department=? ORDER BY name',(dept,)).fetchall() if dept \
         else conn.execute('SELECT * FROM doctors ORDER BY department,name').fetchall()
    data=[]
    for doc in docs:
        cur=conn.execute('SELECT t.token_number,p.name as pn FROM tokens t JOIN patients p ON t.patient_id=p.id WHERE t.doctor_id=? AND t.status="called" LIMIT 1',(doc['id'],)).fetchone()
        nxt=conn.execute('SELECT token_number FROM tokens WHERE doctor_id=? AND status="waiting" ORDER BY token_number LIMIT 1',(doc['id'],)).fetchone()
        wc =conn.execute('SELECT COUNT(*) FROM tokens WHERE doctor_id=? AND status="waiting"',(doc['id'],)).fetchone()[0]
        data.append({'doctor_name':doc['name'],'department':doc['department'],
                     'current_token':cur['token_number'] if cur else None,
                     'current_patient':cur['pn'] if cur else None,
                     'next_token':nxt['token_number'] if nxt else None,
                     'waiting_count':wc})
    conn.close()
    return jsonify({'doctors':data, 'timestamp': fmt_dt(now_ist(), include_date=False)})

@app.route('/api/doctors_by_dept')
def doctors_by_dept():
    dept=request.args.get('dept',''); conn=get_db()
    docs=conn.execute('SELECT id,name FROM doctors WHERE department=? ORDER BY name',(dept,)).fetchall(); conn.close()
    return jsonify([{'id':d['id'],'name':d['name']} for d in docs])

@app.route('/api/search_doctors')
def search_doctors():
    q=request.args.get('q','').strip(); dept=request.args.get('dept',''); conn=get_db()
    if q and dept:   docs=conn.execute('SELECT * FROM doctors WHERE (name LIKE ? OR qualification LIKE ?) AND department=? ORDER BY name',(f'%{q}%',f'%{q}%',dept)).fetchall()
    elif q:          docs=conn.execute('SELECT * FROM doctors WHERE name LIKE ? OR department LIKE ? OR qualification LIKE ? ORDER BY name',(f'%{q}%',f'%{q}%',f'%{q}%')).fetchall()
    elif dept:       docs=conn.execute('SELECT * FROM doctors WHERE department=? ORDER BY name',(dept,)).fetchall()
    else:            docs=conn.execute('SELECT * FROM doctors ORDER BY department,name').fetchall()
    conn.close()
    return jsonify([{'id':d['id'],'name':d['name'],'department':d['department'],
                     'qualification':d['qualification'],'experience_years':d['experience_years']} for d in docs])

# ─────────────────────────────── TEST ROUTES ─────────────────────────────────
# ─────────────────────────────── FEEDBACK ───────────────────────────────────
@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    """Receive feedback from patient UI — logs to console, stores in simple table."""
    try:
        data    = request.get_json() or {}
        rating  = int(data.get('rating', 0))
        comment = str(data.get('comment', '')).strip()[:500]
        source  = str(data.get('source', 'unknown'))
        patient_id = session.get('patient_id')

        # Store in DB (best-effort; never crash)
        try:
            conn = get_db(); c = conn.cursor()
            # Create table if not exists (migration-safe)
            c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER, rating INTEGER, comment TEXT, source TEXT,
                created_at TEXT DEFAULT '')''')
            c.execute('INSERT INTO feedback(patient_id,rating,comment,source,created_at) VALUES(?,?,?,?,?)',
                      (patient_id, rating, comment, source, ist_str_now()))
            conn.commit(); conn.close()
        except Exception as db_e:
            print(f"  ⚠️  Feedback DB error (non-critical): {db_e}")

        print(f"  ⭐ Feedback — patient={patient_id} rating={rating}/5 source={source} comment={comment[:60]}")
        return jsonify({'status': 'ok', 'message': 'Thank you for your feedback!'})
    except Exception as e:
        print(f"  ⚠️  Feedback error: {e}")
        return jsonify({'status': 'error'}), 500


@app.route('/test_time')
def test_time():
    """Debug route to verify time system is working correctly."""
    n = now_ist()
    appt_date, is_next_day = token_appointment_info()
    pos1_meet  = calc_meeting_time(appt_date, 1)
    pos4_meet  = calc_meeting_time(appt_date, 4)
    lines = [
        "=== SmartQueue Time System Verification ===",
        f"Current IST:         {fmt_dt(n)}",
        f"Hospital open:       {'YES' if is_hospital_open() else 'NO — tokens go to next day'}",
        f"Token appt date:     {appt_date} {'(NEXT DAY)' if is_next_day else '(TODAY)'}",
        f"ist_str_now():       {ist_str_now()}",
        "",
        "=== Meeting Time Examples ===",
        f"Position 1 meeting:  {fmt_dt(pos1_meet)}",
        f"Position 4 meeting:  {fmt_dt(pos4_meet)}",
        f"Position 10 meeting: {fmt_dt(calc_meeting_time(appt_date, 10))}",
        "",
        "=== parse_ist_str() roundtrip ===",
        f"Store:  {ist_str_now()}",
        f"Parse:  {fmt_dt(parse_ist_str(ist_str_now()))}",
        "",
        "=== Email Config ===",
        f"GMAIL_ADDRESS: {GMAIL_ADDRESS}",
        f"Configured:    {'YES' if 'your_gmail' not in GMAIL_ADDRESS else 'NO'}",
    ]
    return "<pre style='font:14px monospace;padding:20px;line-height:2;background:#0a1020;color:#00d4ff;'>" + "\n".join(lines) + "</pre>"

@app.route('/test_email')
def test_email():
    lines=["=== Email Config ===", f"GMAIL_ADDRESS = {GMAIL_ADDRESS}",
           "Configured = "+("YES ✅" if 'your_gmail' not in GMAIL_ADDRESS else "NO ❌"), "",
           f"Current IST: {fmt_dt(now_ist())}"]
    if 'your_gmail' not in GMAIL_ADDRESS:
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as srv: srv.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
            lines.append("SMTP login: SUCCESS ✅")
            send_email(GMAIL_ADDRESS, "SmartQueue Test", f"<h2>Email works!</h2><p>IST time: {fmt_dt(now_ist())}</p>")
            lines.append(f"Test email sent to {GMAIL_ADDRESS}")
        except Exception as ex: lines.append(f"ERROR: {ex}")
    return "<pre style='font:14px monospace;padding:20px;line-height:1.8;'>" + "\n".join(lines) + "</pre>"

@app.route('/test_whatsapp')
def test_whatsapp():
    lines=["=== WhatsApp Config ===",
           "TWILIO_SID = "+(TWILIO_SID[:10]+"..." if len(TWILIO_SID)>10 else TWILIO_SID),
           "Configured = "+("YES ✅" if 'your_twilio' not in TWILIO_SID else "NO ❌")]
    if 'your_twilio' not in TWILIO_SID:
        phone=request.args.get('phone','')
        if phone:
            send_whatsapp(phone, f"🏥 *SmartQueue*\n✅ WhatsApp working!\n🕐 {fmt_dt(now_ist())}")
            lines.append(f"Sent to {phone}!")
        else:
            lines.append("Add ?phone=YOUR_NUMBER to test")
    return "<pre style='font:14px monospace;padding:20px;line-height:1.8;'>" + "\n".join(lines) + "</pre>"

# ─────────────────────────────── MAIN ────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    n = now_ist()
    appt_date, is_next_day = token_appointment_info()
    print("\n" + "="*64)
    print("  SMARTQUEUE HOSPITAL + AI  — RUNNING")
    print("="*64)
    print(f"  IST now:      {fmt_dt(n)}")
    print(f"  Hospital:     {HOSPITAL_OPEN_HOUR}:00 AM – {HOSPITAL_CLOSE_HOUR}:00 PM IST")
    print(f"  Status:       {'OPEN ✅' if is_hospital_open() else 'CLOSED — tokens → NEXT DAY'}")
    print(f"  Token date:   {appt_date} {'(tomorrow)' if is_next_day else '(today)'}")
    print(f"  Position-1 meeting: {fmt_dt(calc_meeting_time(appt_date, 1))}")
    print()
    print("  App     ➜  http://127.0.0.1:5000")
    print("  Time    ➜  http://127.0.0.1:5000/test_time")
    print("  Admin   ➜  http://127.0.0.1:5000/admin/login")
    print()
    print("  Admin:   hospitaladmin / AdminSecure@2024")
    print("  Doctor:  anil@hospital.com / doctor123")
    print("  Patient: rajesh1@gmail.com / patient123")
    print("="*64 + "\n")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
