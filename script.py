import os
import sys
import cv2
from PIL import Image
import pytesseract
import json

try:
    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"cv2.imread() failed. Could not read image at {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    temp_path = "temp_processed.png"
    cv2.imwrite(temp_path, thresh)

    processed_image = Image.open(temp_path)
    text = pytesseract.image_to_string(processed_image)

    print(json.dumps({"text": text}))
    os.remove(temp_path)

except Exception as e:
    print(json.dumps({"error": str(e)}))
