import sqlite3
import json

def debug():
    conn = sqlite3.connect('analyzer.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, role_id, analysis_json FROM reports LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row['id']}, File: {row['filename']}, Role: {row['role_id']}")
        # check if analysis_json has role_id
        data = json.loads(row['analysis_json'])
        print(f"  JSON RoleID: {data.get('role_id')}")
    conn.close()

if __name__ == "__main__":
    debug()
