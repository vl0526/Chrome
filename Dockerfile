# Sử dụng Python 3.9 nền Debian Buster
FROM python:3.9-slim-buster

# Thiết lập môi trường không tương tác để tránh treo khi cài đặt
ENV DEBIAN_FRONTEND=noninteractive

# Cập nhật và cài đặt các thư viện hệ thống với cơ chế tự động thử lại nếu lỗi mạng
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    unzip \
    git \
    xvfb \
    x11vnc \
    fluxbox \
    wmctrl \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    libnss3 \
    xdg-utils \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Google Chrome Stable (Sử dụng link trực tiếp từ Google)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update -y && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || apt-get install -f -y && \
    rm google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# Cài đặt noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Cài đặt thư viện Python cần thiết
RUN pip install --no-cache-dir psutil

# Sao chép mã nguồn
COPY main.py /app/main.py
WORKDIR /app

# Render mặc định dùng cổng 10000 hoặc 80, file main.py của chúng ta dùng 80
EXPOSE 80

# Chạy bằng python
CMD ["python", "main.py"]
