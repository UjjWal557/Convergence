import mysql.connector
import sqlite3
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

SQLITE_DB_PATH = 'analyzer.db'


def is_mysql_conn(conn):
    """Checks if the connection is a MySQL connection."""
    if not conn: return False
    return "mysql" in type(conn).__module__.lower()

def get_connection():

    """Returns a MySQL connection or falls back to SQLite if MySQL fails."""
    # Try MySQL first
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

        print(f"[DB] MySQL connection failed (using SQLite fallback): {err}")
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH)
            conn.row_factory = sqlite3.Row # Make it return dict-like objects
            return conn
        except Exception as sqlite_err:

            print(f"[DB] SQLite connection failed: {sqlite_err}")
            return None

def init_db():
    """Creates the database and tables if they do not already exist."""
    print("[DB] Running init_db ...")
    conn = get_connection()
    if not conn:
        print("[DB] Cannot initialize database - no connection available.")
        return

    try:
        cursor = conn.cursor()
        is_mysql = is_mysql_conn(conn)
        if is_mysql:
            # MySQL Initialization
            db = DB_CONFIG['database']
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db}`")
            cursor.execute(f"USE `{db}`")

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
        else:
            # SQLite Initialization
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    role_id TEXT,
                    readiness_score INTEGER,
                    analysis_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_roles (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    skills_json TEXT
                )
            """)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[DB] Database initialized OK (Type: {'MySQL' if is_mysql else 'SQLite'}).")
    except Exception as err:
        print(f"[DB] init_db error: {err}")

def save_report(filename, role_id, readiness_score, analysis_dict):
    conn = get_connection()
    if not conn:
        return None
    try:
        query = "INSERT INTO reports (filename, role_id, readiness_score, analysis_json) VALUES (%s, %s, %s, %s)"
        params = (filename, role_id, readiness_score, json.dumps(analysis_dict))
        
        if not is_mysql_conn(conn):
            query = query.replace('%s', '?')

            
        cursor = conn.cursor()
        cursor.execute(query, params)
        report_id = cursor.lastrowid
        
        conn.commit()
        cursor.close()
        conn.close()
        return report_id
    except Exception as e:
        print(f"[DB] Error saving report: {e}")
        return None

def get_reports():
    conn = get_connection()
    if not conn:
        return []
    try:
        is_mysql = is_mysql_conn(conn)
        cursor = conn.cursor(dictionary=True) if is_mysql else conn.cursor()
        cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        if not is_mysql:
            rows = [dict(r) for r in rows]
            
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"[DB] Error getting reports: {e}")
        return []

def get_report(report_id):
    conn = get_connection()
    if not conn:
        return None
    try:
        is_mysql = is_mysql_conn(conn)
        query = "SELECT * FROM reports WHERE id = %s"
        params = (report_id,)
        if not is_mysql:
            query = query.replace('%s', '?')
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(dictionary=True)
            
        cursor.execute(query, params)
        row = cursor.fetchone()
        
        if row and not is_mysql:
            row = dict(row)
            
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print(f"[DB] Error getting report: {e}")
        return None

def save_custom_role(role_id, name, description, skills):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        if is_mysql_conn(conn):
            cursor.execute("""
                INSERT INTO custom_roles (id, name, description, skills_json)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    description = VALUES(description),
                    skills_json = VALUES(skills_json)
            """, (role_id, name, description, json.dumps(skills)))
        else:
            cursor.execute("""
                INSERT INTO custom_roles (id, name, description, skills_json)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    description = excluded.description,
                    skills_json = excluded.skills_json
            """, (role_id, name, description, json.dumps(skills)))
            
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[DB] Error saving custom role: {e}")

def get_custom_roles():
    conn = get_connection()
    if not conn:
        return {}
    try:
        is_mysql = is_mysql_conn(conn)
        cursor = conn.cursor(dictionary=True) if is_mysql else conn.cursor()
        cursor.execute("SELECT * FROM custom_roles")
        rows = cursor.fetchall()
        
        roles = {}
        for row in rows:
            if not is_mysql:
                row = dict(row)

            raw = row['skills_json']
            skills = json.loads(raw) if isinstance(raw, str) else raw
            roles[row['id']] = {
                "name": row['name'],
                "description": row['description'],
                "skills": skills
            }
        
        cursor.close()
        conn.close()
        return roles
    except Exception as e:
        print(f"[DB] Error getting custom roles: {e}")
        return {}

if __name__ == "__main__":
    init_db()
