import sqlite3


def create_database():

    conn = sqlite3.connect("database/disaster_system.db")
    cursor = conn.cursor()

    # -----------------------------
    # USERS TABLE
    # -----------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # -----------------------------
    # DISASTER ALERTS
    # -----------------------------

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

    # -----------------------------
    # DISASTER EVENTS
    # -----------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disaster_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disaster_type TEXT,
        country TEXT,
        deaths INTEGER,
        affected INTEGER,
        severity TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -----------------------------
    # RESOURCE DEPLOYMENT
    # -----------------------------

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

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully")