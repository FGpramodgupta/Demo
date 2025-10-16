import fitz  # PyMuPDF

input_pdf = "input.pdf"
output_pdf = "output_no_watermark.pdf"

# Open the PDF
doc = fitz.open(input_pdf)

for page in doc:
    # 1️⃣ Remove text-based watermarks
    text_instances = page.search_for("CONFIDENTIAL")  # change this to your watermark text
    for inst in text_instances:
        page.add_redact_annot(inst)
    page.apply_redactions()

    # 2️⃣ Remove annotation-based watermarks (often appear as image or text boxes)
    for annot in page.annots() or []:
        subtype = annot.type[0]
        if subtype in ["FreeText", "Stamp", "Watermark", "Text", "Square"]:
            page.delete_annot(annot)

    # 3️⃣ Optionally, remove images that look like watermarks (if layered)
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        try:
            page._delete_image(xref)
        except Exception:
            pass  # Skip if not removable

# Save cleaned file
doc.save(output_pdf)
doc.close()

print("✅ Watermark removed and saved as:", output_pdf)
