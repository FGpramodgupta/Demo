import cv2
import numpy as np

def remove_lowest_watermark_and_replace(original_img_path, cropped_img_path, top_left_coord, threshold=200):
    # Load original and cropped image
    original = cv2.imread(original_img_path)
    cropped = cv2.imread(cropped_img_path)
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Step 1: Threshold to detect watermark
    _, binary_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Step 2: Find watermark pixels
    coords = np.column_stack(np.where(binary_mask > 0))  # [y, x]

    if coords.shape[0] == 0:
        print("No watermark pixels found.")
        return original

    # Step 3: Find the lowest (bottom-most) row value
    max_y = np.max(coords[:, 0])

    # Step 4: Create a mask of only the lowest watermark pixels
    lowest_mask = np.zeros_like(gray)
    for y, x in coords:
        if y == max_y:
            lowest_mask[y, x] = 255

    # Optional: dilate to cover a slightly bigger region
    kernel = np.ones((3, 3), np.uint8)
    lowest_mask = cv2.dilate(lowest_mask, kernel, iterations=1)

    # Step 5: Inpaint (remove) watermark pixels
    inpainted = cv2.inpaint(cropped, lowest_mask, 3, cv2.INPAINT_TELEA)

    # Step 6: Replace the cleaned cropped image into the original image
    x, y = top_left_coord
    h, w = cropped.shape[:2]
    original[y:y+h, x:x+w] = inpainted

    return original

cleaned = remove_lowest_watermark_and_replace(
    original_img_path="original_image.png",
    cropped_img_path="cropped_watermark_region.png",
    top_left_coord=(100, 500),  # X and Y where cropped region starts in original image
    threshold=200
)

cv2.imwrite("final_cleaned_image.png", cleaned)
