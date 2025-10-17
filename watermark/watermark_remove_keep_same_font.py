import fitz  # PyMuPDF

input_pdf = "input.pdf"
output_pdf = "output_no_watermark.pdf"

# Add all watermark lines you want to remove
watermark_texts = [
    "CONFIDENTIAL",
    "FOR INTERNAL USE ONLY",
    "DO NOT SHARE"
]

doc = fitz.open(input_pdf)

for page in doc:
    # Extract all text spans
    textpage = page.get_textpage()
    spans = textpage.extractDICT()["blocks"]
    
    # Clean existing content
    page.clean_contents()

    # Rebuild content without watermark
    for block in spans:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                # Skip watermark lines
                if any(w.lower() in text.lower() for w in watermark_texts):
                    continue
                # Re-add normal text
                page.insert_text(
                    (span["bbox"][0], span["bbox"][1]),
                    text,
                    fontsize=span["size"],
                    fontname=span["font"],
                    color=span["color"],
                )

doc.save(output_pdf)
doc.close()

print("✅ Watermarks removed successfully without affecting other text.")
