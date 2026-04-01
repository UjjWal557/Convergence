import mysql.connector

print("Step 1: Connecting to MySQL...")
conn = mysql.connector.connect(host='localhost', user='root', password='')
print("Connected OK")

print("Step 2: Creating database...")
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS `resume_analyzer`")
print("DB created OK")

print("Step 3: Switching to DB...")
cursor.execute("USE `resume_analyzer`")
print("USE DB OK")

print("Step 4: Creating reports table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(255),
        role_id VARCHAR(100),
        readiness_score INT,
        analysis_json JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("reports table OK")

print("Step 5: Creating custom_roles table...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS custom_roles (
        id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(255),
        description TEXT,
        skills_json JSON
    )
''')
print("custom_roles table OK")

conn.commit()
cursor.close()
conn.close()
print("ALL DONE - Database initialized successfully!")
