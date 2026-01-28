# Sử dụng image đã cài sẵn Chrome và thư viện cần thiết
FROM ghcr.io/puppeteer/puppeteer:latest

USER root

# Cài đặt các công cụ điều khiển màn hình ảo còn thiếu
# Sử dụng mirror khác nếu mặc định bị lỗi 100
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    wmctrl \
    procps \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cài đặt noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Cài đặt psutil cho Python
RUN pip install psutil

WORKDIR /app
COPY main.py .

# Render yêu cầu dùng PORT từ biến môi trường hoặc mặc định 10000/80
EXPOSE 80

CMD ["python3", "main.py"]
