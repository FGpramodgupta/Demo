import cv2
import numpy as np

def aggressively_remove_watermark(cropped_img_path, original_img_path, top_left_coord, band_height=10):
    # Load images
    cropped = cv2.imread(cropped_img_path)
    original = cv2.imread(original_img_path)
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Step 1: Adaptive threshold (detect light text on varied background)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, blockSize=15, C=10)

    # Step 2: Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    clean_mask = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    # Step 3: Find lowest Y (bottom-most watermark region)
    coords = np.column_stack(np.where(clean_mask > 0))
    if coords.shape[0] == 0:
        print("Watermark not detected.")
        return original

    max_y = np.max(coords[:, 0])
    min_y = max(max_y - band_height, 0)

    # Step 4: Create inpainting mask
    mask = np.zeros_like(gray)
    mask[min_y:max_y + 1, :] = clean_mask[min_y:max_y + 1, :]

    # Step 5: Inpaint watermark area
    inpainted = cv2.inpaint(cropped, mask, 3, cv2.INPAINT_TELEA)

    # Step 6: Replace back in original image
    x, y = top_left_coord
    h, w = cropped.shape[:2]
    original[y:y + h, x:x + w] = inpainted

    return original






------------------------------------------------------------------------

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
