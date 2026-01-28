# Sử dụng Python 3.9 nền Debian để ổn định
FROM python:3.9-slim-buster

# Cài đặt các thư viện hệ thống cần thiết cho Chrome và Đồ họa ảo
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    x11vnc \
    fluxbox \
    wmctrl \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libnss3 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Google Chrome Stable
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Cài đặt noVNC để xem trên trình duyệt web
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC \
    && git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify \
    && ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Cài đặt thư viện Python
RUN pip install psutil

# Sao chép code chính vào container
COPY main.py /app/main.py
WORKDIR /app

# Mở cổng 80 (Render yêu cầu dịch vụ web lắng nghe cổng này)
EXPOSE 80

# Chạy lệnh khởi động
CMD ["python", "main.py"]
