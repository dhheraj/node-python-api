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

# Install Python and dependencies for OpenCV and Tesseract
RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip python3-venv tesseract-ocr \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy package files and install Node dependencies
COPY package*.json ./
RUN npm install

# Copy Python requirements and install Python dependencies
COPY requirements.txt .
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Ensure the upload folder exists
RUN mkdir -p uploads

EXPOSE 3000

CMD ["node", "index.js"]
