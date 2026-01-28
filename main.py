import os
import subprocess
import time
import psutil

CONFIG = {
    "PASS": "123456",
    "RES": "1024x768x16",
    "DISPLAY": ":1",
    "CHROME_URL": "https://www.google.com",
    "PORT": "80"
}

os.environ["DISPLAY"] = CONFIG["DISPLAY"]
os.environ["HOME"] = "/tmp"

def run_silent(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def setup_environment():
    print("--- Khởi động Display Server ---")
    run_silent(f"Xvfb {CONFIG['DISPLAY']} -screen 0 {CONFIG['RES']} -ac +extension GLX +extension RANDR")
    time.sleep(2)
    run_silent("fluxbox")
    
    print("--- Cấu hình VNC ---")
    os.makedirs("/tmp/.vnc", exist_ok=True)
    subprocess.run(f"x11vnc -storepasswd '{CONFIG['PASS']}' /tmp/.vnc/passwd", shell=True)
    run_silent(f"x11vnc -display {CONFIG['DISPLAY']} -rfbport 5901 -rfbauth /tmp/.vnc/passwd -forever -shared -bg")
    
    print(f"--- Khởi động Web Proxy trên cổng {CONFIG['PORT']} ---")
    run_silent(f"/opt/noVNC/utils/novnc_proxy --vnc localhost:5901 --listen {CONFIG['PORT']}")

def manage_chrome():
    # Tìm đường dẫn Chrome đã cài sẵn trong image puppeteer
    chrome_path = "/usr/bin/google-chrome"
    
    while True:
        chrome_running = any('chrome' in proc.name() for proc in psutil.process_iter(['name']))
        
        if not chrome_running:
            print("--- Đang khởi động Chrome có sẵn trong hệ thống ---")
            flags = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--user-data-dir=/tmp/chrome_profile",
                "--disable-gpu",
                "--js-flags='--max-old-space-size=300'"
            ]
            cmd = f"{chrome_path} {' '.join(flags)} '{CONFIG['CHROME_URL']}'"
            run_silent(cmd)
            time.sleep(5)
            subprocess.run("wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz", shell=True)
        
        time.sleep(10)

if __name__ == "__main__":
    setup_environment()
    manage_chrome()
