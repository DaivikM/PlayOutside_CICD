import multiprocessing
import uvicorn
import sys

def run_api():
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)

def run_streamlit():
    import subprocess
    process = subprocess.Popen(["streamlit", "run", "ui.py"])
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()

def main():
    api_process = multiprocessing.Process(target=run_api)
    ui_process = multiprocessing.Process(target=run_streamlit)

    api_process.start()
    ui_process.start()

    try:
        api_process.join()
        ui_process.join()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        api_process.terminate()
        ui_process.terminate()
        api_process.join()
        ui_process.join()
        print("All processes stopped. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
