import traceback
import sys

try:
    print("Pre-importing main...")
    import main
    print("Main imported successfully!")
    
    if __name__ == "__main__":
        print("Executing uvicorn run...")
        import uvicorn
        # Check port 8005
        uvicorn.run(main.app_root, host="0.0.0.0", port=8005)
except Exception as e:
    print("\n" + "!"*50)
    print("CRITICAL STARTUP ERROR DETECTED")
    print("!"*50)
    traceback.print_exc()
    print("!"*50 + "\n")
    sys.exit(1)
