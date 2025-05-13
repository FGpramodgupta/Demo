To build a **generic Named Entity Recognition (NER)** model using **spaCy** that extracts **Assets** and **Client names** from a PDF document, you can follow this step-by-step approach:

---

### ✅ Step 1: Extract Text from PDF

First, extract the text from the PDF using tools like `PyMuPDF`, `pdfminer`, or `PyPDF2`. Here’s an example using `PyMuPDF` (`fitz`):

```python
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text
```

---

### ✅ Step 2: Prepare Training Data

You'll need to **annotate** a few samples with `ASSET` and `CLIENT` entities manually.

**Example of annotated data format:**

```python
TRAIN_DATA = [
    ("The client John Smith invested in Apple Inc shares.", {"entities": [(11, 21, "CLIENT"), (35, 44, "ASSET")]}),
    ("Tesla stock was acquired by Alice Johnson.", {"entities": [(0, 11, "ASSET"), (31, 44, "CLIENT")]}),
]
```

Start with 10–20 samples, then add more iteratively.

---

### ✅ Step 3: Train Custom NER Model in spaCy

```python
import spacy
from spacy.training.example import Example

def train_custom_ner(train_data, iterations=30):
    nlp = spacy.blank("en")  # Create a blank English model
    ner = nlp.add_pipe("ner")

    # Add labels
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Training
    optimizer = nlp.begin_training()
    for i in range(iterations):
        for text, annotations in train_data:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.2, sgd=optimizer)

    return nlp
```

---

### ✅ Step 4: Use Trained Model for Inference

```python
def extract_entities(text, model):
    doc = model(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
```

---

### ✅ Step 5: Put It All Together

```python
# 1. Load PDF
text = extract_text_from_pdf("your_file.pdf")

# 2. Train Model
nlp_model = train_custom_ner(TRAIN_DATA)

# 3. Predict
entities = extract_entities(text, nlp_model)
print(entities)
```

---

### ✅ Tips for Making it Generic:

* Train on a **diverse set** of example documents: different layouts, vocabularies, asset types, and client name styles.
* Use **regular expressions** + rule-based matching (spaCy's `Matcher`) to bootstrap entity annotations.
* Optionally, **fine-tune a pre-trained spaCy model** (e.g., `en_core_web_trf`) instead of using a blank model for better performance.

---

Would you like help in creating a Jupyter notebook or script with bootstrapped sample data and training code?
