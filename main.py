import os
import subprocess
import time
import shutil
import psutil

# Cấu hình tối ưu cho Render (RAM thấp)
CONFIG = {
    "PASS": "123456",
    "RES": "1024x600x16", # Giảm độ phân giải để tiết kiệm RAM
    "DISPLAY": ":1",
    "CHROME_URL": "https://www.google.com",
    "PORT": "80" # Render sử dụng cổng 80 hoặc 10000
}

os.environ["DISPLAY"] = CONFIG["DISPLAY"]
os.environ["HOME"] = "/tmp" # Tránh lỗi ghi quyền root trên Render

def run_silent(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def setup_environment():
    print("--- Đang khởi tạo môi trường đồ họa ảo ---")
    # 1. Khởi chạy Xvfb (Màn hình ảo)
    run_silent(f"Xvfb {CONFIG['DISPLAY']} -screen 0 {CONFIG['RES']} -ac +extension GLX +extension RANDR")
    time.sleep(2)
    
    # 2. Khởi chạy Window Manager (Fluxbox)
    run_silent("fluxbox")
    
    # 3. Khởi chạy VNC Server
    os.makedirs("/tmp/.vnc", exist_ok=True)
    subprocess.run(f"x11vnc -storepasswd '{CONFIG['PASS']}' /tmp/.vnc/passwd", shell=True)
    run_silent(f"x11vnc -display {CONFIG['DISPLAY']} -rfbport 5901 -rfbauth /tmp/.vnc/passwd -forever -shared -bg -threads")
    
    # 4. Khởi chạy noVNC (Proxy từ VNC sang Web)
    run_silent(f"/opt/noVNC/utils/novnc_proxy --vnc localhost:5901 --listen {CONFIG['PORT']}")
    print(f"--- Hệ thống đã sẵn sàng trên cổng {CONFIG['PORT']} ---")

def manage_chrome():
    """Đảm bảo Chrome luôn chạy và tối ưu RAM"""
    while True:
        chrome_running = any('chrome' in proc.name() for proc in psutil.process_iter(['name']))
        
        if not chrome_running:
            print("--- Đang khởi động lại Chrome ---")
            flags = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--user-data-dir=/tmp/chrome_profile",
                "--disable-gpu",
                "--no-first-run",
                "--js-flags='--max-old-space-size=300'", # Cực kỳ quan trọng cho Render Free
                "--disable-software-rasterizer"
            ]
            cmd = f"google-chrome {' '.join(flags)} '{CONFIG['CHROME_URL']}'"
            run_silent(cmd)
            time.sleep(5)
            # Tự động phóng to cửa sổ
            subprocess.run("wmctrl -r :ACTIVE: -b add,maximized_vert,maximized_horz", shell=True)
        
        time.sleep(10)

if __name__ == "__main__":
    setup_environment()
    manage_chrome()
