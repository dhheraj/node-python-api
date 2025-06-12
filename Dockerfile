# Use full Debian image instead of slim
FROM node:18-bullseye

# Install Python, pip, and Tesseract
RUN apt-get update && \
    apt-get install -y python3 python3-pip tesseract-ocr libsm6 libxext6 libxrender-dev && \
    pip3 install --upgrade pip

# Set working directory
WORKDIR /app

# Copy dependencies
COPY package*.json ./
RUN npm install

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 3000

# Run server
CMD ["node", "index.js"]
