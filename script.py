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


# # import os
# # import sys
# # import cv2
# # from PIL import Image
# # import pytesseract
# # import json

# # try:
# #     image_path = sys.argv[1]

# #     if not os.path.exists(image_path):
# #         raise FileNotFoundError(f"Image file not found: {image_path}")

# #     image = cv2.imread(image_path)
# #     if image is None:
# #         raise ValueError(f"cv2.imread() failed. Could not read image at {image_path}")

# #     # Convert to grayscale
# #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# #     # Apply denoising
# #     denoised = cv2.fastNlMeansDenoising(gray, h=30)

# #     # Use adaptive thresholding for better lighting normalization
# #     thresh = cv2.adaptiveThreshold(
# #         denoised, 255,
# #         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
# #         cv2.THRESH_BINARY,
# #         31, 10
# #     )

# #     temp_path = "temp_processed.png"
# #     cv2.imwrite(temp_path, thresh)

# #     processed_image = Image.open(temp_path)

# #     # Tesseract config: LSTM OCR engine, assume block of text
# #     config = r'--oem 3 --psm 6'
# #     text = pytesseract.image_to_string(processed_image, config=config)

# #     print(json.dumps({"text": text}))
# #     os.remove(temp_path)

# # except Exception as e:
# #     print(json.dumps({"error": str(e)}))




import cv2
import easyocr
import os
import ssl
import json
import sys
import warnings
import logging

# Suppress warnings and logs
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["USE_TF"] = "0"
logging.getLogger("easyocr").setLevel(logging.CRITICAL)
ssl._create_default_https_context = ssl._create_unverified_context

def safe_print(*args, **kwargs):
    print(*args, **kwargs)

def preprocess_image(path):
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {path}")

    scale_percent = 200
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    return gray

def extract_text_easyocr(image_path, lang_list=['en']):
    image = preprocess_image(image_path)
    temp_path = "temp_gray_image.png"
    cv2.imwrite(temp_path, image)

    reader = easyocr.Reader(lang_list, gpu=False)
    results = reader.readtext(temp_path)

    os.remove(temp_path)

    extracted_text = ""
    for (_, text, confidence) in results:
        if confidence > 0.4:
            extracted_text += text + "\n"

    return extracted_text.strip()

# === Main Execution ===
try:
    if len(sys.argv) < 2:
        raise ValueError("Image path not provided")

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    final_text = extract_text_easyocr(image_path)
    safe_print(json.dumps({"text": final_text}, ensure_ascii=False))

except Exception as e:
    safe_print(json.dumps({"error": str(e)}))
