# FROM node:18-bullseye

# # Install Python, Tesseract, OpenCV dependencies (including libGL)
# RUN apt-get update && \
#     apt-get install -y python3 python3-venv python3-pip tesseract-ocr \
#     libsm6 libxext6 libxrender-dev libgl1 && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Python virtual environment
# RUN python3 -m venv /app/venv
# ENV PATH="/app/venv/bin:$PATH"

# # Python deps
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Node deps
# COPY package*.json ./
# RUN npm install

# # Copy rest of the files
# COPY . .

# EXPOSE 3000

# CMD ["node", "index.js"]
FROM node:18-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 python3-venv python3-pip \
    tesseract-ocr \
    libsm6 libxext6 libxrender-dev libgl1 \
    ffmpeg libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set up Python virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy application source
COPY . .

# Expose port for Node.js
EXPOSE 3000

# Default command (can be adjusted to your needs)
CMD ["node", "index.js"]
