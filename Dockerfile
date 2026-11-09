# ==========================================
# STAGE 1: BUILDER (Dùng image đầy đủ để cài cắm)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Copy requirements và cài đặt vào một thư mục tạm
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# STAGE 2: RUNNER (Dùng Alpine siêu nhẹ để chạy thực tế)
# ==========================================
FROM python:3.12-alpine

WORKDIR /app

# Chỉ copy những thư viện đã được build sẵn từ STAGE 1 sang STAGE 2
COPY --from=builder /install /usr/local

# Copy mã nguồn Python của bạn vào
COPY . .

# Khởi chạy bot
ENTRYPOINT ["python", "main.py"]