
# ============================================================
# AI-FRAUDGUARD
# PREMIUM NEON CYBER STREAMLIT DASHBOARD
# Phase 6.2 - Threat Intelligence + Risk Gauges
# ============================================================

import os
import sys
import html
import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# PROJECT IMPORTS
# ============================================================

try:
    from src.prediction.fraud_predictor import FraudPredictor
except Exception as e:
    FraudPredictor = None
    PREDICTOR_IMPORT_ERROR = str(e)


try:
    from src.risk.risk_engine import calculate_risk
except Exception as e:
    calculate_risk = None
    RISK_IMPORT_ERROR = str(e)


try:
    from ai.investigator import FraudInvestigator
except Exception as e:
    FraudInvestigator = None
    AI_IMPORT_ERROR = str(e)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI-FraudGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM NEON CSS
# ============================================================

st.html(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(0,229,255,.14), transparent 28%),
            radial-gradient(circle at 90% 5%, rgba(139,92,246,.18), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(37,99,235,.12), transparent 35%),
            #050816;
        color:#f8fafc;
    }

    .main .block-container {
        max-width:1500px;
        padding-top:1.5rem;
        padding-bottom:4rem;
    }

    section[data-testid="stSidebar"] {
        background:linear-gradient(180deg,#050817 0%,#090d20 50%,#050816 100%);
        border-right:1px solid rgba(0,229,255,.20);
    }

    section[data-testid="stSidebar"] * {
        color:#dbeafe;
    }

    .sidebar-brand {
        text-align:center;
        padding:10px 5px 22px 5px;
    }

    .sidebar-logo {
        font-size:52px;
        filter:drop-shadow(0 0 10px rgba(0,229,255,.8))
               drop-shadow(0 0 25px rgba(124,58,237,.8));
    }

    .sidebar-title {
        font-size:23px;
        font-weight:900;
        background:linear-gradient(90deg,#00e5ff,#8b5cf6,#38bdf8);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .sidebar-subtitle {
        margin-top:5px;
        font-size:10px;
        color:#64748b;
        letter-spacing:2px;
    }

    .sidebar-engine {
        padding:18px;
        border-radius:18px;
        background:linear-gradient(145deg,rgba(15,23,42,.95),rgba(30,27,75,.75));
        border:1px solid rgba(0,229,255,.18);
        box-shadow:0 10px 35px rgba(0,0,0,.25);
    }

    .engine-title {
        font-size:13px;
        font-weight:800;
        color:#67e8f9;
        margin-bottom:12px;
    }

    .engine-item {
        padding:7px 0;
        font-size:12px;
        color:#cbd5e1;
    }

    .hero {
        position:relative;
        overflow:hidden;
        padding:35px;
        border-radius:26px;
        margin-bottom:25px;
        background:linear-gradient(135deg,rgba(8,15,35,.97),rgba(31,27,75,.92));
        border:1px solid rgba(0,229,255,.28);
        box-shadow:0 0 30px rgba(0,229,255,.08),
                   0 0 70px rgba(124,58,237,.08);
    }

    .hero-title {
        position:relative;
        z-index:2;
        font-size:45px;
        font-weight:900;
        background:linear-gradient(90deg,#00e5ff,#8b5cf6,#38bdf8);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .hero-subtitle {
        position:relative;
        z-index:2;
        color:#94a3b8;
        font-size:16px;
        margin-top:8px;
    }

    .system-status {
        position:relative;
        z-index:2;
        margin-top:17px;
        font-size:12px;
        color:#67e8f9;
        letter-spacing:1px;
    }

    .section-title {
        font-size:23px;
        font-weight:900;
        margin:25px 0 15px 0;
        background:linear-gradient(90deg,#f8fafc,#67e8f9);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .metric-card {
        min-height:145px;
        padding:21px;
        border-radius:20px;
        background:linear-gradient(145deg,rgba(15,23,42,.96),rgba(17,24,39,.78));
        border:1px solid rgba(148,163,184,.16);
        box-shadow:inset 0 1px 0 rgba(255,255,255,.04),
                   0 15px 40px rgba(0,0,0,.25);
    }

    .metric-icon {
        font-size:30px;
        margin-bottom:8px;
    }

    .metric-label {
        font-size:11px;
        color:#64748b;
        letter-spacing:1px;
        font-weight:700;
    }

    .metric-value {
        font-size:30px;
        font-weight:900;
        margin-top:6px;
    }

    .glass-card {
        padding:23px;
        border-radius:21px;
        background:linear-gradient(145deg,rgba(15,23,42,.88),rgba(17,24,39,.70));
        border:1px solid rgba(139,92,246,.20);
        box-shadow:0 15px 45px rgba(0,0,0,.24),
                   inset 0 1px 0 rgba(255,255,255,.03);
    }

    .input-card {
        padding:22px;
        border-radius:20px;
        background:linear-gradient(145deg,rgba(8,15,35,.94),rgba(20,25,55,.76));
        border:1px solid rgba(0,229,255,.15);
        box-shadow:0 12px 35px rgba(0,0,0,.22);
    }

    .risk-card {
        padding:28px;
        border-radius:23px;
        text-align:center;
        margin-top:18px;
    }

    .risk-critical {
        background:linear-gradient(135deg,rgba(127,29,29,.80),rgba(35,8,30,.88));
        border:1px solid #ff3864;
        box-shadow:0 0 35px rgba(255,56,100,.18);
    }

    .risk-high {
        background:linear-gradient(135deg,rgba(124,45,18,.80),rgba(40,20,10,.88));
        border:1px solid #fb923c;
        box-shadow:0 0 35px rgba(251,146,60,.16);
    }

    .risk-medium {
        background:linear-gradient(135deg,rgba(113,63,18,.80),rgba(40,35,10,.88));
        border:1px solid #facc15;
        box-shadow:0 0 30px rgba(250,204,21,.12);
    }

    .risk-low {
        background:linear-gradient(135deg,rgba(6,78,59,.80),rgba(5,35,35,.88));
        border:1px solid #22d3ee;
        box-shadow:0 0 30px rgba(34,211,238,.12);
    }

    .risk-icon {
        font-size:44px;
        margin-bottom:5px;
    }

    .risk-title {
        font-size:32px;
        font-weight:900;
        margin:0;
    }

    .risk-score {
        font-size:22px;
        color:#cbd5e1;
        margin-top:7px;
    }

    .risk-status {
        font-size:13px;
        color:#94a3b8;
        margin-top:6px;
    }

    .reason-card {
        padding:14px 16px;
        margin:7px 0;
        border-radius:12px;
        background:rgba(15,23,42,.78);
        border-left:3px solid #00e5ff;
        color:#cbd5e1;
        box-shadow:0 5px 18px rgba(0,0,0,.18);
    }

    .ai-header {
        padding:20px;
        border-radius:18px;
        background:linear-gradient(135deg,rgba(30,27,75,.88),rgba(8,47,73,.72));
        border:1px solid rgba(0,229,255,.30);
        margin-bottom:15px;
    }

    .ai-title {
        font-size:19px;
        font-weight:900;
        color:#67e8f9;
    }

    .ai-description {
        color:#94a3b8;
        font-size:13px;
        margin-top:6px;
    }

    /* PHASE 6.2 - THREAT INTELLIGENCE */

    .gauge-container {
        display:flex;
        justify-content:center;
        align-items:center;
        padding:20px;
    }

    .gauge {
        width:190px;
        height:190px;
        border-radius:50%;
        display:flex;
        justify-content:center;
        align-items:center;
        position:relative;
    }

    .gauge-inner {
        width:145px;
        height:145px;
        border-radius:50%;
        background:#080d1d;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        border:1px solid rgba(255,255,255,.08);
    }

    .gauge-value {
        font-size:32px;
        font-weight:900;
    }

    .gauge-label {
        font-size:10px;
        color:#64748b;
        letter-spacing:1px;
        margin-top:4px;
    }

    .analysis-item {
        padding:18px;
        border-radius:16px;
        background:rgba(15,23,42,.75);
        border:1px solid rgba(34,211,238,.12);
        margin-top:10px;
    }

    .analysis-item-title {
        color:#64748b;
        font-size:11px;
        letter-spacing:1px;
        font-weight:800;
    }

    .analysis-item-value {
        color:#f8fafc;
        font-size:20px;
        font-weight:900;
        margin-top:7px;
    }

    .stButton > button {
        min-height:48px;
        border-radius:13px !important;
        border:1px solid rgba(0,229,255,.38) !important;
        background:linear-gradient(90deg,#0891b2,#7c3aed) !important;
        color:white !important;
        font-weight:900 !important;
        box-shadow:0 0 20px rgba(0,229,255,.12);
    }

    .stButton > button:hover {
        transform:translateY(-2px);
        box-shadow:0 0 30px rgba(0,229,255,.28);
    }

    .stTextInput input,
    .stNumberInput input {
        background:#0b1120 !important;
        color:#f8fafc !important;
        border:1px solid #26324a !important;
        border-radius:11px !important;
    }

    div[data-baseweb="select"] > div {
        background:#0b1120 !important;
        border-radius:11px !important;
    }

    .stDownloadButton > button {
        border-radius:12px !important;
        background:linear-gradient(90deg,#0e7490,#4338ca) !important;
        color:white !important;
        font-weight:800 !important;
    }

    .bulk-dropzone {
        padding:24px;
        border-radius:20px;
        background:linear-gradient(
            145deg,
            rgba(8,15,35,.94),
            rgba(30,27,75,.72)
        );
        border:1px dashed rgba(34,211,238,.38);
        box-shadow:0 12px 35px rgba(0,0,0,.20);
        margin-bottom:18px;
    }

    .bulk-stat {
        padding:18px;
        border-radius:16px;
        background:rgba(15,23,42,.78);
        border:1px solid rgba(139,92,246,.18);
    }


    .analytics-card {
        padding:22px;
        border-radius:20px;
        background:linear-gradient(
            145deg,
            rgba(15,23,42,.92),
            rgba(30,27,75,.72)
        );
        border:1px solid rgba(34,211,238,.16);
        box-shadow:0 14px 40px rgba(0,0,0,.22);
        margin-bottom:18px;
    }

    .analytics-title {
        color:#67e8f9;
        font-size:15px;
        font-weight:900;
        margin-bottom:5px;
    }

    .analytics-subtitle {
        color:#64748b;
        font-size:11px;
        margin-bottom:15px;
    }

    .insight-card {
        padding:17px;
        border-radius:15px;
        background:rgba(15,23,42,.82);
        border-left:3px solid #8b5cf6;
        margin-bottom:10px;
    }

    .insight-label {
        color:#64748b;
        font-size:10px;
        letter-spacing:1px;
        font-weight:800;
    }

    .insight-value {
        color:#f8fafc;
        font-size:19px;
        font-weight:900;
        margin-top:5px;
    }


    .case-badge {
        display:inline-block;
        padding:7px 12px;
        border-radius:999px;
        background:rgba(34,211,238,.10);
        border:1px solid rgba(34,211,238,.22);
        color:#67e8f9;
        font-size:11px;
        font-weight:900;
        letter-spacing:.5px;
        margin:3px;
    }

    .timeline-line {
        border-left:2px solid rgba(34,211,238,.25);
        padding-left:16px;
        margin-left:8px;
    }

    .footer {
        text-align:center;
        padding:35px 10px 10px 10px;
        color:#475569;
        font-size:11px;
    }

    .footer-highlight {
        color:#22d3ee;
        font-weight:800;
    }

    </style>
    """
)




# ============================================================
# PHASE 6.8 - ADMIN MANAGEMENT / LOGIN AUDIT
# ============================================================

ADMIN_DB = os.path.join(BASE_DIR, "data", "admin_registry.db")
os.makedirs(os.path.dirname(ADMIN_DB), exist_ok=True)
CASE_EVIDENCE_DIR = os.path.join(BASE_DIR, "data", "case_evidence")
os.makedirs(CASE_EVIDENCE_DIR, exist_ok=True)


def init_admin_db():
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                username TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                last_login TEXT,
                login_count INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                password_hash TEXT,
                recovery_hash TEXT
            )
            """
        )

        # Upgrade an existing database created before password support.
        try:
            conn.execute("ALTER TABLE admins ADD COLUMN password_hash TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute("ALTER TABLE admins ADD COLUMN recovery_hash TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            conn.execute(
                "ALTER TABLE admins ADD COLUMN role TEXT DEFAULT 'Analyst'"
            )
        except sqlite3.OperationalError:
            pass

        conn.commit()


def register_admin(username):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO admins
            (username, created_at, last_login, login_count, is_active)
            VALUES (?, ?, NULL, 0, 1)
            """,
            (username, now),
        )
        conn.commit()


def record_admin_login(username):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            UPDATE admins
            SET last_login = ?,
                login_count = login_count + 1
            WHERE username = ?
            """,
            (now, username),
        )
        conn.commit()



# ============================================================
# AUDIT LOG / SECURITY MONITORING
# ============================================================

def init_security_db():
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                event_type TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fraud_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                fraud_probability REAL,
                prediction TEXT NOT NULL,
                location TEXT,
                amount REAL,
                merchant_category TEXT,
                device TEXT,
                reason TEXT,
                status TEXT DEFAULT 'OPEN',
                created_at TEXT NOT NULL,
                resolved_at TEXT,
                resolved_by TEXT
            )
            """
        )


        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS investigation_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT UNIQUE NOT NULL,
                alert_id INTEGER,
                transaction_id TEXT NOT NULL,
                title TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT DEFAULT 'OPEN',
                outcome TEXT DEFAULT 'PENDING',
                assigned_to TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                closed_at TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS case_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                username TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS case_evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                evidence_name TEXT NOT NULL,
                evidence_type TEXT NOT NULL,
                description TEXT,
                file_path TEXT,
                file_size INTEGER DEFAULT 0,
                added_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS case_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT NOT NULL,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def log_audit(username, action, status="SUCCESS", details=""):
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT INTO audit_logs
            (username, action, status, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                action,
                status,
                details,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def log_security_event(username, event_type, details=""):
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT INTO security_events
            (username, event_type, details, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (
                username,
                event_type,
                details,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def create_fraud_alert(
    transaction_id,
    severity,
    fraud_probability,
    prediction,
    transaction,
    reason,
):
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT INTO fraud_alerts
            (
                transaction_id,
                severity,
                fraud_probability,
                prediction,
                location,
                amount,
                merchant_category,
                device,
                reason,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'OPEN', ?)
            """,
            (
                str(transaction_id),
                str(severity),
                float(fraud_probability),
                str(prediction),
                str(transaction.get("Location", "")),
                float(transaction.get("Amount", 0) or 0),
                str(transaction.get("Merchant_Category", "")),
                str(transaction.get("Device", "")),
                str(reason),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def get_fraud_alerts(status="ALL", limit=300):
    with sqlite3.connect(ADMIN_DB) as conn:
        if status == "ALL":
            return pd.read_sql_query(
                """
                SELECT
                    id AS Alert_ID,
                    transaction_id AS Transaction_ID,
                    severity AS Severity,
                    fraud_probability AS Fraud_Probability,
                    prediction AS Prediction,
                    location AS Location,
                    amount AS Amount,
                    merchant_category AS Merchant_Category,
                    device AS Device,
                    reason AS Reason,
                    status AS Status,
                    created_at AS Created_At,
                    resolved_at AS Resolved_At,
                    resolved_by AS Resolved_By
                FROM fraud_alerts
                ORDER BY id DESC
                LIMIT ?
                """,
                conn,
                params=(limit,),
            )

        return pd.read_sql_query(
            """
            SELECT
                id AS Alert_ID,
                transaction_id AS Transaction_ID,
                severity AS Severity,
                fraud_probability AS Fraud_Probability,
                prediction AS Prediction,
                location AS Location,
                amount AS Amount,
                merchant_category AS Merchant_Category,
                device AS Device,
                reason AS Reason,
                status AS Status,
                created_at AS Created_At,
                resolved_at AS Resolved_At,
                resolved_by AS Resolved_By
            FROM fraud_alerts
            WHERE status = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(status, limit),
        )


def get_fraud_alert_counts():
    with sqlite3.connect(ADMIN_DB) as conn:
        rows = conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'OPEN' THEN 1 ELSE 0 END) AS open_count,
                SUM(CASE WHEN severity = 'CRITICAL' AND status = 'OPEN'
                         THEN 1 ELSE 0 END) AS critical_count,
                SUM(CASE WHEN severity = 'HIGH' AND status = 'OPEN'
                         THEN 1 ELSE 0 END) AS high_count
            FROM fraud_alerts
            """
        ).fetchone()

    return tuple(int(x or 0) for x in rows)


def resolve_fraud_alert(alert_id, username):
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            UPDATE fraud_alerts
            SET status = 'RESOLVED',
                resolved_at = ?,
                resolved_by = ?
            WHERE id = ?
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                username,
                int(alert_id),
            ),
        )
        conn.commit()


def get_alert_severity(probability):
    probability = float(probability)

    if probability >= 0.70:
        return "CRITICAL"
    if probability >= 0.40:
        return "HIGH"
    if probability >= 0.19:
        return "MEDIUM"
    return "LOW"


def get_alert_reason(transaction, probability):
    reasons = []

    try:
        if float(transaction.get("Amount", 0) or 0) >= 50000:
            reasons.append("Very high transaction amount")
    except (TypeError, ValueError):
        pass

    if str(transaction.get("Device", "")).strip().lower() == "new":
        reasons.append("Transaction from a new device")

    try:
        hour = int(transaction.get("Hour", 0) or 0)
        if hour < 6 or hour >= 23:
            reasons.append("Unusual transaction time")
    except (TypeError, ValueError):
        pass

    try:
        if float(transaction.get("Transaction_Count", 0) or 0) >= 10:
            reasons.append("High transaction frequency")
    except (TypeError, ValueError):
        pass

    try:
        if float(transaction.get("Account_Age_Days", 99999) or 99999) < 180:
            reasons.append("Relatively young account")
    except (TypeError, ValueError):
        pass

    category = str(
        transaction.get("Merchant_Category", "")
    ).strip().lower()
    if category in {"electronics", "jewelry", "shopping"}:
        reasons.append("High-risk merchant category")

    reasons.append(
        f"Machine learning fraud probability: {float(probability):.1f}%"
    )

    return " • ".join(reasons)




def add_case_activity(case_id, username, action, details=""):
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT INTO case_activity
            (case_id, username, action, details, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(case_id),
                str(username),
                str(action),
                str(details),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def add_case_note(case_id, username, note):
    note = str(note).strip()
    if not note:
        return False

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT INTO case_notes
            (case_id, username, note, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (str(case_id), str(username), note, now),
        )
        conn.commit()

    add_case_activity(case_id, username, "NOTE_ADDED", note[:250])
    return True


def get_case_notes(case_id, limit=200):
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT username AS User,
                   note AS Note,
                   created_at AS Timestamp
            FROM case_notes
            WHERE case_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(str(case_id), int(limit)),
        )


def add_case_evidence(case_id, evidence_name, evidence_type,
                      description, file_path, file_size, username):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(ADMIN_DB) as conn:
        cur = conn.execute(
            """
            INSERT INTO case_evidence
            (case_id, evidence_name, evidence_type, description,
             file_path, file_size, added_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(case_id),
                str(evidence_name),
                str(evidence_type),
                str(description or ""),
                str(file_path or ""),
                int(file_size or 0),
                str(username),
                now,
            ),
        )
        evidence_id = cur.lastrowid
        conn.commit()

    add_case_activity(
        case_id,
        username,
        "EVIDENCE_ADDED",
        f"{evidence_name} ({evidence_type})",
    )
    return evidence_id


def get_case_evidence(case_id, limit=200):
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT id AS Evidence_ID,
                   evidence_name AS Evidence,
                   evidence_type AS Type,
                   description AS Description,
                   file_path AS File_Path,
                   file_size AS Size_Bytes,
                   added_by AS Added_By,
                   created_at AS Timestamp
            FROM case_evidence
            WHERE case_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(str(case_id), int(limit)),
        )


def get_case_timeline(case_id, limit=300):
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT username AS User,
                   action AS Action,
                   details AS Details,
                   created_at AS Timestamp
            FROM case_activity
            WHERE case_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(str(case_id), int(limit)),
        )


def build_case_report(case_row, notes_df, evidence_df, timeline_df):
    lines = [
        "AI-FRAUDGUARD — INVESTIGATION CASE REPORT",
        "=" * 62,
        f"Case ID: {case_row['Case_ID']}",
        f"Transaction ID: {case_row['Transaction_ID']}",
        f"Alert ID: {case_row['Alert_ID']}",
        f"Title: {case_row['Title']}",
        f"Priority: {case_row['Priority']}",
        f"Status: {case_row['Status']}",
        f"Outcome: {case_row['Outcome']}",
        f"Assigned Analyst: {case_row['Assigned_To']}",
        f"Created: {case_row['Created_At']}",
        f"Updated: {case_row['Updated_At']}",
        f"Closed: {case_row['Closed_At']}",
        "",
        "CURRENT CASE NOTES",
        "-" * 62,
        str(case_row["Notes"] or ""),
        "",
        "NOTE HISTORY",
        "-" * 62,
    ]

    if notes_df.empty:
        lines.append("No note history.")
    else:
        for _, r in notes_df.iterrows():
            lines.append(
                f"[{r['Timestamp']}] {r['User']}: {r['Note']}"
            )

    lines.extend(["", "EVIDENCE", "-" * 62])
    if evidence_df.empty:
        lines.append("No evidence attached.")
    else:
        for _, r in evidence_df.iterrows():
            lines.append(
                f"#{r['Evidence_ID']} | {r['Evidence']} | {r['Type']} | "
                f"{r['Added_By']} | {r['Timestamp']}"
            )
            if r["Description"]:
                lines.append(f"  Description: {r['Description']}")
            if r["File_Path"]:
                lines.append(f"  File: {r['File_Path']}")

    lines.extend(["", "CASE TIMELINE", "-" * 62])
    if timeline_df.empty:
        lines.append("No activity recorded.")
    else:
        for _, r in timeline_df.iterrows():
            lines.append(
                f"[{r['Timestamp']}] {r['User']} | "
                f"{r['Action']} | {r['Details']}"
            )

    lines.extend([
        "",
        "=" * 62,
        "Generated by AI-FraudGuard",
        "Developed by Mayur Verma",
    ])
    return "\n".join(lines)


def create_investigation_case(alert_id, transaction_id, severity, username):
    case_id = "CASE-" + datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    priority = severity if severity in {"CRITICAL", "HIGH", "MEDIUM", "LOW"} else "MEDIUM"

    with sqlite3.connect(ADMIN_DB) as conn:
        existing = conn.execute(
            "SELECT case_id FROM investigation_cases WHERE alert_id = ?",
            (int(alert_id),),
        ).fetchone()

        if existing:
            return existing[0]

        conn.execute(
            """
            INSERT INTO investigation_cases
            (case_id, alert_id, transaction_id, title, priority, status,
             outcome, assigned_to, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'OPEN', 'PENDING', ?, '', ?, ?)
            """,
            (
                case_id,
                int(alert_id),
                str(transaction_id),
                f"Fraud Investigation - {transaction_id}",
                priority,
                username,
                now,
                now,
            ),
        )
        conn.commit()

    add_case_activity(
        case_id,
        username,
        "CASE_CREATED",
        f"Case created from Alert #{int(alert_id)}",
    )
    return case_id


def get_cases(status="ALL", limit=500):
    with sqlite3.connect(ADMIN_DB) as conn:
        if status == "ALL":
            return pd.read_sql_query(
                """
                SELECT id AS Case_Row, case_id AS Case_ID, alert_id AS Alert_ID,
                       transaction_id AS Transaction_ID, title AS Title,
                       priority AS Priority, status AS Status,
                       outcome AS Outcome, assigned_to AS Assigned_To,
                       notes AS Notes, created_at AS Created_At,
                       updated_at AS Updated_At, closed_at AS Closed_At
                FROM investigation_cases
                ORDER BY id DESC LIMIT ?
                """,
                conn, params=(limit,),
            )

        return pd.read_sql_query(
            """
            SELECT id AS Case_Row, case_id AS Case_ID, alert_id AS Alert_ID,
                   transaction_id AS Transaction_ID, title AS Title,
                   priority AS Priority, status AS Status,
                   outcome AS Outcome, assigned_to AS Assigned_To,
                   notes AS Notes, created_at AS Created_At,
                   updated_at AS Updated_At, closed_at AS Closed_At
            FROM investigation_cases
            WHERE status = ?
            ORDER BY id DESC LIMIT ?
            """,
            conn, params=(status, limit),
        )


def update_case(case_id, status=None, outcome=None, assigned_to=None, notes=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = st.session_state.get("logged_in_admin", "UNKNOWN")

    with sqlite3.connect(ADMIN_DB) as conn:
        row = conn.execute(
            """
            SELECT status, outcome, assigned_to, notes
            FROM investigation_cases
            WHERE case_id = ?
            """,
            (case_id,),
        ).fetchone()

        if not row:
            return False

        old_status, old_outcome, old_assigned, old_notes = row
        new_status = status if status is not None else old_status
        new_outcome = outcome if outcome is not None else old_outcome
        new_assigned = assigned_to if assigned_to is not None else old_assigned
        new_notes = notes if notes is not None else old_notes
        closed_at = now if new_status in {"RESOLVED", "CLOSED"} else None

        conn.execute(
            """
            UPDATE investigation_cases
            SET status=?, outcome=?, assigned_to=?, notes=?,
                updated_at=?, closed_at=?
            WHERE case_id=?
            """,
            (
                new_status,
                new_outcome,
                new_assigned,
                new_notes,
                now,
                closed_at,
                case_id,
            ),
        )
        conn.commit()

    if old_status != new_status:
        add_case_activity(
            case_id,
            username,
            "STATUS_CHANGED",
            f"{old_status} → {new_status}",
        )

    if old_outcome != new_outcome:
        add_case_activity(
            case_id,
            username,
            "OUTCOME_CHANGED",
            f"{old_outcome} → {new_outcome}",
        )

    if (old_assigned or "") != (new_assigned or ""):
        add_case_activity(
            case_id,
            username,
            "ANALYST_ASSIGNED",
            f"{old_assigned or 'Unassigned'} → {new_assigned or 'Unassigned'}",
        )

    if notes is not None and str(notes).strip() and str(old_notes or "").strip() != str(notes).strip():
        add_case_note(case_id, username, notes)

    return True


# ---------- Phase 8.3: Advanced Analytics ----------
def load_alert_analytics():
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT severity, status, location, amount,
                   merchant_category, device, fraud_probability, created_at
            FROM fraud_alerts
            ORDER BY id DESC
            """,
            conn,
        )


# ---------- Phase 8.4: Customer & Device Intelligence ----------
def get_customer_intelligence(transaction_df):
    df = transaction_df.copy()
    if df.empty:
        return pd.DataFrame()

    group_col = "Customer_ID" if "Customer_ID" in df.columns else None
    if group_col:
        return (
            df.groupby(group_col)
            .agg(
                Transactions=("Amount", "count"),
                Total_Amount=("Amount", "sum"),
                Avg_Amount=("Amount", "mean"),
            )
            .reset_index()
            .sort_values("Total_Amount", ascending=False)
        )

    if "Device" in df.columns:
        return (
            df.groupby("Device")
            .agg(
                Transactions=("Amount", "count"),
                Total_Amount=("Amount", "sum"),
                Avg_Amount=("Amount", "mean"),
            )
            .reset_index()
            .sort_values("Transactions", ascending=False)
        )

    return pd.DataFrame()


# ---------- Phase 8.5: Professional Reports ----------
def build_fraud_report(alerts_df, cases_df):
    total = len(alerts_df)
    open_count = int((alerts_df["Status"] == "OPEN").sum()) if not alerts_df.empty else 0
    critical = int((alerts_df["Severity"] == "CRITICAL").sum()) if not alerts_df.empty else 0
    cases = len(cases_df)

    lines = [
        "AI-FRAUDGUARD — FRAUD INTELLIGENCE REPORT",
        "=" * 55,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "SUMMARY",
        f"Total Alerts: {total}",
        f"Open Alerts: {open_count}",
        f"Critical Alerts: {critical}",
        f"Investigation Cases: {cases}",
        "",
        "ALERT DETAILS",
    ]

    if alerts_df.empty:
        lines.append("No alerts recorded.")
    else:
        for _, row in alerts_df.iterrows():
            lines.extend([
                f"Alert #{row['Alert_ID']} | {row['Transaction_ID']}",
                f"Severity: {row['Severity']} | Probability: {row['Fraud_Probability']:.2f}%",
                f"Prediction: {row['Prediction']} | Status: {row['Status']}",
                f"Location: {row['Location']} | Amount: ₹{float(row['Amount']):,.2f}",
                f"Reason: {row['Reason']}",
                "-" * 55,
            ])

    lines.append("")
    lines.append("INVESTIGATION CASES")
    if cases_df.empty:
        lines.append("No investigation cases recorded.")
    else:
        for _, row in cases_df.iterrows():
            lines.append(
                f"{row['Case_ID']} | {row['Transaction_ID']} | "
                f"{row['Priority']} | {row['Status']} | {row['Outcome']}"
            )

    return "\n".join(lines)


# ---------- Phase 8.6: Security Hardening ----------
def check_login_lockout(username, window_minutes=15, max_failures=5):
    cutoff = (datetime.now() - timedelta(minutes=window_minutes)).strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(ADMIN_DB) as conn:
        count = conn.execute(
            """
            SELECT COUNT(*)
            FROM security_events
            WHERE username = ?
              AND event_type = 'LOGIN_FAILED'
              AND timestamp >= ?
            """,
            (username, cutoff),
        ).fetchone()[0]
    return count >= max_failures


def security_event_count(username=None, event_type=None):
    with sqlite3.connect(ADMIN_DB) as conn:
        query = "SELECT COUNT(*) FROM security_events WHERE 1=1"
        params = []
        if username:
            query += " AND username = ?"
            params.append(username)
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        return int(conn.execute(query, params).fetchone()[0])


def logout_user():
    username = st.session_state.get("logged_in_admin")
    if username:
        log_audit(username, "LOGOUT", "SUCCESS", "User logged out")
    for key in ["logged_in", "logged_in_admin", "is_developer"]:
        st.session_state.pop(key, None)
    st.rerun()


def get_audit_logs(limit=300):
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT
                username AS User,
                action AS Action,
                status AS Status,
                details AS Details,
                timestamp AS Timestamp
            FROM audit_logs
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(limit,),
        )


def get_security_events(limit=100):
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT
                username AS User,
                event_type AS Event,
                details AS Details,
                timestamp AS Timestamp
            FROM security_events
            ORDER BY id DESC
            LIMIT ?
            """,
            conn,
            params=(limit,),
        )


def get_security_counts():
    with sqlite3.connect(ADMIN_DB) as conn:
        failed = conn.execute(
            """
            SELECT COUNT(*)
            FROM audit_logs
            WHERE action = 'LOGIN' AND status = 'FAILED'
            """
        ).fetchone()[0]

        total_logins = conn.execute(
            """
            SELECT COUNT(*)
            FROM audit_logs
            WHERE action = 'LOGIN' AND status = 'SUCCESS'
            """
        ).fetchone()[0]

        suspicious = conn.execute(
            "SELECT COUNT(*) FROM security_events"
        ).fetchone()[0]

    return int(total_logins), int(failed), int(suspicious)


def get_admin_registry():
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT
                username AS Admin,
                role AS Role,
                created_at AS Created,
                last_login AS Last_Login,
                login_count AS Login_Count,
                CASE
                    WHEN is_active = 1 THEN 'ACTIVE'
                    ELSE 'DISABLED'
                END AS Status
            FROM admins
            ORDER BY last_login DESC
            """,
            conn,
        )


def get_admin_role(username):
    with sqlite3.connect(ADMIN_DB) as conn:
        row = conn.execute(
            "SELECT role FROM admins WHERE username = ?",
            (username,),
        ).fetchone()

    return row[0] if row and row[0] else "Analyst"


def set_admin_role(username, role):
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            "UPDATE admins SET role = ? WHERE username = ?",
            (role, username),
        )
        conn.commit()


