# Use a complete base image
FROM node:18-bullseye

# Install required OS packages
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip tesseract-ocr libsm6 libxext6 libxrender-dev

# Create app directory
WORKDIR /app

# Create and activate a virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy Python and Node dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY package*.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 3000

# Start the Node server
CMD ["node", "index.js"]
