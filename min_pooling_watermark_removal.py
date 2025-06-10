import cv2
import numpy as np
from pdf2image import convert_from_path
import os

# Step 1: Convert PDF to images
def convert_pdf_to_images(pdf_path):
    pages = convert_from_path(pdf_path, dpi=200)
    image_list = []
    for i, page in enumerate(pages):
        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        image_list.append(img)
    return image_list

# Step 2: Apply min-pooling to detect watermark
def min_pooling(images):
    return np.min(np.stack(images), axis=0).astype(np.uint8)

# Step 3: Detect watermark mask
def detect_watermark_mask(images, pooled_image, threshold=30):
    masks = []
    for img in images:
        diff = cv2.absdiff(img, pooled_image)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)
        masks.append(mask)
    return masks

# Step 4: Inpaint each image using the detected mask
def remove_watermark(images, masks):
    inpainted_images = []
    for img, mask in zip(images, masks):
        inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        inpainted_images.append(inpainted)
    return inpainted_images

# Save images to disk
def save_images(images, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for i, img in enumerate(images):
        cv2.imwrite(os.path.join(output_folder, f"page_{i+1}_cleaned.jpg"), img)

# ========== MAIN ==========
pdf_path = "your_pdf_with_watermark.pdf"
images = convert_pdf_to_images(pdf_path)
pooled = min_pooling(images)
masks = detect_watermark_mask(images, pooled, threshold=30)
cleaned_images = remove_watermark(images, masks)
save_images(cleaned_images, "output_pages")
