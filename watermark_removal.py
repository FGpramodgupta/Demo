import fitz  # PyMuPDF
import cv2
import numpy as np
import os

def remove_watermark_from_image(img):
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define mask to capture light gray watermark (tune as needed)
    lower = np.array([0, 0, 160])
    upper = np.array([180, 50, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Inpaint to remove watermark
    result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    return result

def pdf_watermark_removal(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    temp_images = []

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)  # High-res for quality
        img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:
            img_data = cv2.cvtColor(img_data, cv2.COLOR_RGBA2BGR)

        cleaned_img = remove_watermark_from_image(img_data)

        temp_path = f"page_{i}.png"
        cv2.imwrite(temp_path, cleaned_img)
        temp_images.append(temp_path)

    # Convert images back to PDF
    doc_out = fitz.open()
    for img_path in temp_images:
        img_pdf = fitz.open(img_path)
        rect = img_pdf[0].rect
        page = doc_out.new_page(width=rect.width, height=rect.height)
        page.insert_image(rect, filename=img_path)
        os.remove(img_path)

    doc_out.save(output_pdf)
    print(f"✅ Output saved to: {output_pdf}")

# Example usage
pdf_watermark_removal("input.pdf", "output_no_watermark.pdf")
