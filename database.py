import mysql.connector
import json
import os

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'mysql'),
    'database': os.getenv('DB_NAME', 'resume_analyzer_app')
}

def get_connection():
    """Returns a MySQL connection to the resume_analyzer database."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        return conn
    except Exception as err:
        print(f"[DB] Connection failed: {err}")
        return None

def init_db():
    """Creates the database and tables if they do not already exist."""
    print("[DB] Running init_db ...")
    try:
        # Connect without specifying the database first
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        db = DB_CONFIG['database']

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db}`")
        conn.database = db

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                role_id VARCHAR(100),
                readiness_score INT,
                analysis_json LONGTEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_roles (
                id VARCHAR(100) PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                skills_json LONGTEXT
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[DB] MySQL database '{db}' initialized OK.")
    except Exception as err:
        print(f"[DB] init_db error: {err}")

def save_report(filename, role_id, readiness_score, analysis_dict):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reports (filename, role_id, readiness_score, analysis_json) VALUES (%s, %s, %s, %s)",
        (filename, role_id, readiness_score, json.dumps(analysis_dict))
    )
    report_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return report_id

def get_reports():
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_report(report_id):
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reports WHERE id = %s", (report_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def save_custom_role(role_id, name, description, skills):
    conn = get_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO custom_roles (id, name, description, skills_json)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            description = VALUES(description),
            skills_json = VALUES(skills_json)
    """, (role_id, name, description, json.dumps(skills)))
    conn.commit()
    cursor.close()
    conn.close()

def get_custom_roles():
    conn = get_connection()
    if not conn:
        return {}
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM custom_roles")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    roles = {}
    for row in rows:
        raw = row['skills_json']
        skills = json.loads(raw) if isinstance(raw, str) else raw
        roles[row['id']] = {
            "name": row['name'],
            "description": row['description'],
            "skills": skills
        }
    return roles

if __name__ == "__main__":
    init_db()
