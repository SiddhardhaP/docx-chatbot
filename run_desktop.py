import threading
import webview
import time
import socket
import os
import subprocess

def is_port_in_use(port: int) -> bool:
    """Checks if a port is in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_streamlit():
    """Runs the Streamlit app using subprocess."""
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    command = [
        "streamlit",
        "run",
        app_path,
        "--server.port", "8501",
        "--server.headless", "true", # Prevents Streamlit from opening a browser
        "--server.enableCORS", "false" # Can be important for webview
    ]
    # The subprocess will run in the background
    # and be terminated when the main pywebview thread is closed.
    subprocess.run(command)

def start_desktop_app():
    """Starts the Streamlit server and the pywebview window."""
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()

    # Wait for the Streamlit server to start
    max_wait_time = 60  # seconds
    start_time = time.time()
    while not is_port_in_use(8501):
        time.sleep(0.5)
        if time.time() - start_time > max_wait_time:
            raise TimeoutError("Streamlit server did not start in time.")

    webview.create_window('OpenAI RAG Chatbot', 'http://localhost:8501')
    webview.start()

if __name__ == '__main__':
    start_desktop_app()