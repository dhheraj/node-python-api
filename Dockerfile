# Base image with both Node and Python
FROM node:18-slim

# Install Python, pip, tesseract, and OpenCV dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip tesseract-ocr libsm6 libxext6 libxrender-dev && \
    pip3 install --upgrade pip

# Create app directory
WORKDIR /app

# Copy files
COPY package*.json ./
RUN npm install

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

# Expose port
EXPOSE 3000

# Run server
CMD ["node", "index.js"]
