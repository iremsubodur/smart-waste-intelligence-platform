import sqlite3

DB_NAME = "users.db"

# =========================================================
# INIT DB
# =========================================================

def init_user_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        eco_points INTEGER DEFAULT 0
    )

    """)

    conn.commit()

    conn.close()

# =========================================================
# REGISTER
# =========================================================

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    try:

        cursor.execute("""

        INSERT INTO users (
            username,
            password
        )

        VALUES (?, ?)

        """, (

            username,
            password
        ))

        conn.commit()

        conn.close()

        return True

    except:

        conn.close()

        return False

# =========================================================
# LOGIN
# =========================================================

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM users

    WHERE username=?
    AND password=?

    """, (

        username,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user

# =========================================================
# UPDATE ECO POINTS
# =========================================================

def update_eco_points(username, points):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE users

    SET eco_points = eco_points + ?

    WHERE username=?

    """, (

        points,
        username
    ))

    conn.commit()

    conn.close()

# =========================================================
# LEADERBOARD
# =========================================================

def get_leaderboard():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT username, eco_points

    FROM users

    ORDER BY eco_points DESC

    LIMIT 10

    """)

    data = cursor.fetchall()

    conn.close()

    return data