def set_admin_status(username, is_active):
    if username.lower() == DEVELOPER_USERNAME.lower():
        return False, "Developer account cannot be disabled."

    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            "UPDATE admins SET is_active = ? WHERE username = ?",
            (1 if is_active else 0, username),
        )
        conn.commit()

    return True, "Admin status updated."


def delete_admin(username):
    if username.lower() == DEVELOPER_USERNAME.lower():
        return False, "Developer account cannot be deleted."

    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            "DELETE FROM admins WHERE username = ?",
            (username,),
        )
        conn.commit()

    return True, "Admin deleted."


def change_admin_password(username, new_password):
    password_hash = hash_password(new_password)

    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            UPDATE admins
            SET password_hash = ?
            WHERE username = ?
            """,
            (password_hash, username),
        )
        conn.commit()


init_security_db()

def get_admin_stats():
    with sqlite3.connect(ADMIN_DB) as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS total_admins,
                SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END)
                    AS active_admins
            FROM admins
            """
        ).fetchone()

        total = int(row[0] or 0)
        active = int(row[1] or 0)

        return total, active


def get_admin_table():
    with sqlite3.connect(ADMIN_DB) as conn:
        return pd.read_sql_query(
            """
            SELECT
                username AS Admin,
                created_at AS Created,
                last_login AS Last_Login,
                login_count AS Login_Count,
                CASE
                    WHEN is_active = 1 THEN 'ACTIVE'
                    ELSE 'DISABLED'
                END AS Status
            FROM admins
            ORDER BY last_login DESC
            """,
            conn,
        )


