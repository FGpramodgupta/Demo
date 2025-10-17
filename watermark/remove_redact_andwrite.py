import fitz  # PyMuPDF

input_pdf = "input.pdf"
output_pdf = "output_cleaned.pdf"

watermark_texts = [
    "CONFIDENTIAL",
    "FOR INTERNAL USE ONLY",
    "DO NOT SHARE"
]

def normalize_color(color_value):
    """Convert PyMuPDF color int or list into (r,g,b) tuple between 0–1."""
    if isinstance(color_value, (list, tuple)) and len(color_value) == 3:
        return tuple(float(c) / 255.0 if c > 1 else float(c) for c in color_value)
    elif isinstance(color_value, int):
        r = (color_value >> 16) & 255
        g = (color_value >> 8) & 255
        b = color_value & 255
        return (r / 255.0, g / 255.0, b / 255.0)
    return (0, 0, 0)

doc = fitz.open(input_pdf)

for page in doc:
    # 1️⃣ Find watermark bounding boxes
    wm_boxes = []
    for wm in watermark_texts:
        wm_boxes.extend(page.search_for(wm))

    if not wm_boxes:
        continue

    # 2️⃣ Extract all text spans before redaction
    textpage = page.get_textpage()
    blocks = textpage.extractDICT()["blocks"]

    overlapping_spans = []
    for block in blocks:
        for line in block["lines"]:
            for span in line["spans"]:
                bbox = fitz.Rect(span["bbox"])
                for wm_rect in wm_boxes:
                    if bbox.intersects(wm_rect):
                        overlapping_spans.append(span)
                        break

    # 3️⃣ Redact (erase watermark)
    for rect in wm_boxes:
        page.add_redact_annot(rect, fill=(1, 1, 1))  # white fill
    page.apply_redactions()

    # 4️⃣ Restore overlapping text
    for span in overlapping_spans:
        color = normalize_color(span.get("color", (0, 0, 0)))
        page.insert_text(
            (span["bbox"][0], span["bbox"][1]),
            span["text"],
            fontsize=span.get("size", 12),
            fontname="helv",  # safe built-in font
            color=color,
        )

doc.save(output_pdf)
doc.close()

print("✅ Watermarks redacted & overlapping text restored successfully!")
