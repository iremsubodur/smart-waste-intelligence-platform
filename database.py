import sqlite3
from datetime import datetime

DB_NAME = "waste_analytics.db"

# =========================================================
# CREATE DATABASE
# =========================================================

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS detections (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        waste_type TEXT,

        confidence REAL,

        timestamp TEXT
    )

    """)

    conn.commit()

    conn.close()

# =========================================================
# INSERT DETECTION
# =========================================================

def insert_detection(waste_type, confidence):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO detections (
        waste_type,
        confidence,
        timestamp
    )

    VALUES (?, ?, ?)

    """, (

        waste_type,

        confidence,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()

# =========================================================
# FETCH DATA
# =========================================================

def fetch_all_data():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT waste_type, confidence, timestamp
    FROM detections

    """)

    data = cursor.fetchall()

    conn.close()

    return data