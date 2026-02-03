FROM python:3.10-slim

WORKDIR /app

# System deps (safe for headless OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libxrender1 \
    libxext6 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install everything (let pip resolve deps)
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# 🔥 HARD FIX: remove conflicting OpenCV wheels
RUN pip uninstall -y opencv-python opencv-contrib-python || true

# ✅ Reinstall headless OpenCV ONLY
RUN pip install --no-cache-dir opencv-python-headless==4.7.0.72

# Copy app
COPY . .

# Sanity check
RUN python - <<EOF
import cv2
print("OpenCV version:", cv2.__version__)
EOF

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