init_admin_db()

# ============================================================
# DEVELOPER ACCOUNT
# ============================================================
DEVELOPER_USERNAME = "Mayur2006"
DEVELOPER_PASSWORD = "Mayur@1234"

ROLES = {
    "Developer": "Full system control",
    "Senior Admin": "Admin operations and investigation",
    "Analyst": "Fraud analysis and investigation",
    "Viewer": "Read-only access",
}
DEVELOPER_RECOVERY_CODE = os.getenv("DEVELOPER_RECOVERY_CODE", "MAYUR-RESET-2026")


def ensure_developer_account():
    password_hash = hash_password(DEVELOPER_PASSWORD)
    recovery_hash = hash_password(DEVELOPER_RECOVERY_CODE)
    with sqlite3.connect(ADMIN_DB) as conn:
        conn.execute(
            """
            INSERT INTO admins
            (username, created_at, last_login, login_count, is_active, password_hash, recovery_hash)
            VALUES (?, ?, NULL, 0, 1, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
                password_hash = excluded.password_hash,
                recovery_hash = excluded.recovery_hash,
                is_active = 1
            """,
            (
                DEVELOPER_USERNAME,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                password_hash,
                recovery_hash,
            ),
        )
        conn.commit()


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return f"{salt}${digest}"


def verify_password(password, stored_hash):
    if not stored_hash or "$" not in stored_hash:
        return False
    salt, expected = stored_hash.split("$", 1)
    actual = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return secrets.compare_digest(actual, expected)


ensure_developer_account()


def create_admin_account(username, password):
    username = username.strip()
    if len(username) < 3:
        return False, "Username must contain at least 3 characters."
    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    password_hash = hash_password(password)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect(ADMIN_DB) as conn:
            conn.execute(
                """
                INSERT INTO admins
                (username, created_at, last_login, login_count, is_active, password_hash)
                VALUES (?, ?, NULL, 0, 1, ?)
                """,
                (username, now, password_hash),
            )
            conn.commit()
        return True, "Admin account created successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."


def authenticate_admin(username, password):
    username = username.strip()
    with sqlite3.connect(ADMIN_DB) as conn:
        row = conn.execute(
            "SELECT password_hash, is_active FROM admins WHERE username = ?",
            (username,),
        ).fetchone()

    if not row:
        return False

    password_hash, is_active = row
    return bool(is_active) and verify_password(password, password_hash)


def reset_password_with_recovery(username, recovery_code, new_password):
    username = username.strip()
    if len(username) < 3:
        return False, "Enter a valid username."
    if len(new_password) < 6:
        return False, "New password must contain at least 6 characters."

    with sqlite3.connect(ADMIN_DB) as conn:
        row = conn.execute(
            "SELECT recovery_hash, is_active FROM admins WHERE username = ?",
            (username,),
        ).fetchone()

        if not row:
            return False, "Account not found."

        recovery_hash, is_active = row
        if not is_active:
            return False, "This account is disabled."

        # The developer recovery code can recover any admin account.
        valid_recovery = verify_password(recovery_code, recovery_hash) if recovery_hash else False
        if not valid_recovery:
            valid_recovery = secrets.compare_digest(
                recovery_code.strip(),
                DEVELOPER_RECOVERY_CODE,
            )

        if not valid_recovery:
            return False, "Invalid recovery code."

        conn.execute(
            "UPDATE admins SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), username),
        )
        conn.commit()

    return True, "Password reset successfully. You can now login."


# ============================================================
# PHASE 6.7 - SECURE LOGIN
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:

    st.markdown(
        """
        <style>
        .login-wrap {
            max-width: 620px;
            margin: 5vh auto 2vh auto;
            padding: 38px;
            border-radius: 28px;
            background: linear-gradient(
                145deg,
                rgba(8,15,35,.97),
                rgba(30,27,75,.92)
            );
            border: 1px solid rgba(34,211,238,.28);
            box-shadow:
                0 0 35px rgba(34,211,238,.10),
                0 25px 70px rgba(0,0,0,.35);
        }
        .login-logo {
            text-align:center;
            font-size:62px;
            filter:drop-shadow(0 0 16px rgba(34,211,238,.65));
        }
        .login-title {
            text-align:center;
            font-size:40px;
            font-weight:950;
            background:linear-gradient(
                90deg,#22d3ee,#60a5fa,#a78bfa
            );
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        }
        .login-subtitle {
            text-align:center;
            color:#94a3b8;
            font-size:14px;
            margin-top:7px;
            margin-bottom:24px;
        }
        .developer-box {
            padding:20px;
            border-radius:20px;
            background:linear-gradient(145deg,rgba(8,15,35,.96),rgba(30,27,75,.90));
            border:1px solid rgba(34,211,238,.30);
            box-shadow:0 0 28px rgba(34,211,238,.10), inset 0 0 22px rgba(99,102,241,.06);
            margin:0 auto 22px auto;
            text-align:left;
        }
        .developer-name {
            color:#67e8f9;
            font-size:17px;
            font-weight:900;
        }
        .developer-description {
            color:#94a3b8;
            font-size:12px;
            line-height:1.75;
            margin-top:7px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.html(
        """
        <div class="login-wrap">
            <div class="login-logo">🛡️</div>
            <div class="login-title">AI-FraudGuard</div>
            <div class="login-subtitle">
                AI Financial Fraud Detection & Investigation Platform
            </div>

            <div class="developer-box">
                <div class="developer-name">
                    👨‍💻 Developed by Mayur Verma
                </div>

                <div class="developer-description">
                    AI-FraudGuard is an intelligent financial fraud
                    detection and investigation platform that combines
                    Machine Learning, AI-assisted investigation,
                    behavioral risk analysis, transaction analytics
                    and bulk fraud screening to identify suspicious
                    financial activity.
                </div>

                <div class="developer-description">
                    <b>Core Technologies:</b><br>
                    Python • Streamlit • Random Forest • XGBoost •
                    LightGBM • SMOTE • Risk Engine • Groq AI
                </div>
            </div>
        </div>
        """
    )

    st.markdown("### 🔐 AI-FraudGuard Access")

    login_tab, signup_tab, forgot_tab = st.tabs([
        "🔐 Login",
        "📝 Sign Up",
        "🔑 Forgot Password",
    ])

    with login_tab:
        with st.form("ai_fraudguard_login"):
            username = st.text_input(
                "Username",
                placeholder="Enter username",
                key="login_username",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_password",
            )

            submitted = st.form_submit_button(
                "🚀 LOGIN TO AI-FRAUDGUARD",
                use_container_width=True,
            )

            if submitted:
                if (
                    username.strip() == DEVELOPER_USERNAME
                    and password == DEVELOPER_PASSWORD
                ):
                    register_admin(DEVELOPER_USERNAME)
                    record_admin_login(DEVELOPER_USERNAME)
                    st.session_state["authenticated"] = True
                    st.session_state["logged_in_admin"] = DEVELOPER_USERNAME
                    st.session_state["is_developer"] = True
                    log_audit(
                        DEVELOPER_USERNAME,
                        "LOGIN",
                        "SUCCESS",
                        "Developer login",
                    )
                    st.rerun()

                elif authenticate_admin(username, password):
                    record_admin_login(username.strip())
                    st.session_state["authenticated"] = True
                    st.session_state["logged_in_admin"] = username.strip()
                    st.session_state["is_developer"] = (
                        username.strip().lower() == DEVELOPER_USERNAME.lower()
                    )
                    log_audit(
                        username.strip(),
                        "LOGIN",
                        "SUCCESS",
                        "Admin login",
                    )
                    st.rerun()
                else:
                    log_audit(
                        username.strip() or "UNKNOWN",
                        "LOGIN",
                        "FAILED",
                        "Invalid username/password",
                    )
                    log_security_event(
                        username.strip() or "UNKNOWN",
                        "FAILED_LOGIN",
                        "Invalid credentials",
                    )
                    st.error("❌ Invalid username or password.")

        st.caption("Developer access is restricted to the configured developer account.")

    with signup_tab:
        st.markdown(
            "**Create a new Admin account**  \n            \n            Your account will be added to the Admin Registry."
        )

        with st.form("ai_fraudguard_signup"):
            new_username = st.text_input(
                "New Username",
                placeholder="e.g. analyst01",
                key="signup_username",
            )
            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="signup_password",
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter password",
                key="signup_confirm",
            )

            signup_submitted = st.form_submit_button(
                "✨ CREATE ADMIN ACCOUNT",
                use_container_width=True,
            )

            if signup_submitted:
                if new_password != confirm_password:
                    st.error("❌ Passwords do not match.")
                else:
                    ok, message = create_admin_account(
                        new_username,
                        new_password,
                    )
                    if ok:
                        st.success("✅ " + message)
                        st.info("You can now use the Login tab.")
                    else:
                        st.error("❌ " + message)

    with forgot_tab:
        st.markdown("### 🔑 Account Recovery")
        st.caption(
            "Use the recovery code to reset an admin password. "
            "This local recovery system does not send email."
        )

        with st.form("ai_fraudguard_forgot_password"):
            recovery_username = st.text_input(
                "Username",
                placeholder="Enter your admin username",
                key="recovery_username",
            )
            recovery_code = st.text_input(
                "Recovery Code",
                type="password",
                placeholder="Enter recovery code",
                key="recovery_code",
            )
            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="recovery_new_password",
            )
            confirm_new_password = st.text_input(
                "Confirm New Password",
                type="password",
                placeholder="Re-enter new password",
                key="recovery_confirm_password",
            )

            reset_submitted = st.form_submit_button(
                "🔐 RESET PASSWORD",
                use_container_width=True,
            )

            if reset_submitted:
                if new_password != confirm_new_password:
                    st.error("❌ Passwords do not match.")
                else:
                    ok, message = reset_password_with_recovery(
                        recovery_username,
                        recovery_code,
                        new_password,
                    )
                    if ok:
                        st.success("✅ " + message)
                    else:
                        st.error("❌ " + message)

        st.caption("For security, the recovery code is not displayed here.")

    st.stop()


# ============================================================
# DATASET FINDER
# ============================================================

def find_dataset():
    possible_paths = [
        os.path.join(BASE_DIR, "dataset", "creditcard.csv"),
        os.path.join(BASE_DIR, "dataset", "raw", "creditcard.csv"),
        os.path.join(BASE_DIR, "dataset", "raw", "fraud_dataset.csv"),
        os.path.join(BASE_DIR, "dataset", "fraud_dataset.csv"),
        os.path.join(BASE_DIR, "dataset", "raw_data.csv"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


DATASET_PATH = find_dataset()

if DATASET_PATH is None:
    st.error(
        "❌ Dataset CSV नहीं मिला। dataset folder में अपनी CSV check करो."
    )
    st.stop()

try:
    df = pd.read_csv(DATASET_PATH)
except Exception as e:
    st.error(f"Dataset loading failed: {e}")
    st.stop()


# ============================================================
# LOAD ML PREDICTOR
# ============================================================

if FraudPredictor is None:
    st.error("FraudPredictor import नहीं हो पाया.")
    st.code(PREDICTOR_IMPORT_ERROR)
    st.stop()

try:
    predictor = FraudPredictor()
except Exception as e:
    st.error(f"ML model loading failed: {e}")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🛡️</div>
            <div class="sidebar-title">AI-FraudGuard</div>
            <div class="sidebar-subtitle">
                INTELLIGENT FRAUD DEFENSE
            </div>
        </div>
        """
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "🔍 Transaction Analyzer",
            "📦 Bulk Fraud Scanner",
            "🚨 Fraud Alert Center",
            "🗂️ Investigation Cases",
            "🧠 Fraud Intelligence",
            "👤 Customer & Device Intelligence",
            "📑 Reports",
            "📈 Fraud Analytics",
            "📊 Model Performance",
            "📋 Transaction Data",
        ],
    )

    st.markdown("---")

    st.html(
        """
        <div class="sidebar-engine">
            <div class="engine-title">⚡ SECURITY ENGINE</div>
            <div class="engine-item">🤖 ML + SMOTE</div>
            <div class="engine-item">🧠 Groq AI</div>
            <div class="engine-item">🛡️ Risk Engine</div>
            <div class="engine-item">📊 Real-Time Detection</div>
            <div class="engine-item">🔎 AI Investigation</div>
        </div>
        """
    )



    st.markdown("---")

    if st.session_state.get("is_developer", False):

        total_admins, active_admins = get_admin_stats()

        st.html(
            f"""
            <div style="
                padding:16px;
                border-radius:17px;
                background:linear-gradient(
                    145deg,
                    rgba(8,15,35,.94),
                    rgba(30,27,75,.76)
                );
                border:1px solid rgba(139,92,246,.20);
                margin-bottom:12px;
            ">
                <div style="
                    color:#67e8f9;
                    font-size:11px;
                    letter-spacing:1px;
                    font-weight:900;
                ">
                    👥 ADMIN CONTROL
                </div>

                <div style="
                    display:flex;
                    justify-content:space-between;
                    margin-top:10px;
                ">
                    <div>
                        <div style="
                            color:#64748b;
                            font-size:10px;
                        ">
                            TOTAL ADMINS
                        </div>
                        <div style="
                            color:#22d3ee;
                            font-size:25px;
                            font-weight:950;
                        ">
                            {total_admins}
                        </div>
                    </div>

                    <div>
                        <div style="
                            color:#64748b;
                            font-size:10px;
                        ">
                            ACTIVE
                        </div>
                        <div style="
                            color:#4ade80;
                            font-size:25px;
                            font-weight:950;
                        ">
                            {active_admins}
                        </div>
                    </div>
                </div>
            </div>
            """
        )

        if st.button(
            "👥 View Admin Registry",
            use_container_width=True,
        ):
            st.session_state["show_admin_registry"] = True



    st.html(
        """
        <div style="
            padding:16px;
            border-radius:17px;
            background:rgba(15,23,42,.78);
            border:1px solid rgba(34,211,238,.16);
        ">
            <div style="
                color:#67e8f9;
                font-size:11px;
                letter-spacing:1px;
                font-weight:900;
            ">
                👨‍💻 DEVELOPED BY
            </div>

            <div style="
                color:#f8fafc;
                font-size:17px;
                font-weight:950;
                margin-top:6px;
            ">
                Mayur Verma
            </div>

            <div style="
                color:#64748b;
                font-size:11px;
                line-height:1.6;
                margin-top:5px;
            ">
                AI + ML Financial Fraud Detection &
                Investigation Platform
            </div>
        </div>
        """
    )

    if st.button(
        "ℹ️ About AI-FraudGuard",
        use_container_width=True,
    ):
        st.session_state["show_about"] = True

    if st.button(
        "🚪 Logout",
        use_container_width=True,
    ):
        current_user = st.session_state.get(
            "logged_in_admin",
            "UNKNOWN",
        )

        log_audit(
            current_user,
            "LOGOUT",
            "SUCCESS",
            "User logout",
        )

        st.session_state["authenticated"] = False
        st.session_state["is_developer"] = False
        st.session_state["show_admin_registry"] = False
        st.session_state["show_security_center"] = False
        st.rerun()



