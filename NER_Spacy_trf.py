Great! Here's a **Jupyter Notebook** that walks you through fine-tuning a **large spaCy pre-trained model (`en_core_web_trf`)** for custom NER tasks like **`ASSET`** and **`CLIENT`** entity recognition.

---

## ✅ Jupyter Notebook: Fine-tuning spaCy Transformer NER

```python
# 1. Install required packages
!pip install -U spacy transformers

# Download the large transformer-based English model
!python -m spacy download en_core_web_trf
```

---

```python
# 2. Import packages and initialize
import spacy
from spacy.tokens import DocBin
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import random
```

---

```python
# 3. Sample training data
# Replace with your annotated data
TRAIN_DATA = [
    ("John Smith invested in Apple Inc.", {"entities": [(0, 10, "CLIENT"), (24, 34, "ASSET")]}),
    ("The client Mary Johnson bought Tesla shares.", {"entities": [(11, 23, "CLIENT"), (31, 43, "ASSET")]}),
    ("Goldman Sachs handled the investment for Mark Doe.", {"entities": [(0, 13, "ASSET"), (42, 50, "CLIENT")]}),
]
```

---

```python
# 4. Load the transformer-based spaCy model
nlp = spacy.load("en_core_web_trf")
ner = nlp.get_pipe("ner")

# Add new entity labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])
```

---

```python
# 5. Disable other pipes and start training
import warnings
warnings.filterwarnings("ignore", message=r"\[W007\]")

from spacy.training import Example

# Convert data to spaCy Example objects
examples = []
for text, ann in TRAIN_DATA:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, ann)
    examples.append(example)

# Train
optimizer = nlp.resume_training()
for i in range(10):  # 10 epochs
    random.shuffle(examples)
    losses = {}
    batches = minibatch(examples, size=2)
    for batch in batches:
        nlp.update(batch, drop=0.3, losses=losses)
    print(f"Iteration {i+1} - Losses: {losses}")
```

---

```python
# 6. Save the trained model
nlp.to_disk("ner_asset_client_model")
```

---

```python
# 7. Load and test the model
nlp2 = spacy.load("ner_asset_client_model")
doc = nlp2("Jane Doe has invested heavily in Microsoft stocks.")
for ent in doc.ents:
    print(ent.text, ent.label_)
```

---

## ✅ Tips for Real-World Use:

* **Use more examples (\~100+) for better generalization**
* **Add noisy/realistic PDF-extracted examples**
* Combine this with **rule-based matchers** for fallback coverage
* Use tools like **Doccano** or **Label Studio** to prepare annotations

---

Would you like:

* A ready-to-run Colab version?
* Or I can generate a larger synthetic training dataset to start with?
