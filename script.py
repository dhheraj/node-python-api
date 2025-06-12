# import os
# import sys
# import cv2
# from PIL import Image
# import pytesseract
# import json

# try:
#     image_path = sys.argv[1]

#     if not os.path.exists(image_path):
#         raise FileNotFoundError(f"Image file not found: {image_path}")

#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"cv2.imread() failed. Could not read image at {image_path}")

#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#     temp_path = "temp_processed.png"
#     cv2.imwrite(temp_path, thresh)

#     processed_image = Image.open(temp_path)
#     text = pytesseract.image_to_string(processed_image)

#     print(json.dumps({"text": text}))
#     os.remove(temp_path)

# except Exception as e:
#     print(json.dumps({"error": str(e)}))


import os
import sys
import cv2
from PIL import Image
import pytesseract
import json
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"cv2.imread() failed. Could not read image at {image_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Denoising
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    
    # Adaptive thresholding (more effective for varying lighting)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 31, 10
    )
    
    return thresh

def extract_text(image_path):
    preprocessed = preprocess_image(image_path)

    temp_path = "temp_processed.png"
    cv2.imwrite(temp_path, preprocessed)

    try:
        image_pil = Image.open(temp_path)
        # Customize Tesseract config for better accuracy
        config = r'--oem 3 --psm 6'  # LSTM OCR Engine, assume a single block of text
        text = pytesseract.image_to_string(image_pil, config=config)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("Usage: python script.py <image_path>")
        
        image_path = sys.argv[1]
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        extracted_text = extract_text(image_path)
        print(json.dumps({"text": extracted_text}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

