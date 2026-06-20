import sqlite3

DB_PATH = "database/disaster_system.db"


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

def get_connection():
    return sqlite3.connect(DB_PATH)


# -----------------------------
# INITIALIZE DATABASE
# -----------------------------

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS broadcasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ALERTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disaster_type TEXT,
        country TEXT,
        severity TEXT,
        latitude REAL,
        longitude REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # RESOURCE DEPLOYMENT TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resource_allocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital TEXT,
        shelter TEXT,
        warehouse TEXT,
        transport_route TEXT,
        disaster_id INTEGER
    )
    """)

    # HELP REQUEST TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS help_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        message TEXT,
        image_path TEXT,
        status TEXT DEFAULT 'PENDING',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# CREATE USER
# -----------------------------

def create_user(username, password, role="admin"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, password, role))

    conn.commit()
    conn.close()


# -----------------------------
# VERIFY LOGIN
# -----------------------------

def verify_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    return user


# -----------------------------
# STORE ALERT
# -----------------------------

def store_alert(disaster_type, country, severity, latitude, longitude):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alerts (disaster_type, country, severity, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, (disaster_type, country, severity, latitude, longitude))

    conn.commit()
    conn.close()


# -----------------------------
# STORE HELP REQUEST
# -----------------------------

def store_help_request(latitude, longitude, message, image_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO help_requests (latitude, longitude, message, image_path)
        VALUES (?, ?, ?, ?)
    """, (latitude, longitude, message, image_path))

    conn.commit()
    conn.close()

def store_broadcast(message):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO broadcasts (message)
        VALUES (?)
    """, (message,))

    conn.commit()
    conn.close()


def get_broadcasts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT message, timestamp
        FROM broadcasts
        ORDER BY timestamp DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()
    conn.close()

    broadcasts = []

    for r in rows:
        broadcasts.append({
            "message": r[0],
            "timestamp": r[1]
        })

    return broadcasts

# -----------------------------
# STORE RESOURCE DEPLOYMENT
# -----------------------------

def store_resource(hospital, shelter, warehouse, route, disaster_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resource_allocations
        (hospital, shelter, warehouse, transport_route, disaster_id)
        VALUES (?, ?, ?, ?, ?)
    """, (hospital, shelter, warehouse, route, disaster_id))

    conn.commit()
    conn.close()


# -----------------------------
# GET ALERTS
# -----------------------------

def get_alerts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT disaster_type, country, severity, latitude, longitude, timestamp
        FROM alerts
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    alerts = []

    for r in rows:
        alerts.append({
            "disaster_type": r[0],
            "country": r[1],
            "severity": r[2],
            "latitude": r[3],
            "longitude": r[4],
            "timestamp": r[5]
        })

    return alerts


# -----------------------------
# GET LATEST ALERT
# -----------------------------

def get_latest_alert():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT disaster_type, country, severity, latitude, longitude
        FROM alerts
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "disaster_type": row[0],
        "country": row[1],
        "severity": row[2],
        "latitude": row[3],
        "longitude": row[4]
    }

def update_help_status(request_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE help_requests
        SET status = ?
        WHERE id = ?
    """, (status, request_id))

    conn.commit()
    conn.close()

# -----------------------------
# GET HELP REQUESTS
# -----------------------------

def get_help_requests():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, latitude, longitude, message, image_path, timestamp
        FROM help_requests
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    requests = []

    for r in rows:
        requests.append({
            "id": r[0],
            "latitude": r[1],
            "longitude": r[2],
            "message": r[3],
            "image_path": r[4],
            "timestamp": r[5]
        })

    return requests