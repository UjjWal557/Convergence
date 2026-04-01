import sys
print("Testing imports...")
try:
    import fastapi
    import uvicorn
    import mysql.connector
    import google.generativeai
    print("Imports successful!")
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

print("\nTesting database connection...")
import database
try:
    conn = database.get_connection()
    if conn:
        print("Database connection successful!")
        conn.close()
    else:
        print("Database connection failed (get_connection returned None).")
except Exception as e:
    print(f"Database error: {e}")

print("\nRunning init_db...")
try:
    database.init_db()
    print("init_db completed!")
except Exception as e:
    print(f"init_db error: {e}")