# ============================================================
# PHASE 7 - SECURITY CONTROL CENTER
# ============================================================

if (
    st.session_state.get("is_developer", False)
    and st.session_state.get("show_security_center", False)
):

    total_admins, active_admins = get_admin_stats()
    total_logins, failed_logins, suspicious_events = get_security_counts()

    st.html(
        f"""
        <div class="hero">
            <div class="hero-title">
                🛡️ Security Control Center
            </div>
            <div class="hero-subtitle">
                Developer-only Advanced Security & Admin Control
            </div>
        </div>
        """
    )

    cols = st.columns(5)
    cards = [
        ("👥", "TOTAL ADMINS", total_admins),
        ("🟢", "ACTIVE", active_admins),
        ("🔐", "SUCCESS LOGINS", total_logins),
        ("🚨", "FAILED LOGINS", failed_logins),
        ("⚠️", "SECURITY EVENTS", suspicious_events),
    ]

    for col, (icon, label, value) in zip(cols, cards):
        with col:
            st.metric(f"{icon} {label}", value)

    st.markdown("### 👥 Admin Management")

    admin_df = get_admin_registry()

    if not admin_df.empty:
        st.dataframe(
            admin_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### ⚙️ Manage Admin")

        selectable = [
            x for x in admin_df["Admin"].tolist()
            if x != DEVELOPER_USERNAME
        ]

        if selectable:
            selected_admin = st.selectbox(
                "Select Admin",
                selectable,
            )

            current_role = get_admin_role(selected_admin)

            manage_col1, manage_col2 = st.columns(2)

            with manage_col1:
                new_role = st.selectbox(
                    "Role",
                    list(ROLES.keys()),
                    index=(
                        list(ROLES.keys()).index(current_role)
                        if current_role in ROLES
                        else 2
                    ),
                )

                if st.button(
                    "💾 UPDATE ROLE",
                    use_container_width=True,
                ):
                    set_admin_role(selected_admin, new_role)
                    log_audit(
                        DEVELOPER_USERNAME,
                        "ROLE_UPDATE",
                        "SUCCESS",
                        f"{selected_admin} -> {new_role}",
                    )
                    st.success("✅ Role updated.")
                    st.rerun()

            with manage_col2:
                if st.button(
                    "🔴 DISABLE ADMIN",
                    use_container_width=True,
                ):
                    ok, msg = set_admin_status(
                        selected_admin,
                        False,
                    )
                    if ok:
                        log_audit(
                            DEVELOPER_USERNAME,
                            "ADMIN_DISABLE",
                            "SUCCESS",
                            selected_admin,
                        )
                        st.success("✅ Admin disabled.")
                        st.rerun()
                    else:
                        st.error(msg)

                if st.button(
                    "🟢 ENABLE ADMIN",
                    use_container_width=True,
                ):
                    ok, msg = set_admin_status(
                        selected_admin,
                        True,
                    )
                    if ok:
                        log_audit(
                            DEVELOPER_USERNAME,
                            "ADMIN_ENABLE",
                            "SUCCESS",
                            selected_admin,
                        )
                        st.success("✅ Admin enabled.")
                        st.rerun()

                if st.button(
                    "🗑️ DELETE ADMIN",
                    use_container_width=True,
                ):
                    ok, msg = delete_admin(selected_admin)
                    if ok:
                        log_audit(
                            DEVELOPER_USERNAME,
                            "ADMIN_DELETE",
                            "SUCCESS",
                            selected_admin,
                        )
                        st.success("✅ Admin deleted.")
                        st.rerun()
                    else:
                        st.error(msg)

    st.markdown("### 📝 Security Audit Log")

    audit_df = get_audit_logs()

    if audit_df.empty:
        st.info("No audit events yet.")
    else:
        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### 🚨 Security Events")

    events_df = get_security_events()

    if events_df.empty:
        st.success("No security events detected.")
    else:
        st.dataframe(
            events_df,
            use_container_width=True,
            hide_index=True,
        )

    if st.button(
        "✕ Close Security Control Center",
        use_container_width=False,
    ):
        st.session_state["show_security_center"] = False
        st.rerun()


# ============================================================
# ABOUT AI-FRAUDGUARD
# ============================================================

if st.session_state.get("show_about", False):

    st.html(
        """
        <div class="hero">

            <div class="hero-title">
                🛡️ About AI-FraudGuard
            </div>

            <div class="hero-subtitle">
                Developed by Mayur Verma
            </div>

            <div style="
                color:#cbd5e1;
                line-height:1.8;
                margin-top:18px;
                max-width:1050px;
            ">
                AI-FraudGuard is a final-year AI/ML project for
                intelligent financial fraud detection and
                investigation. The platform combines machine
                learning models, a rule-based risk engine,
                transaction analytics, bulk screening and
                AI-assisted investigation into a single
                security dashboard.
            </div>

            <div style="
                color:#67e8f9;
                font-size:12px;
                margin-top:17px;
                letter-spacing:.5px;
            ">
                Python • Streamlit • Random Forest • XGBoost •
                LightGBM • SMOTE • Risk Engine • Groq AI
            </div>

        </div>
        """
    )

    if st.button(
        "✕ Close About",
        use_container_width=False,
    ):
        st.session_state["show_about"] = False
        st.rerun()



# ============================================================
# ADMIN REGISTRY
# ============================================================

if (
    st.session_state.get("is_developer", False)
    and st.session_state.get("show_admin_registry", False)
):

    total_admins, active_admins = get_admin_stats()

    st.html(
        f"""
        <div class="hero">

            <div class="hero-title">
                👥 Admin Registry
            </div>

            <div class="hero-subtitle">
                Developer-only monitoring panel
            </div>

            <div style="
                color:#94a3b8;
                line-height:1.7;
                margin-top:12px;
            ">
                Total registered admins:
                <b style="color:#22d3ee;">
                    {total_admins}
                </b>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Active admins:
                <b style="color:#4ade80;">
                    {active_admins}
                </b>
            </div>

        </div>
        """
    )

    admin_df = get_admin_table()

    if admin_df.empty:
        st.info("No admin accounts registered yet.")
    else:
        st.dataframe(
            admin_df,
            use_container_width=True,
            hide_index=True,
        )

    # Developer-only admin deletion controls
    if st.session_state.get("is_developer", False):
        
        st.markdown("### 🔒 Security Hardening")
        hard_cols = st.columns(3)
        hard_cols[0].metric("Failed Login Events", security_event_count(event_type="LOGIN_FAILED"))
        hard_cols[1].metric("Successful Logins", security_event_count(event_type="LOGIN_SUCCESS"))
        hard_cols[2].metric("Audit Events", security_event_count())

        st.markdown("### 🛡️ Developer Admin Controls")

        registry_df = get_admin_registry()

        removable = [
            u for u in registry_df["Admin"].tolist()
            if u.lower() != DEVELOPER_USERNAME.lower()
        ]

        if removable:
            selected_delete_admin = st.selectbox(
                "Select admin to delete",
                removable,
                key="delete_admin_select",
            )

            if st.button(
                "🗑️ DELETE SELECTED ADMIN",
                use_container_width=True,
                key="delete_selected_admin_btn",
            ):
                ok, msg = delete_admin(selected_delete_admin)

                if ok:
                    log_audit(
                        DEVELOPER_USERNAME,
                        "ADMIN_DELETE",
                        "SUCCESS",
                        selected_delete_admin,
                    )
                    st.success(
                        f"✅ Admin '{selected_delete_admin}' deleted successfully."
                    )
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.info("No removable admin accounts found.")

    if st.button(
        "✕ Close Admin Registry",
        use_container_width=False,
    ):
        st.session_state["show_admin_registry"] = False
        st.rerun()



# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">
        <div class="hero-title">🛡️ AI-FraudGuard</div>
        <div class="hero-subtitle">
            AI Financial Fraud Detection & Investigation Platform
        </div>
        <div class="system-status">
            ● SYSTEM ONLINE
            &nbsp;&nbsp; • &nbsp;&nbsp;
            ● ML ENGINE ACTIVE
            &nbsp;&nbsp; • &nbsp;&nbsp;
            ● AI INVESTIGATION READY
        </div>
    </div>
    """
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    total = len(df)
    fraud = int((df["Class"] == 1).sum())
    normal = int((df["Class"] == 0).sum())

    fraud_rate = (
        fraud / total * 100
        if total > 0
        else 0
    )

    st.html(
        """
        <div class="section-title">
            <span style="color:#22d3ee;">◆</span>
            Security Overview
        </div>
        """
    )

    metric_cols = st.columns(4)

    metric_data = [
        ("💳", "TOTAL TRANSACTIONS", f"{total:,}", "#22d3ee"),
        ("🟢", "NORMAL", f"{normal:,}", "#22c55e"),
        ("🚨", "FRAUD", f"{fraud:,}", "#fb7185"),
        ("⚡", "FRAUD RATE", f"{fraud_rate:.2f}%", "#a78bfa"),
    ]

    for col, item in zip(metric_cols, metric_data):
        icon, label, value, color = item

        with col:
            st.html(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="color:{color};">
                        {value}
                    </div>
                </div>
                """
            )

    st.html(
        """
        <div class="section-title">
            <span style="color:#8b5cf6;">◆</span>
            Fraud Intelligence
        </div>
        """
    )

    left, right = st.columns(2)

    with left:

        st.html(
            """
            <div class="glass-card">
                <h3>🚨 Transaction Distribution</h3>
                <p style="color:#64748b;">
                    Normal vs suspicious transaction overview
                </p>
            </div>
            """
        )

        distribution = pd.DataFrame(
            {"Transactions": [normal, fraud]},
            index=["Normal", "Fraud"],
        )

        st.bar_chart(distribution)

    with right:

        st.html(
            """
            <div class="glass-card">
                <h3>💰 Transaction Amount Trend</h3>
                <p style="color:#64748b;">
                    Recent transaction amount analysis
                </p>
            </div>
            """
        )

        if "Amount" in df.columns:
            st.line_chart(df["Amount"].head(100))

    st.html(
        """
        <div class="section-title">
            <span style="color:#22d3ee;">◆</span>
            Recent Transactions
        </div>
        """
    )

    st.dataframe(
        df.head(15),
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# TRANSACTION ANALYZER
# ============================================================

elif page == "🔍 Transaction Analyzer":

    st.html(
        """
        <div class="section-title">
            <span style="color:#22d3ee;">◆</span>
            Real-Time Transaction Analyzer
        </div>

        <p style="color:#64748b;margin-top:-8px;">
            ML + Risk Engine + AI Investigation
        </p>
        """
    )

    left, right = st.columns(2)

    with left:

        st.html(
            """
            <div class="input-card">
                <h3>💳 Transaction Details</h3>
            </div>
            """
        )

        amount = st.number_input(
            "💰 Transaction Amount (₹)",
            min_value=1.0,
            value=5000.0,
            step=500.0,
        )

        location = st.selectbox(
            "📍 Location",
            [
                "Delhi",
                "Mumbai",
                "Lucknow",
                "Kanpur",
                "Jhansi",
                "Noida",
                "Pune",
                "Jaipur",
            ],
        )

        device = st.selectbox(
            "📱 Device",
            ["Known", "New"],
        )

        transaction_count = st.number_input(
            "🔄 Transaction Count",
            min_value=1,
            max_value=100,
            value=3,
        )

    with right:

        st.html(
            """
            <div class="input-card">
                <h3>🏪 Account & Merchant</h3>
            </div>
            """
        )

        merchant = st.selectbox(
            "🏪 Merchant Category",
            [
                "Food",
                "Shopping",
                "Electronics",
                "Travel",
                "Fuel",
                "Bills",
                "Entertainment",
            ],
        )

        account_age = st.number_input(
            "📅 Account Age (Days)",
            min_value=1,
            max_value=5000,
            value=365,
        )

        hour = st.slider(
            "🕐 Transaction Hour",
            0,
            23,
            14,
        )

        minute = st.slider(
            "⏱️ Transaction Minute",
            0,
            59,
            30,
        )

    st.write("")

    analyze = st.button(
        "⚡ ANALYZE TRANSACTION",
        type="primary",
        use_container_width=True,
    )

    if analyze:

        transaction = {
            "Amount": amount,
            "Location": location,
            "Device": device,
            "Transaction_Count": transaction_count,
            "Merchant_Category": merchant,
            "Account_Age_Days": account_age,
            "Hour": hour,
            "Minute": minute,
        }

        try:
            with st.spinner("🤖 ML engine analyzing..."):
                ml_result = predictor.predict(transaction)
        except Exception as e:
            st.error(f"ML prediction failed: {e}")
            st.stop()

        if calculate_risk is None:
            st.error("Risk Engine import नहीं हो पाया.")
            st.code(RISK_IMPORT_ERROR)
            st.stop()

        try:
            risk_result = calculate_risk(
                transaction,
                ml_result,
            )
        except Exception as e:
            st.error(f"Risk engine failed: {e}")
            st.stop()

        st.session_state["transaction"] = transaction
        st.session_state["ml_result"] = ml_result
        st.session_state["risk_result"] = risk_result

        st.session_state.pop(
            "investigation_report",
            None,
        )


    # ========================================================
    # RESULTS
    # ========================================================

    if "risk_result" in st.session_state:

        transaction = st.session_state["transaction"]
        ml_result = st.session_state["ml_result"]
        risk_result = st.session_state["risk_result"]


        # ====================================================
        # SECURITY ANALYSIS
        # ====================================================

        st.html(
            """
            <div class="section-title">
                <span style="color:#22d3ee;">◆</span>
                Security Analysis
            </div>
            """
        )


        # ====================================================
        # PREMIUM SECURITY METRICS
        # ====================================================

        ml_probability = float(
            ml_result["fraud_probability"]
        )

        risk_score = float(
            risk_result["risk_score"]
        )

        risk_level = str(
            risk_result["risk_level"]
        )

        status = str(
            risk_result["status"]
        )

        metric_cols = st.columns(4)


        # ----------------------------------------------------
        # ML PROBABILITY
        # ----------------------------------------------------

        with metric_cols[0]:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">🤖</div>

                    <div class="metric-label">
                        ML FRAUD PROBABILITY
                    </div>

                    <div
                        class="metric-value"
                        style="color:#22d3ee;"
                    >
                        {ml_probability:.1f}%
                    </div>

                    <div style="
                        margin-top:10px;
                        height:6px;
                        background:#111827;
                        border-radius:10px;
                        overflow:hidden;
                    ">

                        <div style="
                            width:{min(ml_probability,100)}%;
                            height:100%;
                            background:
                            linear-gradient(
                                90deg,
                                #06b6d4,
                                #8b5cf6
                            );
                            border-radius:10px;
                            box-shadow:
                            0 0 12px
                            rgba(34,211,238,.7);
                        ">
                        </div>

                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # RISK SCORE
        # ----------------------------------------------------

        with metric_cols[1]:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">🛡️</div>

                    <div class="metric-label">
                        RISK SCORE
                    </div>

                    <div
                        class="metric-value"
                        style="color:#a78bfa;"
                    >
                        {risk_score:.0f}
                        <span style="
                            font-size:14px;
                            color:#64748b;
                        ">
                            /100
                        </span>
                    </div>

                    <div style="
                        margin-top:10px;
                        height:6px;
                        background:#111827;
                        border-radius:10px;
                        overflow:hidden;
                    ">

                        <div style="
                            width:{min(risk_score,100)}%;
                            height:100%;
                            background:
                            linear-gradient(
                                90deg,
                                #8b5cf6,
                                #ec4899
                            );
                            border-radius:10px;
                            box-shadow:
                            0 0 12px
                            rgba(139,92,246,.7);
                        ">
                        </div>

                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # RISK LEVEL
        # ----------------------------------------------------

        with metric_cols[2]:

            if risk_level.lower() == "critical":
                level_color = "#fb7185"
                level_icon = "🚨"
            elif risk_level.lower() == "high":
                level_color = "#fb923c"
                level_icon = "🔴"
            elif risk_level.lower() == "medium":
                level_color = "#facc15"
                level_icon = "🟡"
            else:
                level_color = "#22d3ee"
                level_icon = "🟢"

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        {level_icon}
                    </div>

                    <div class="metric-label">
                        RISK LEVEL
                    </div>

                    <div
                        class="metric-value"
                        style="
                            color:{level_color};
                            font-size:24px;
                        "
                    >
                        {html.escape(risk_level)}
                    </div>

                    <div style="
                        margin-top:12px;
                        color:{level_color};
                        font-size:12px;
                        font-weight:800;
                    ">
                        ● THREAT STATUS
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # SECURITY ACTION
        # ----------------------------------------------------

        with metric_cols[3]:

            if "BLOCK" in status.upper():
                status_color = "#fb7185"
                status_icon = "⛔"
            elif "REVIEW" in status.upper():
                status_color = "#facc15"
                status_icon = "⚠️"
            else:
                status_color = "#22d3ee"
                status_icon = "✓"

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        {status_icon}
                    </div>

                    <div class="metric-label">
                        SECURITY ACTION
                    </div>

                    <div
                        class="metric-value"
                        style="
                            color:{status_color};
                            font-size:17px;
                        "
                    >
                        {html.escape(status)}
                    </div>

                    <div style="
                        margin-top:12px;
                        color:#64748b;
                        font-size:11px;
                    ">
                        AI-RISK DECISION
                    </div>

                </div>
                """
            )


        # ====================================================
        # PHASE 6.2 - THREAT INTELLIGENCE
        # ====================================================

        st.html(
            """
            <div class="section-title">
                <span style="color:#a78bfa;">◆</span>
                Threat Intelligence
            </div>
            """
        )


        # ====================================================
        # GAUGE COLORS
        # ====================================================

        if ml_probability >= 70:
            gauge_color = "#fb7185"
        elif ml_probability >= 40:
            gauge_color = "#facc15"
        else:
            gauge_color = "#22d3ee"

        if risk_score >= 80:
            risk_gauge_color = "#fb7185"
        elif risk_score >= 50:
            risk_gauge_color = "#facc15"
        else:
            risk_gauge_color = "#22d3ee"


        # ====================================================
        # GAUGES
        # ====================================================

        gauge_col1, gauge_col2 = st.columns(2)


        # ----------------------------------------------------
        # ML GAUGE
        # ----------------------------------------------------

        with gauge_col1:

            ml_angle = (
                ml_probability / 100
            ) * 360

            st.html(
                f"""
                <div class="glass-card">

                    <div style="
                        text-align:center;
                        color:#67e8f9;
                        font-size:15px;
                        font-weight:900;
                        margin-bottom:5px;
                    ">
                        🤖 ML FRAUD PROBABILITY
                    </div>

                    <div class="gauge-container">

                        <div
                            class="gauge"
                            style="
                                background:
                                conic-gradient(
                                    {gauge_color}
                                    {ml_angle}deg,
                                    #172033
                                    {ml_angle}deg
                                );

                                box-shadow:
                                0 0 30px
                                {gauge_color}55;
                            "
                        >

                            <div class="gauge-inner">

                                <div
                                    class="gauge-value"
                                    style="
                                        color:{gauge_color};
                                    "
                                >
                                    {ml_probability:.1f}%
                                </div>

                                <div class="gauge-label">
                                    FRAUD PROBABILITY
                                </div>

                            </div>

                        </div>

                    </div>

                    <div style="
                        text-align:center;
                        color:#64748b;
                        font-size:12px;
                    ">
                        Machine Learning Prediction
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # RISK GAUGE
        # ----------------------------------------------------

        with gauge_col2:

            risk_angle = (
                risk_score / 100
            ) * 360

            st.html(
                f"""
                <div class="glass-card">

                    <div style="
                        text-align:center;
                        color:#a78bfa;
                        font-size:15px;
                        font-weight:900;
                        margin-bottom:5px;
                    ">
                        🛡️ SECURITY RISK SCORE
                    </div>

                    <div class="gauge-container">

                        <div
                            class="gauge"
                            style="
                                background:
                                conic-gradient(
                                    {risk_gauge_color}
                                    {risk_angle}deg,
                                    #172033
                                    {risk_angle}deg
                                );

                                box-shadow:
                                0 0 30px
                                {risk_gauge_color}55;
                            "
                        >

                            <div class="gauge-inner">

                                <div
                                    class="gauge-value"
                                    style="
                                        color:{risk_gauge_color};
                                    "
                                >
                                    {risk_score:.0f}
                                </div>

                                <div class="gauge-label">
                                    RISK / 100
                                </div>

                            </div>

                        </div>

                    </div>

                    <div style="
                        text-align:center;
                        color:#64748b;
                        font-size:12px;
                    ">
                        Rule-Based Risk Engine
                    </div>

                </div>
                """
            )


        # ====================================================
        # RISK BREAKDOWN
        # ====================================================

        st.html(
            """
            <div class="section-title">
                <span style="color:#22d3ee;">◆</span>
                Risk Breakdown
            </div>
            """
        )

        breakdown_col1, breakdown_col2 = st.columns(2)


        with breakdown_col1:

            st.html(
                f"""
                <div class="analysis-item">

                    <div class="analysis-item-title">
                        ML ENGINE
                    </div>

                    <div
                        class="analysis-item-value"
                        style="color:#22d3ee;"
                    >
                        {ml_probability:.1f}%
                    </div>

                    <div style="
                        color:#64748b;
                        font-size:11px;
                        margin-top:5px;
                    ">
                        Fraud probability generated
                        by trained ML model.
                    </div>

                </div>
                """
            )


        with breakdown_col2:

            st.html(
                f"""
                <div class="analysis-item">

                    <div class="analysis-item-title">
                        RISK ENGINE
                    </div>

                    <div
                        class="analysis-item-value"
                        style="color:#a78bfa;"
                    >
                        {risk_score:.0f}/100
                    </div>

                    <div style="
                        color:#64748b;
                        font-size:11px;
                        margin-top:5px;
                    ">
                        Combined rule-based
                        transaction risk.
                    </div>

                </div>
                """
            )


        # ====================================================
        # RISK CARD
        # ====================================================

        risk_class = risk_level.lower()

        if risk_class == "critical":
            risk_icon = "🚨"
        elif risk_class == "high":
            risk_icon = "🔴"
        elif risk_class == "medium":
            risk_icon = "🟡"
        else:
            risk_class = "low"
            risk_icon = "🟢"

        st.html(
            f"""
            <div class="risk-card risk-{risk_class}">

                <div class="risk-icon">
                    {risk_icon}
                </div>

                <div class="risk-title">
                    {html.escape(risk_level)}
                </div>

                <div class="risk-score">
                    Risk Score:
                    <b>{risk_score:.0f}/100</b>
                </div>

                <div class="risk-status">
                    {html.escape(status)}
                </div>

            </div>
            """
        )


        # ====================================================
        # SUSPICIOUS INDICATORS
        # ====================================================

        st.html(
            """
            <div class="section-title">
                <span style="color:#fb7185;">◆</span>
                Suspicious Indicators
            </div>
            """
        )

        reasons = risk_result.get(
            "reasons",
            []
        )

        if reasons:

            reason_cols = st.columns(2)

            for i, reason in enumerate(reasons):

                safe_reason = html.escape(
                    str(reason)
                )

                with reason_cols[i % 2]:

                    st.html(
                        f"""
                        <div class="reason-card">
                            ⚠️ {safe_reason}
                        </div>
                        """
                    )

        else:

            st.info(
                "No specific rule-based indicators returned."
            )


        # ====================================================
        # PHASE 6.3 - FORENSIC INVESTIGATION CENTER
        # ====================================================

        st.html(
            """
            <div class="section-title">
                <span style="color:#fb7185;">◆</span>
                Forensic Investigation Center
            </div>
            """
        )

        # Evidence severity
        if risk_score >= 80 or ml_probability >= 70:
            evidence_color = "#fb7185"
            evidence_level = "CRITICAL EVIDENCE"
        elif risk_score >= 50 or ml_probability >= 40:
            evidence_color = "#facc15"
            evidence_level = "HIGH PRIORITY EVIDENCE"
        else:
            evidence_color = "#22d3ee"
            evidence_level = "STANDARD REVIEW"

        # Recommended action
        if "BLOCK" in status.upper() or risk_score >= 80:
            recommended_action = "BLOCK & INVESTIGATE"
            action_color = "#fb7185"
            action_icon = "⛔"
        elif risk_score >= 50 or ml_probability >= 40:
            recommended_action = "HOLD & REVIEW"
            action_color = "#facc15"
            action_icon = "⚠️"
        else:
            recommended_action = "ALLOW & MONITOR"
            action_color = "#22d3ee"
            action_icon = "✓"

        forensic_top = st.columns(3)

        with forensic_top[0]:
            st.html(
                f"""
                <div class="glass-card">
                    <div style="color:#64748b;font-size:11px;
                                letter-spacing:1px;font-weight:800;">
                        EVIDENCE STATUS
                    </div>
                    <div style="color:{evidence_color};
                                font-size:22px;font-weight:900;
                                margin-top:8px;">
                        {evidence_level}
                    </div>
                    <div style="color:#64748b;font-size:11px;margin-top:7px;">
                        Combined ML and rule-engine evidence
                    </div>
                </div>
                """
            )

        with forensic_top[1]:
            st.html(
                f"""
                <div class="glass-card">
                    <div style="color:#64748b;font-size:11px;
                                letter-spacing:1px;font-weight:800;">
                        INVESTIGATION PRIORITY
                    </div>
                    <div style="color:{action_color};
                                font-size:22px;font-weight:900;
                                margin-top:8px;">
                        {action_icon} {recommended_action}
                    </div>
                    <div style="color:#64748b;font-size:11px;margin-top:7px;">
                        Operational recommendation
                    </div>
                </div>
                """
            )

        with forensic_top[2]:
            st.html(
                f"""
                <div class="glass-card">
                    <div style="color:#64748b;font-size:11px;
                                letter-spacing:1px;font-weight:800;">
                        TRANSACTION ID
                    </div>
                    <div style="color:#67e8f9;
                                font-size:22px;font-weight:900;
                                margin-top:8px;">
                        {html.escape(str(
                            transaction.get("Transaction_ID", "LIVE-ANALYSIS")
                        ))}
                    </div>
                    <div style="color:#64748b;font-size:11px;margin-top:7px;">
                        Current investigation case
                    </div>
                </div>
                """
            )

        # ----------------------------------------------------
        # INVESTIGATION TIMELINE
        # ----------------------------------------------------

        st.html(
            """
            <div style="
                margin-top:20px;
                padding:22px;
                border-radius:20px;
                background:linear-gradient(
                    145deg,
                    rgba(8,15,35,.94),
                    rgba(20,25,55,.76)
                );
                border:1px solid rgba(139,92,246,.20);
            ">

                <div style="
                    color:#a78bfa;
                    font-size:16px;
                    font-weight:900;
                    margin-bottom:18px;
                ">
                    🕵️ Investigation Timeline
                </div>

                <div style="
                    display:grid;
                    grid-template-columns:
                    repeat(4,1fr);
                    gap:12px;
                ">

                    <div style="
                        padding:15px;
                        border-left:3px solid #22d3ee;
                        background:rgba(15,23,42,.70);
                        border-radius:10px;
                    ">
                        <b style="color:#67e8f9;">01</b>
                        <div style="color:#f8fafc;margin-top:5px;">
                            Transaction Captured
                        </div>
                        <small style="color:#64748b;">
                            Input received
                        </small>
                    </div>

                    <div style="
                        padding:15px;
                        border-left:3px solid #8b5cf6;
                        background:rgba(15,23,42,.70);
                        border-radius:10px;
                    ">
                        <b style="color:#a78bfa;">02</b>
                        <div style="color:#f8fafc;margin-top:5px;">
                            ML Analysis
                        </div>
                        <small style="color:#64748b;">
                            Probability evaluated
                        </small>
                    </div>

                    <div style="
                        padding:15px;
                        border-left:3px solid #fb7185;
                        background:rgba(15,23,42,.70);
                        border-radius:10px;
                    ">
                        <b style="color:#fb7185;">03</b>
                        <div style="color:#f8fafc;margin-top:5px;">
                            Risk Evaluation
                        </div>
                        <small style="color:#64748b;">
                            Rules and signals combined
                        </small>
                    </div>

                    <div style="
                        padding:15px;
                        border-left:3px solid #facc15;
                        background:rgba(15,23,42,.70);
                        border-radius:10px;
                    ">
                        <b style="color:#facc15;">04</b>
                        <div style="color:#f8fafc;margin-top:5px;">
                            Analyst Decision
                        </div>
                        <small style="color:#64748b;">
                            Review recommended
                        </small>
                    </div>

                </div>
            </div>
            """
        )

        # ----------------------------------------------------
        # EVIDENCE MATRIX
        # ----------------------------------------------------

        st.html(
            """
            <div class="section-title">
                <span style="color:#22d3ee;">◆</span>
                Evidence Matrix
            </div>
            """
        )

        evidence_rows = [
            (
                "🤖 ML Engine",
                f"{ml_probability:.1f}%",
                "Fraud Probability",
                "#22d3ee",
            ),
            (
                "🛡️ Risk Engine",
                f"{risk_score:.0f}/100",
                "Risk Score",
                "#a78bfa",
            ),
            (
                "💰 Amount",
                f"₹{float(transaction.get('Amount', 0)):,.2f}",
                "Transaction Value",
                "#38bdf8",
            ),
            (
                "📱 Device",
                str(transaction.get("Device", "Unknown")),
                "Device Status",
                "#fb7185"
                if str(transaction.get("Device", "")).lower() == "new"
                else "#22d3ee",
            ),
            (
                "🕐 Time",
                f"{int(transaction.get('Hour', 0)):02d}:"
                f"{int(transaction.get('Minute', 0)):02d}",
                "Transaction Time",
                "#facc15",
            ),
            (
                "🔄 Frequency",
                str(transaction.get("Transaction_Count", "N/A")),
                "Transaction Count",
                "#8b5cf6",
            ),
        ]

        evidence_cols = st.columns(3)

        for i, (label, value, desc, color) in enumerate(evidence_rows):
            with evidence_cols[i % 3]:
                st.html(
                    f"""
                    <div class="analysis-item">
                        <div class="analysis-item-title">
                            {html.escape(label)}
                        </div>

                        <div class="analysis-item-value"
                             style="color:{color};">
                            {html.escape(value)}
                        </div>

                        <div style="
                            color:#64748b;
                            font-size:11px;
                            margin-top:5px;
                        ">
                            {html.escape(desc)}
                        </div>
                    </div>
                    """
                )

        # ----------------------------------------------------
        # CASE DECISION
        # ----------------------------------------------------

        st.html(
            f"""
            <div style="
                margin-top:20px;
                padding:24px;
                border-radius:20px;
                background:
                    linear-gradient(
                        135deg,
                        rgba(127,29,29,.30),
                        rgba(30,27,75,.50)
                    );
                border:1px solid {action_color}55;
                box-shadow:0 0 30px {action_color}12;
            ">

                <div style="
                    color:#64748b;
                    font-size:11px;
                    letter-spacing:1px;
                    font-weight:800;
                ">
                    CASE DECISION
                </div>

                <div style="
                    color:{action_color};
                    font-size:27px;
                    font-weight:900;
                    margin-top:6px;
                ">
                    {action_icon} {recommended_action}
                </div>

                <div style="
                    color:#94a3b8;
                    font-size:12px;
                    margin-top:8px;
                    line-height:1.6;
                ">
                    This recommendation combines the machine-learning
                    signal, rule-based risk score, and transaction
                    evidence. It is an analytical recommendation and
                    should be reviewed by an authorized fraud analyst
                    before final action.
                </div>

            </div>
            """
        )


        # ====================================================
        # AI INVESTIGATION
        # ====================================================

        st.html(
            """
            <div class="section-title">
                <span style="color:#a78bfa;">◆</span>
                AI Investigation
            </div>

            <div class="ai-header">

                <div class="ai-title">
                    ⚡ Groq AI Investigation Assistant
                </div>

                <div class="ai-description">
                    Generate an evidence-based fraud
                    investigation report from ML and
                    Risk Engine results.
                </div>

            </div>
            """
        )

        if st.button(
            "🧠 GENERATE AI INVESTIGATION",
            use_container_width=True,
        ):

            if FraudInvestigator is None:

                st.error(
                    "AI Investigator import failed."
                )

                st.code(
                    AI_IMPORT_ERROR
                )

            else:

                try:

                    with st.spinner(
                        "🧠 Groq AI is investigating..."
                    ):

                        investigator = (
                            FraudInvestigator()
                        )

                        report = (
                            investigator.investigate(
                                transaction,
                                ml_result,
                                risk_result,
                            )
                        )

                    st.session_state[
                        "investigation_report"
                    ] = report

                except Exception as e:

                    st.error(
                        f"AI investigation failed: {e}"
                    )


        if (
            "investigation_report"
            in st.session_state
        ):

            report = st.session_state[
                "investigation_report"
            ]

            st.markdown(report)

            st.download_button(
                label="📄 DOWNLOAD INVESTIGATION REPORT",
                data=report,
                file_name=(
                    "AI_FraudGuard_"
                    "Investigation_Report.txt"
                ),
                mime="text/plain",
                use_container_width=True,
            )


# ============================================================
# PHASE 6.5 - BULK FRAUD SCANNER
# ============================================================

elif page == "📦 Bulk Fraud Scanner":

    st.html(
        """
        <div class="section-title">
            <span style="color:#22d3ee;">◆</span>
            Bulk Fraud Scanner
        </div>

        <p style="color:#64748b;">
            Upload transaction data and run ML-based fraud screening
            across multiple records.
        </p>
        """
    )

    st.html(
        """
        <div class="bulk-dropzone">
            <div style="
                color:#67e8f9;
                font-size:18px;
                font-weight:900;
            ">
                📥 Upload Transaction CSV
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                margin-top:6px;
            ">
                Use the same feature structure as the training dataset.
            </div>
        </div>
        """
    )

    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"],
        key="bulk_fraud_csv",
    )

    if uploaded_file is not None:

        try:
            bulk_df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"CSV loading failed: {e}")
            st.stop()

        st.html(
            """
            <div class="section-title">
                <span style="color:#a78bfa;">◆</span>
                Uploaded Dataset
            </div>
            """
        )

        st.dataframe(
            bulk_df.head(20),
            use_container_width=True,
            hide_index=True,
        )

        if st.button(
            "⚡ RUN BULK FRAUD SCAN",
            use_container_width=True,
            type="primary",
        ):

            results = []
            progress = st.progress(0)

            for index, row in bulk_df.iterrows():

                transaction = row.to_dict()

                # ------------------------------------------------
                # BULK SCANNER FEATURE PREPARATION
                # The trained model expects Hour/Minute and
                # derived behavioral features. Build them from
                # the uploaded CSV before prediction.
                # ------------------------------------------------

                # Convert Time (HH:MM) into Hour and Minute
                if "Time" in transaction:
                    time_value = str(transaction.get("Time", "")).strip()

                    try:
                        parts = time_value.split(":")
                        transaction["Hour"] = int(parts[0])
                        transaction["Minute"] = int(parts[1])
                    except (ValueError, IndexError):
                        transaction["Hour"] = int(
                            transaction.get("Hour", 0) or 0
                        )
                        transaction["Minute"] = int(
                            transaction.get("Minute", 0) or 0
                        )

                # Ensure derived behavioral features exist
                if "New_Device" not in transaction:
                    device_value = str(
                        transaction.get("Device", "")
                    ).strip().lower()

                    transaction["New_Device"] = (
                        1 if device_value == "new" else 0
                    )

                if "High_Transaction_Frequency" not in transaction:
                    try:
                        tx_count = float(
                            transaction.get(
                                "Transaction_Count",
                                0,
                            )
                        )
                    except (TypeError, ValueError):
                        tx_count = 0

                    transaction[
                        "High_Transaction_Frequency"
                    ] = 1 if tx_count >= 10 else 0

                # Class is the ground-truth label, not an input feature.
                transaction.pop("Class", None)

                try:
                    ml_result = predictor.predict(transaction)

                    fraud_probability = float(
                        ml_result["fraud_probability"]
                    )

                    prediction = int(
                        ml_result.get(
                            "prediction",
                            1 if fraud_probability >= 0.19 else 0,
                        )
                    )

                    transaction_id = transaction.get(
                        "Transaction_ID",
                        f"ROW-{index + 1:05d}",
                    )

                    prediction_label = (
                        "FRAUD"
                        if prediction == 1
                        else "NORMAL"
                    )

                    results.append(
                        {
                            "Row": index + 1,
                            "Transaction_ID": transaction_id,
                            "Fraud_Probability": round(
                                fraud_probability,
                                2,
                            ),
                            "Prediction": prediction_label,
                        }
                    )

                    # Phase 8.1: create a persistent alert whenever
                    # the operational ML threshold flags a transaction.
                    if prediction == 1 or fraud_probability >= 0.19:
                        create_fraud_alert(
                            transaction_id=transaction_id,
                            severity=get_alert_severity(
                                fraud_probability
                            ),
                            fraud_probability=fraud_probability,
                            prediction=prediction_label,
                            transaction=transaction,
                            reason=get_alert_reason(
                                transaction,
                                fraud_probability,
                            ),
                        )

                except Exception as e:

                    results.append(
                        {
                            "Row": index + 1,
                            "Transaction_ID": transaction.get(
                                "Transaction_ID",
                                f"ROW-{index + 1:05d}",
                            ),
                            "Fraud_Probability": None,
                            "Prediction": f"ERROR: {e}",
                        }
                    )

                progress.progress(
                    (index + 1) / len(bulk_df)
                )

            result_df = pd.DataFrame(results)

            st.session_state[
                "bulk_scan_results"
            ] = result_df

    if "bulk_scan_results" in st.session_state:

        result_df = st.session_state[
            "bulk_scan_results"
        ]

        valid_results = result_df[
            result_df["Prediction"].isin(
                ["FRAUD", "NORMAL"]
            )
        ]

        fraud_count = int(
            (valid_results["Prediction"] == "FRAUD").sum()
        )

        normal_count = int(
            (valid_results["Prediction"] == "NORMAL").sum()
        )

        total_scanned = len(valid_results)

        fraud_rate_bulk = (
            fraud_count / total_scanned * 100
            if total_scanned
            else 0
        )

        st.html(
            """
            <div class="section-title">
                <span style="color:#fb7185;">◆</span>
                Scan Results
            </div>
            """
        )

        bulk_cols = st.columns(4)

        stats = [
            (
                "📊",
                "SCANNED",
                f"{total_scanned:,}",
                "#22d3ee",
            ),
            (
                "🚨",
                "FRAUD",
                f"{fraud_count:,}",
                "#fb7185",
            ),
            (
                "🟢",
                "NORMAL",
                f"{normal_count:,}",
                "#22c55e",
            ),
            (
                "⚡",
                "FRAUD RATE",
                f"{fraud_rate_bulk:.2f}%",
                "#a78bfa",
            ),
        ]

        for col, (icon, label, value, color) in zip(
            bulk_cols,
            stats,
        ):

            with col:

                st.html(
                    f"""
                    <div class="bulk-stat">

                        <div class="metric-icon">
                            {icon}
                        </div>

                        <div class="metric-label">
                            {label}
                        </div>

                        <div
                            class="metric-value"
                            style="color:{color};"
                        >
                            {value}
                        </div>

                    </div>
                    """
                )

        st.write("")

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = result_df.to_csv(
            index=False
        )

        st.download_button(
            "📥 DOWNLOAD BULK SCAN RESULTS",
            data=csv_data,
            file_name="AI_FraudGuard_Bulk_Scan.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ============================================================
# PHASE 6.6 - FRAUD ANALYTICS & VISUALIZATION
# ============================================================

elif page == "🚨 Fraud Alert Center":

    st.html(
        """
        <div class="section-title">
            <span style="color:#fb7185;">◆</span>
            Fraud Alert Center
        </div>
        <p style="color:#94a3b8;">
            Centralized monitoring of ML-generated fraud alerts.
            Critical and high-risk transactions appear here for review.
        </p>
        """
    )

    total_alerts, open_alerts, critical_alerts, high_alerts = (
        get_fraud_alert_counts()
    )

    alert_cols = st.columns(4)

    alert_stats = [
        ("🚨", "TOTAL ALERTS", total_alerts, "#22d3ee"),
        ("🔓", "OPEN ALERTS", open_alerts, "#f59e0b"),
        ("🛑", "CRITICAL", critical_alerts, "#fb7185"),
        ("⚠️", "HIGH", high_alerts, "#a78bfa"),
    ]

    for col, (icon, label, value, color) in zip(
        alert_cols,
        alert_stats,
    ):
        with col:
            st.html(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value"
                         style="color:{color};">
                        {value:,}
                    </div>
                </div>
                """
            )

    st.markdown("### 🔎 Alert Filter")

    filter_col, action_col = st.columns([2, 1])

    with filter_col:
        alert_filter = st.selectbox(
            "Alert Status",
            ["OPEN", "RESOLVED", "ALL"],
            key="fraud_alert_filter",
        )

    with action_col:
        if st.button(
            "🔄 Refresh Alerts",
            use_container_width=True,
            key="refresh_fraud_alerts",
        ):
            st.rerun()

    alerts_df = get_fraud_alerts(
        status=alert_filter,
        limit=300,
    )

    if alerts_df.empty:
        st.success(
            "✅ No fraud alerts found for the selected filter."
        )
    else:
        display_df = alerts_df.copy()

        if "Fraud_Probability" in display_df.columns:
            display_df["Fraud_Probability"] = (
                display_df["Fraud_Probability"].round(2)
            )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("### 🧾 Alert Investigation")

        selectable = alerts_df[
            ["Alert_ID", "Transaction_ID", "Severity", "Status"]
        ].copy()

        selectable["Label"] = selectable.apply(
            lambda row: (
                f"#{int(row['Alert_ID'])} • "
                f"{row['Transaction_ID']} • "
                f"{row['Severity']} • "
                f"{row['Status']}"
            ),
            axis=1,
        )

        selected_label = st.selectbox(
            "Select alert",
            selectable["Label"].tolist(),
            key="selected_fraud_alert",
        )

        selected_row = selectable[
            selectable["Label"] == selected_label
        ].iloc[0]

        selected_alert = alerts_df[
            alerts_df["Alert_ID"] == selected_row["Alert_ID"]
        ].iloc[0]

        detail_cols = st.columns(4)

        detail_items = [
            (
                "Transaction",
                selected_alert["Transaction_ID"],
            ),
            (
                "Severity",
                selected_alert["Severity"],
            ),
            (
                "Probability",
                f"{float(selected_alert['Fraud_Probability']):.2f}%",
            ),
            (
                "Status",
                selected_alert["Status"],
            ),
        ]

        for col, (label, value) in zip(
            detail_cols,
            detail_items,
        ):
            with col:
                st.metric(label, value)

        st.html(
            f"""
            <div class="hero" style="margin-top:15px;">
                <div style="
                    color:#67e8f9;
                    font-size:12px;
                    letter-spacing:1px;
                    font-weight:900;
                ">
                    ALERT DETAILS
                </div>

                <div style="
                    color:#f8fafc;
                    font-size:18px;
                    font-weight:900;
                    margin-top:8px;
                ">
                    {html.escape(str(selected_alert["Transaction_ID"]))}
                </div>

                <div style="
                    color:#cbd5e1;
                    margin-top:10px;
                    line-height:1.8;
                ">
                    <b>Location:</b>
                    {html.escape(str(selected_alert["Location"]))}<br>

                    <b>Amount:</b>
                    ₹{float(selected_alert["Amount"]):,.2f}<br>

                    <b>Merchant:</b>
                    {html.escape(str(selected_alert["Merchant_Category"]))}<br>

                    <b>Device:</b>
                    {html.escape(str(selected_alert["Device"]))}<br>

                    <b>Reason:</b>
                    {html.escape(str(selected_alert["Reason"]))}<br>

                    <b>Created:</b>
                    {html.escape(str(selected_alert["Created_At"]))}
                </div>
            </div>
            """
        )

        if selected_alert["Status"] == "OPEN":
            if st.button(
                "✅ RESOLVE SELECTED ALERT",
                type="primary",
                use_container_width=True,
                key="resolve_selected_fraud_alert",
            ):
                current_user = st.session_state.get(
                    "logged_in_admin",
                    "UNKNOWN",
                )

                resolve_fraud_alert(
                    selected_alert["Alert_ID"],
                    current_user,
                )

                log_audit(
                    current_user,
                    "FRAUD_ALERT_RESOLVE",
                    "SUCCESS",
                    f"Alert #{int(selected_alert['Alert_ID'])} / "
                    f"{selected_alert['Transaction_ID']}",
                )

                st.success("✅ Alert resolved successfully.")
                st.rerun()


elif page == "🗂️ Investigation Cases":
    st.markdown("## 🗂️ Investigation Case Management")
    st.caption("Alert → Case → Evidence → Investigation → Resolution → Report")

    cases_df = get_cases("ALL")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cases", len(cases_df))
    c2.metric(
        "Open",
        int((cases_df["Status"] == "OPEN").sum()) if not cases_df.empty else 0,
    )
    c3.metric(
        "Investigating",
        int((cases_df["Status"] == "INVESTIGATING").sum()) if not cases_df.empty else 0,
    )
    c4.metric(
        "Resolved",
        int(cases_df["Status"].isin(["RESOLVED", "CLOSED"]).sum())
        if not cases_df.empty else 0,
    )

    alerts = get_fraud_alerts("ALL", 500)
    if not alerts.empty:
        open_alerts = alerts[alerts["Status"] == "OPEN"]

        if not open_alerts.empty:
            st.markdown("### 🚨 Create Case from Alert")
            opts = open_alerts.apply(
                lambda r: (
                    f"#{int(r['Alert_ID'])} • "
                    f"{r['Transaction_ID']} • {r['Severity']}"
                ),
                axis=1,
            ).tolist()

            choice = st.selectbox(
                "Alert",
                opts,
                key="case_alert_choice",
            )
            alert_row = open_alerts.iloc[opts.index(choice)]

            if st.button(
                "➕ Create Investigation Case",
                type="primary",
                use_container_width=True,
            ):
                user = st.session_state.get(
                    "logged_in_admin",
                    "UNKNOWN",
                )
                case_id = create_investigation_case(
                    alert_row["Alert_ID"],
                    alert_row["Transaction_ID"],
                    alert_row["Severity"],
                    user,
                )
                log_audit(
                    user,
                    "CASE_CREATE",
                    "SUCCESS",
                    case_id,
                )
                st.success(f"✅ Case {case_id} created.")
                st.rerun()

    if cases_df.empty:
        st.info("No investigation cases yet.")
    else:
        st.dataframe(
            cases_df,
            use_container_width=True,
            hide_index=True,
        )

        case_choices = cases_df["Case_ID"].tolist()
        selected_case = st.selectbox(
            "Select Case",
            case_choices,
            key="case_select",
        )
        current = cases_df[
            cases_df["Case_ID"] == selected_case
        ].iloc[0]

        st.markdown("### 🔎 Case Investigation")

        info_cols = st.columns(4)
        info_cols[0].metric("Case", str(current["Case_ID"]))
        info_cols[1].metric("Transaction", str(current["Transaction_ID"]))
        info_cols[2].metric("Priority", str(current["Priority"]))
        info_cols[3].metric("Status", str(current["Status"]))

        left, right = st.columns(2)

        with left:
            status_options = [
                "OPEN",
                "INVESTIGATING",
                "RESOLVED",
                "CLOSED",
            ]
            outcome_options = [
                "PENDING",
                "CONFIRMED_FRAUD",
                "FALSE_POSITIVE",
                "INCONCLUSIVE",
            ]

            current_status = (
                current["Status"]
                if current["Status"] in status_options
                else "OPEN"
            )
            current_outcome = (
                current["Outcome"]
                if current["Outcome"] in outcome_options
                else "PENDING"
            )

            status = st.selectbox(
                "Case Status",
                status_options,
                index=status_options.index(current_status),
                key=f"case_status_{selected_case}",
            )

            outcome = st.selectbox(
                "Final Outcome",
                outcome_options,
                index=outcome_options.index(current_outcome),
                key=f"case_outcome_{selected_case}",
            )

        with right:
            assigned = st.text_input(
                "Assigned Analyst",
                value=str(current["Assigned_To"] or ""),
                key=f"case_assigned_{selected_case}",
            )

            notes = st.text_area(
                "Investigation Notes",
                value=str(current["Notes"] or ""),
                height=130,
                key=f"case_notes_{selected_case}",
            )

        if st.button(
            "💾 Update Case",
            type="primary",
            use_container_width=True,
            key=f"update_case_{selected_case}",
        ):
            user = st.session_state.get(
                "logged_in_admin",
                "UNKNOWN",
            )

            update_case(
                selected_case,
                status,
                outcome,
                assigned,
                notes,
            )

            log_audit(
                user,
                "CASE_UPDATE",
                "SUCCESS",
                f"{selected_case}: {status}/{outcome}",
            )

            st.success("✅ Case updated and timeline recorded.")
            st.rerun()

        # ----------------------------------------------------
        # EVIDENCE MANAGEMENT
        # ----------------------------------------------------
        st.markdown("### 📎 Evidence Management")

        ev_left, ev_right = st.columns([1, 1.35])

        with ev_left:
            evidence_file = st.file_uploader(
                "Upload Evidence",
                type=[
                    "png", "jpg", "jpeg", "pdf",
                    "txt", "csv", "xlsx",
                    "json", "log",
                ],
                key=f"evidence_upload_{selected_case}",
                help="Maximum recommended size: 10 MB.",
            )

            evidence_type = st.selectbox(
                "Evidence Type",
                [
                    "Transaction Screenshot",
                    "Bank Statement",
                    "Device Evidence",
                    "Customer Verification",
                    "Merchant Evidence",
                    "System Log",
                    "Other",
                ],
                key=f"evidence_type_{selected_case}",
            )

            evidence_description = st.text_area(
                "Evidence Description",
                placeholder="Explain why this evidence is relevant...",
                height=100,
                key=f"evidence_desc_{selected_case}",
            )

            if st.button(
                "📎 Attach Evidence",
                use_container_width=True,
                key=f"attach_evidence_{selected_case}",
            ):
                if evidence_file is None:
                    st.error("Please select an evidence file.")
                elif evidence_file.size > 10 * 1024 * 1024:
                    st.error("Evidence file is larger than 10 MB.")
                else:
                    user = st.session_state.get(
                        "logged_in_admin",
                        "UNKNOWN",
                    )

                    safe_name = os.path.basename(
                        evidence_file.name
                    )
                    case_dir = os.path.join(
                        CASE_EVIDENCE_DIR,
                        selected_case,
                    )
                    os.makedirs(case_dir, exist_ok=True)

                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S_%f"
                    )
                    saved_name = (
                        f"{timestamp}_{safe_name}"
                    )
                    saved_path = os.path.join(
                        case_dir,
                        saved_name,
                    )

                    with open(saved_path, "wb") as f:
                        f.write(evidence_file.getbuffer())

                    evidence_id = add_case_evidence(
                        selected_case,
                        safe_name,
                        evidence_type,
                        evidence_description,
                        saved_path,
                        evidence_file.size,
                        user,
                    )

                    log_audit(
                        user,
                        "EVIDENCE_UPLOAD",
                        "SUCCESS",
                        f"{selected_case} / Evidence #{evidence_id}",
                    )

                    st.success(
                        f"✅ Evidence #{evidence_id} attached."
                    )
                    st.rerun()

        with ev_right:
            evidence_df = get_case_evidence(selected_case)

            if evidence_df.empty:
                st.info("No evidence attached to this case yet.")
            else:
                display_evidence = evidence_df.copy()
                display_evidence["Size"] = (
                    display_evidence["Size_Bytes"]
                    .fillna(0)
                    .astype(int)
                    .map(
                        lambda x: (
                            f"{x / 1024:.1f} KB"
                            if x < 1024 * 1024
                            else f"{x / (1024 * 1024):.1f} MB"
                        )
                    )
                )

                st.dataframe(
                    display_evidence[
                        [
                            "Evidence_ID",
                            "Evidence",
                            "Type",
                            "Description",
                            "Size",
                            "Added_By",
                            "Timestamp",
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

                for _, ev in evidence_df.iterrows():
                    file_path = str(ev["File_Path"] or "")
                    if file_path and os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                f"⬇️ {ev['Evidence']}",
                                data=f.read(),
                                file_name=str(ev["Evidence"]),
                                key=(
                                    f"download_ev_"
                                    f"{selected_case}_{int(ev['Evidence_ID'])}"
                                ),
                                use_container_width=True,
                            )

        # ----------------------------------------------------
        # NOTES HISTORY + TIMELINE
        # ----------------------------------------------------
        st.markdown("### 📝 Investigation Notes History")

        notes_df = get_case_notes(selected_case)
        if notes_df.empty:
            st.info("No separate investigation notes recorded yet.")
        else:
            st.dataframe(
                notes_df,
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("### 🕒 Case Activity Timeline")

        timeline_df = get_case_timeline(selected_case)
        if timeline_df.empty:
            st.info("No case activity recorded yet.")
        else:
            for _, event in timeline_df.iterrows():
                st.html(
                    f"""
                    <div class="analysis-item">
                        <div class="analysis-item-title">
                            {html.escape(str(event["Timestamp"]))}
                            &nbsp; • &nbsp;
                            {html.escape(str(event["User"]))}
                        </div>
                        <div class="analysis-item-value"
                             style="font-size:15px;">
                            {html.escape(str(event["Action"]))}
                        </div>
                        <div style="
                            color:#94a3b8;
                            margin-top:5px;
                            font-size:12px;
                        ">
                            {html.escape(str(event["Details"] or ""))}
                        </div>
                    </div>
                    """
                )

        # ----------------------------------------------------
        # CASE-SPECIFIC REPORT
        # ----------------------------------------------------
        st.markdown("### 📄 Investigation Case Report")

        report = build_case_report(
            current,
            notes_df,
            get_case_evidence(selected_case),
            timeline_df,
        )

        st.download_button(
            "⬇️ Download Complete Case Report",
            data=report,
            file_name=(
                f"{selected_case}_investigation_report.txt"
            ),
            mime="text/plain",
            use_container_width=True,
            key=f"case_report_{selected_case}",
        )

        with st.expander("👀 Preview Case Report"):
            st.text(report)


elif page == "🧠 Fraud Intelligence":
    st.markdown("## 🧠 Fraud Intelligence")
    st.caption("Advanced fraud patterns from the alert history.")

    df = load_alert_analytics()
    if df.empty:
        st.info("No alert data available yet. Run the Bulk Fraud Scanner.")
    else:
        a, b, c, d = st.columns(4)
        a.metric("Alerts", len(df))
        b.metric("Critical", int((df["severity"] == "CRITICAL").sum()))
        c.metric("High", int((df["severity"] == "HIGH").sum()))
        d.metric("Open", int((df["status"] == "OPEN").sum()))

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📍 Alerts by Location")
            st.bar_chart(df["location"].value_counts())
        with col2:
            st.markdown("### 🏪 Alerts by Merchant")
            st.bar_chart(df["merchant_category"].value_counts())

        st.markdown("### 📱 Alerts by Device")
        st.bar_chart(df["device"].value_counts())

        st.markdown("### 📊 Severity Distribution")
        st.bar_chart(df["severity"].value_counts())


elif page == "👤 Customer & Device Intelligence":
    st.markdown("## 👤 Customer & Device Intelligence")
    st.caption("Behavioral and device-level risk overview.")

    # Use the application's loaded transaction dataset when available.
    source_df = None
    for candidate in ["df", "data", "dataset", "transactions_df"]:
        if candidate in locals() and isinstance(locals()[candidate], pd.DataFrame):
            source_df = locals()[candidate]
            break

    if source_df is None or source_df.empty:
        st.info("Transaction dataset is not available on this page.")
    else:
        intelligence = get_customer_intelligence(source_df)
        if intelligence.empty:
            st.info("No customer/device grouping fields are available.")
        else:
            st.dataframe(intelligence, use_container_width=True, hide_index=True)

        alerts = get_fraud_alerts("ALL", 500)
        if not alerts.empty:
            st.markdown("### 🔐 Suspicious Devices")
            device_summary = (
                alerts.groupby("Device")
                .agg(
                    Alerts=("Alert_ID", "count"),
                    Open_Alerts=("Status", lambda x: int((x == "OPEN").sum())),
                    Avg_Probability=("Fraud_Probability", "mean"),
                )
                .reset_index()
                .sort_values("Alerts", ascending=False)
            )
            device_summary["Avg_Probability"] = device_summary["Avg_Probability"].round(2)
            st.dataframe(device_summary, use_container_width=True, hide_index=True)


elif page == "📑 Reports":
    st.markdown("## 📑 Professional Reports")
    st.caption("Export fraud alerts and investigation cases.")

    alerts = get_fraud_alerts("ALL", 500)
    cases = get_cases("ALL", 500)

    report_text = build_fraud_report(alerts, cases)

    st.download_button(
        "⬇️ Download Fraud Investigation Report",
        data=report_text,
        file_name=f"fraudguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    if not alerts.empty:
        st.download_button(
            "⬇️ Download Alerts CSV",
            data=alerts.to_csv(index=False).encode("utf-8"),
            file_name="fraud_alerts.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if not cases.empty:
        st.download_button(
            "⬇️ Download Cases CSV",
            data=cases.to_csv(index=False).encode("utf-8"),
            file_name="investigation_cases.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("### 👀 Report Preview")
    st.text_area("Report", report_text, height=420)


elif page == "📈 Fraud Analytics":


    st.html(
        """
        <div class="section-title">
            <span style="color:#22d3ee;">◆</span>
            Fraud Analytics & Visualization
        </div>

        <p style="color:#64748b;">
            Explore fraud patterns across amount, location, device,
            merchant category and transaction time.
        </p>
        """
    )

    # --------------------------------------------------------
    # DATA PREPARATION
    # --------------------------------------------------------

    analytics_df = df.copy()

    # Normalize common columns if available
    if "Class" in analytics_df.columns:
        analytics_df["Fraud_Label"] = analytics_df["Class"].map(
            {0: "Normal", 1: "Fraud"}
        ).fillna(analytics_df["Class"].astype(str))
    else:
        analytics_df["Fraud_Label"] = "Unknown"

    if "Amount" in analytics_df.columns:
        analytics_df["Amount"] = pd.to_numeric(
            analytics_df["Amount"],
            errors="coerce",
        )

    # Time parsing
    if "Time" in analytics_df.columns:
        parsed_time = pd.to_datetime(
            analytics_df["Time"].astype(str),
            format="%H:%M",
            errors="coerce",
        )
        analytics_df["Analysis_Hour"] = parsed_time.dt.hour
    elif "Hour" in analytics_df.columns:
        analytics_df["Analysis_Hour"] = pd.to_numeric(
            analytics_df["Hour"],
            errors="coerce",
        )
    else:
        analytics_df["Analysis_Hour"] = None

    # --------------------------------------------------------
    # TOP ANALYTICS METRICS
    # --------------------------------------------------------

    total_txn = len(analytics_df)

    fraud_txn = int(
        (analytics_df["Fraud_Label"] == "Fraud").sum()
    )

    normal_txn = int(
        (analytics_df["Fraud_Label"] == "Normal").sum()
    )

    fraud_rate = (
        fraud_txn / total_txn * 100
        if total_txn
        else 0
    )

    if (
        "Amount" in analytics_df.columns
        and analytics_df["Amount"].notna().any()
    ):
        avg_amount = analytics_df["Amount"].mean()
        fraud_amount = analytics_df.loc[
            analytics_df["Fraud_Label"] == "Fraud",
            "Amount",
        ].mean()
    else:
        avg_amount = 0
        fraud_amount = 0

    metric_cols = st.columns(4)

    analytics_metrics = [
        (
            "📊",
            "TOTAL TRANSACTIONS",
            f"{total_txn:,}",
            "#22d3ee",
        ),
        (
            "🚨",
            "FRAUD CASES",
            f"{fraud_txn:,}",
            "#fb7185",
        ),
        (
            "⚡",
            "FRAUD RATE",
            f"{fraud_rate:.2f}%",
            "#a78bfa",
        ),
        (
            "💰",
            "AVG AMOUNT",
            f"₹{avg_amount:,.0f}",
            "#22c55e",
        ),
    ]

    for col, (icon, label, value, color) in zip(
        metric_cols,
        analytics_metrics,
    ):
        with col:
            st.html(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value"
                         style="color:{color};">
                        {value}
                    </div>
                </div>
                """
            )

    # --------------------------------------------------------
    # FRAUD VS NORMAL
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-title">
            <span style="color:#fb7185;">◆</span>
            Fraud Distribution
        </div>
        """
    )

    chart_left, chart_right = st.columns(2)

    with chart_left:

        st.html(
            """
            <div class="analytics-card">
                <div class="analytics-title">
                    🚨 Fraud vs Normal
                </div>
                <div class="analytics-subtitle">
                    Overall transaction classification
                </div>
            </div>
            """
        )

        distribution = pd.DataFrame(
            {
                "Transactions": [
                    normal_txn,
                    fraud_txn,
                ]
            },
            index=[
                "Normal",
                "Fraud",
            ],
        )

        st.bar_chart(
            distribution,
            use_container_width=True,
        )

    with chart_right:

        st.html(
            """
            <div class="analytics-card">
                <div class="analytics-title">
                    💰 Amount Comparison
                </div>
                <div class="analytics-subtitle">
                    Average transaction value
                </div>
            </div>
            """
        )

        amount_compare = pd.DataFrame(
            {
                "Average Amount": [
                    avg_amount,
                    fraud_amount if pd.notna(fraud_amount) else 0,
                ]
            },
            index=[
                "All Transactions",
                "Fraud Transactions",
            ],
        )

        st.bar_chart(
            amount_compare,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # LOCATION ANALYSIS
    # --------------------------------------------------------

    if "Location" in analytics_df.columns:

        st.html(
            """
            <div class="section-title">
                <span style="color:#22d3ee;">◆</span>
                Location Intelligence
            </div>
            """
        )

        location_data = (
            analytics_df.groupby(
                ["Location", "Fraud_Label"]
            )
            .size()
            .unstack(fill_value=0)
        )

        if not location_data.empty:

            location_left, location_right = st.columns(2)

            with location_left:

                st.html(
                    """
                    <div class="analytics-card">
                        <div class="analytics-title">
                            📍 Transactions by Location
                        </div>
                        <div class="analytics-subtitle">
                            Normal and suspicious activity by location
                        </div>
                    </div>
                    """
                )

                st.bar_chart(
                    location_data,
                    use_container_width=True,
                )

            with location_right:

                location_fraud = (
                    analytics_df[
                        analytics_df["Fraud_Label"] == "Fraud"
                    ]
                    .groupby("Location")
                    .size()
                    .sort_values(
                        ascending=False
                    )
                )

                st.html(
                    """
                    <div class="analytics-card">
                        <div class="analytics-title">
                            🚨 Top Fraud Locations
                        </div>
                        <div class="analytics-subtitle">
                            Locations with the highest fraud count
                        </div>
                    </div>
                    """
                )

                if not location_fraud.empty:
                    st.bar_chart(
                        location_fraud,
                        use_container_width=True,
                    )
                else:
                    st.info(
                        "No fraud-location records available."
                    )

    # --------------------------------------------------------
    # MERCHANT ANALYSIS
    # --------------------------------------------------------

    if "Merchant_Category" in analytics_df.columns:

        st.html(
            """
            <div class="section-title">
                <span style="color:#a78bfa;">◆</span>
                Merchant Intelligence
            </div>
            """
        )

        merchant_data = (
            analytics_df.groupby(
                ["Merchant_Category", "Fraud_Label"]
            )
            .size()
            .unstack(fill_value=0)
        )

        merchant_left, merchant_right = st.columns(2)

        with merchant_left:

            st.html(
                """
                <div class="analytics-card">
                    <div class="analytics-title">
                        🏪 Merchant Category Distribution
                    </div>
                    <div class="analytics-subtitle">
                        Transaction volume by merchant category
                    </div>
                </div>
                """
            )

            st.bar_chart(
                merchant_data,
                use_container_width=True,
            )

        with merchant_right:

            merchant_fraud = (
                analytics_df[
                    analytics_df["Fraud_Label"] == "Fraud"
                ]
                .groupby("Merchant_Category")
                .size()
                .sort_values(
                    ascending=False
                )
            )

            st.html(
                """
                <div class="analytics-card">
                    <div class="analytics-title">
                        🚨 Fraud by Merchant
                    </div>
                    <div class="analytics-subtitle">
                        Categories generating the most fraud cases
                    </div>
                </div>
                """
            )

            if not merchant_fraud.empty:
                st.bar_chart(
                    merchant_fraud,
                    use_container_width=True,
                )
            else:
                st.info(
                    "No merchant-level fraud data available."
                )

    # --------------------------------------------------------
    # DEVICE ANALYSIS
    # --------------------------------------------------------

    if "Device" in analytics_df.columns:

        st.html(
            """
            <div class="section-title">
                <span style="color:#22d3ee;">◆</span>
                Device Intelligence
            </div>
            """
        )

        device_data = (
            analytics_df.groupby(
                ["Device", "Fraud_Label"]
            )
            .size()
            .unstack(fill_value=0)
        )

        device_left, device_right = st.columns(2)

        with device_left:

            st.html(
                """
                <div class="analytics-card">
                    <div class="analytics-title">
                        📱 Device Activity
                    </div>
                    <div class="analytics-subtitle">
                        Normal vs fraud transactions by device status
                    </div>
                </div>
                """
            )

            st.bar_chart(
                device_data,
                use_container_width=True,
            )

        with device_right:

            device_fraud = (
                analytics_df[
                    analytics_df["Fraud_Label"] == "Fraud"
                ]
                .groupby("Device")
                .size()
                .sort_values(
                    ascending=False
                )
            )

            st.html(
                """
                <div class="analytics-card">
                    <div class="analytics-title">
                        🚨 Fraud Device Signals
                    </div>
                    <div class="analytics-subtitle">
                        Device statuses associated with fraud
                    </div>
                </div>
                """
            )

            if not device_fraud.empty:
                st.bar_chart(
                    device_fraud,
                    use_container_width=True,
                )
            else:
                st.info(
                    "No device-level fraud data available."
                )

    # --------------------------------------------------------
    # TIME ANALYSIS
    # --------------------------------------------------------

    if analytics_df["Analysis_Hour"].notna().any():

        st.html(
            """
            <div class="section-title">
                <span style="color:#fb7185;">◆</span>
                Time-Based Fraud Intelligence
            </div>
            """
        )

        hourly = (
            analytics_df.dropna(
                subset=["Analysis_Hour"]
            )
            .assign(
                Analysis_Hour=lambda x:
                    x["Analysis_Hour"].astype(int)
            )
            .groupby(
                ["Analysis_Hour", "Fraud_Label"]
            )
            .size()
            .unstack(fill_value=0)
            .reindex(
                range(24),
                fill_value=0,
            )
        )

        st.html(
            """
            <div class="analytics-card">
                <div class="analytics-title">
                    🕐 24-Hour Transaction Pattern
                </div>
                <div class="analytics-subtitle">
                    Identify unusual activity during specific hours
                </div>
            </div>
            """
        )

        st.line_chart(
            hourly,
            use_container_width=True,
        )

        # Night activity
        night_hours = [0, 1, 2, 3, 4, 5, 23]

        night_df = analytics_df[
            analytics_df["Analysis_Hour"].isin(
                night_hours
            )
        ]

        night_fraud = int(
            (
                night_df["Fraud_Label"] == "Fraud"
            ).sum()
        )

        st.html(
            f"""
            <div class="insight-card">
                <div class="insight-label">
                    NIGHT-TIME FRAUD SIGNAL
                </div>
                <div class="insight-value">
                    🌙 {night_fraud:,} fraud transactions
                </div>
                <div style="
                    color:#64748b;
                    font-size:11px;
                    margin-top:5px;
                ">
                    Activity detected during 23:00–05:00
                    monitoring window.
                </div>
            </div>
            """
        )

    # --------------------------------------------------------
    # TOP SUSPICIOUS TRANSACTIONS
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-title">
            <span style="color:#fb7185;">◆</span>
            Top Suspicious Transactions
        </div>
        """
    )

    if "Amount" in analytics_df.columns:

        suspicious = analytics_df[
            analytics_df["Fraud_Label"] == "Fraud"
        ].copy()

        suspicious = suspicious.sort_values(
            "Amount",
            ascending=False,
        )

        display_columns = [
            column
            for column in [
                "Transaction_ID",
                "Amount",
                "Time",
                "Location",
                "Device",
                "Transaction_Count",
                "Merchant_Category",
                "Account_Age_Days",
                "Class",
            ]
            if column in suspicious.columns
        ]

        if not suspicious.empty:

            st.dataframe(
                suspicious[
                    display_columns
                ].head(20),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info(
                "No fraud transactions available."
            )

    # --------------------------------------------------------
    # AUTOMATED ANALYST INSIGHTS
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-title">
            <span style="color:#a78bfa;">◆</span>
            Automated Analyst Insights
        </div>
        """
    )

    insight_cols = st.columns(3)

    # Highest fraud location
    if (
        "Location" in analytics_df.columns
        and fraud_txn > 0
    ):
        location_counts = (
            analytics_df[
                analytics_df["Fraud_Label"] == "Fraud"
            ]
            .groupby("Location")
            .size()
        )

        top_location = (
            location_counts.idxmax()
            if not location_counts.empty
            else "N/A"
        )

        top_location_count = (
            int(location_counts.max())
            if not location_counts.empty
            else 0
        )
    else:
        top_location = "N/A"
        top_location_count = 0

    with insight_cols[0]:
        st.html(
            f"""
            <div class="insight-card">
                <div class="insight-label">
                    TOP FRAUD LOCATION
                </div>
                <div class="insight-value">
                    📍 {html.escape(str(top_location))}
                </div>
                <div style="color:#64748b;font-size:11px;">
                    {top_location_count:,} fraud cases
                </div>
            </div>
            """
        )

    # Highest fraud merchant
    if (
        "Merchant_Category" in analytics_df.columns
        and fraud_txn > 0
    ):
        merchant_counts = (
            analytics_df[
                analytics_df["Fraud_Label"] == "Fraud"
            ]
            .groupby("Merchant_Category")
            .size()
        )

        top_merchant = (
            merchant_counts.idxmax()
            if not merchant_counts.empty
            else "N/A"
        )

        top_merchant_count = (
            int(merchant_counts.max())
            if not merchant_counts.empty
            else 0
        )
    else:
        top_merchant = "N/A"
        top_merchant_count = 0

    with insight_cols[1]:
        st.html(
            f"""
            <div class="insight-card">
                <div class="insight-label">
                    TOP FRAUD MERCHANT
                </div>
                <div class="insight-value">
                    🏪 {html.escape(str(top_merchant))}
                </div>
                <div style="color:#64748b;font-size:11px;">
                    {top_merchant_count:,} fraud cases
                </div>
            </div>
            """
        )

    # Highest fraud hour
    if fraud_txn > 0 and analytics_df["Analysis_Hour"].notna().any():

        hour_counts = (
            analytics_df[
                analytics_df["Fraud_Label"] == "Fraud"
            ]
            .groupby("Analysis_Hour")
            .size()
        )

        top_hour = (
            int(hour_counts.idxmax())
            if not hour_counts.empty
            else 0
        )

        top_hour_count = (
            int(hour_counts.max())
            if not hour_counts.empty
            else 0
        )

        top_hour_text = f"{top_hour:02d}:00"

    else:
        top_hour_text = "N/A"
        top_hour_count = 0

    with insight_cols[2]:
        st.html(
            f"""
            <div class="insight-card">
                <div class="insight-label">
                    PEAK FRAUD HOUR
                </div>
                <div class="insight-value">
                    🕐 {top_hour_text}
                </div>
                <div style="color:#64748b;font-size:11px;">
                    {top_hour_count:,} fraud cases
                </div>
            </div>
            """
        )

    # --------------------------------------------------------
    # EXPORT ANALYTICS SUMMARY
    # --------------------------------------------------------

    summary = pd.DataFrame(
        {
            "Metric": [
                "Total Transactions",
                "Fraud Transactions",
                "Normal Transactions",
                "Fraud Rate",
                "Average Amount",
                "Average Fraud Amount",
                "Top Fraud Location",
                "Top Fraud Merchant",
                "Peak Fraud Hour",
            ],
            "Value": [
                total_txn,
                fraud_txn,
                normal_txn,
                f"{fraud_rate:.2f}%",
                f"{avg_amount:.2f}",
                f"{fraud_amount:.2f}"
                if pd.notna(fraud_amount)
                else "0.00",
                top_location,
                top_merchant,
                top_hour_text,
            ],
        }
    )

    st.download_button(
        "📥 DOWNLOAD ANALYTICS SUMMARY",
        data=summary.to_csv(index=False),
        file_name="AI_FraudGuard_Analytics_Summary.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif page == "📊 Model Performance":

    st.html(
        """
        <div class="section-title">
            <span style="color:#a78bfa;">◆</span>
            ML Model Intelligence
        </div>

        <p style="color:#64748b;">
            Performance comparison of trained fraud detection models.
        </p>
        """
    )

    results_path = os.path.join(
        BASE_DIR,
        "models",
        "v2",
        "model_results_v2.csv",
    )

    if os.path.exists(results_path):

        results = pd.read_csv(
            results_path,
            index_col=0,
        )

        st.dataframe(
            results,
            use_container_width=True,
        )

        st.html(
            """
            <div class="section-title">
                <span style="color:#22d3ee;">◆</span>
                Model Comparison
            </div>
            """
        )

        chart_columns = [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC",
            "PR-AUC",
        ]

        available_columns = [
            column
            for column in chart_columns
            if column in results.columns
        ]

        if available_columns:
            st.bar_chart(
                results[available_columns]
            )

        if "F1 Score" in results.columns:

            best_model = results[
                "F1 Score"
            ].idxmax()

            best_score = results.loc[
                best_model,
                "F1 Score",
            ]

            st.html(
                f"""
                <div class="glass-card">

                    <h3>🏆 Best Model</h3>

                    <div style="
                        color:#67e8f9;
                        font-size:27px;
                        font-weight:900;
                    ">
                        {html.escape(str(best_model))}
                    </div>

                    <div style="
                        color:#94a3b8;
                        margin-top:5px;
                    ">
                        F1 Score:
                        <b>{best_score:.4f}</b>
                    </div>

                </div>
                """
            )

    else:

        st.warning(
            "Model results file not found: "
            "models/v2/model_results_v2.csv"
        )


# ============================================================
# TRANSACTION DATA
# ============================================================

elif page == "📋 Transaction Data":

    st.html(
        """
        <div class="section-title">
            <span style="color:#22d3ee;">◆</span>
            Transaction Intelligence Database
        </div>

        <p style="color:#64748b;">
            Search and explore transaction records.
        </p>
        """
    )

    search = st.text_input(
        "🔎 Search Transaction ID"
    )

    filtered_df = df

    if search and "Transaction_ID" in df.columns:

        filtered_df = df[
            df["Transaction_ID"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=560,
        hide_index=True,
    )

    st.download_button(
        label="⬇️ DOWNLOAD DATASET",
        data=df.to_csv(index=False),
        file_name="AI_FraudGuard_Dataset.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        🛡️
        <span class="footer-highlight">
            AI-FraudGuard
        </span>

        &nbsp; • &nbsp;

        AI Financial Fraud Detection
        & Investigation

        <br><br>

        🤖 ML + SMOTE
        &nbsp; • &nbsp;
        🧠 Groq AI
        &nbsp; • &nbsp;
        🛡️ Risk Intelligence
        &nbsp; • &nbsp;
        🎯 Threat Intelligence

    </div>
    """
)
