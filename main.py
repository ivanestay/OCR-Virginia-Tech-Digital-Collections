import pytesseract
import cv2 as cv
import json
import os
import glob
import spacy
import re

# Tesseract executable path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ivanestay\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Output directory
output_folder = "C:/Users/ivanestay/PycharmProjects/OCR-Virginia-Tech-Digital-Collections/BARTER_COLLECTION/output/"
os.makedirs(output_folder, exist_ok=True)

# Load English NLP model, use py -m spacy download en_core_web_sm in cmd
nlp = spacy.load("en_core_web_sm")

def process_image(image_path, threshvalue, ksize):
    """Preprocess the image (convert to grayscale, apply median blur, thresholding)."""
    grayscale_img = cv.imread(image_path, 0)
    blurred_grayscale_img = cv.medianBlur(grayscale_img, ksize)
    ret, thresholded_img = cv.threshold(blurred_grayscale_img, threshvalue, 255, cv.THRESH_BINARY)
    return thresholded_img

def perform_ocr(thresholded_image):
    """Run OCR on the preprocessed image."""
    return pytesseract.image_to_string(thresholded_image)

def normalize_text(text):
    """Lowercase everything and convert to title case."""
    return text.lower().title()

def extract_names(text):
    """Extracts names using spaCy's Named Entity Recognition (NER)."""
    doc = nlp(normalize_text(text))
    """Normalization is necessary, as some names may not be recognized otherwise. """
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    """List of names to exclude"""
    #exclude_names = {""}

    """Filter out the excluded names"""
    #filtered_names = [name for name in names if not any(excl in name.lower() for excl in exclude_names)]

    return(names)

def save_json(output_folder, file_name, text):
    """Save OCR results to a JSON file."""
    data = {"image": file_name, "output": text}
    with open(os.path.join(output_folder, file_name), 'w') as f:
        json.dump(data, f, indent=4)

def process_images(path, threshvalue=127, ksize=3):
    """Process a list of images. Inputs include the filepath as well as the thresh value, set to 127 by default."""
    for img in path:
        try:
            file_name = os.path.basename(img)
            file_name_no_extension = os.path.splitext(file_name)[0]
            thresholded_image = process_image(img, threshvalue, ksize)
            text = perform_ocr(thresholded_image)
            detected_names = extract_names(text)
            print(detected_names)
            save_json(output_folder, f"{file_name_no_extension}.json", text)
        except Exception as e:
            print(f"Error processing {img}: {e}")

# Process regular images
regular_images = glob.glob("C:/Users/ivanestay/PycharmProjects/OCR-Virginia-Tech-Digital-Collections/BARTER_COLLECTION/regular/*.jpg")
process_images(regular_images)

# Process handwriting images
handwriting_images = glob.glob("C:/Users/ivanestay/PycharmProjects/OCR-Virginia-Tech-Digital-Collections/BARTER_COLLECTION/handwriting/*.jpg")
process_images(handwriting_images,100)

print("OCR processing complete.")