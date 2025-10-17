import fitz  # PyMuPDF

input_pdf = "input.pdf"
output_pdf = "output_no_watermark.pdf"

watermark_texts = [
    "CONFIDENTIAL",
    "FOR INTERNAL USE ONLY",
    "DO NOT SHARE"
]

doc = fitz.open(input_pdf)

for page in doc:
    # Extract page text blocks
    blocks = page.get_text("blocks")
    
    # Rebuild the page without watermark blocks
    new_page = fitz.open()  # temporary doc
    temp = new_page.new_page(width=page.rect.width, height=page.rect.height)
    
    for b in blocks:
        text = b[4].strip()
        if not any(w.lower() in text.lower() for w in watermark_texts):
            temp.insert_text((b[0], b[1]), text, fontsize=12)
    
    # Replace original page with cleaned one
    page.clean_contents()  # clear existing content
    page.show_pdf_page(page.rect, new_page, 0)

doc.save(output_pdf)
doc.close()

print("✅ Watermarks removed without deleting other text.")
