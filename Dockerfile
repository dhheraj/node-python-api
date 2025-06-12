# Use Node base image with Debian
FROM node:18-bullseye

# Install Python and system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip tesseract-ocr libsm6 libxext6 libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Create and activate Python virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy Python dependencies first and install them inside venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Node dependencies and install them
COPY package*.json ./
RUN npm install

# Copy rest of the app
COPY . .

# Expose port
EXPOSE 3000

# Start the Node server
CMD ["node", "index.js"]
