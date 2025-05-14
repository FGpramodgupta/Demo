import spacy
from spacy.pipeline import EntityRuler
import random

# Step 1: Prepare entity lists
clients = ["John Smith", "Alice Johnson", "Emma Davis"]
assets = ["Apple Inc.", "Microsoft Corp", "Tesla"]

# Step 2: Create a blank English pipeline and add EntityRuler before NER
nlp = spacy.blank("en")
ruler = nlp.add_pipe("entity_ruler", name="entity_ruler", before="ner")

# Step 3: Add patterns to the EntityRuler
patterns = [{"label": "CLIENT", "pattern": name} for name in clients] + \
           [{"label": "ASSET", "pattern": name} for name in assets]
ruler.add_patterns(patterns)

# Step 4: Add NER to pipeline
ner = nlp.add_pipe("ner", name="ner", last=True)
ner.add_label("CLIENT")
ner.add_label("ASSET")

# Step 5: Generate synthetic training data
TRAIN_DATA = []
for _ in range(200):
    client = random.choice(clients)
    asset = random.choice(assets)
    sentence = f"{client} recently sold his shares of {asset} due to market fluctuations."
    start_client = sentence.find(client)
    end_client = start_client + len(client)
    start_asset = sentence.find(asset)
    end_asset = start_asset + len(asset)
    TRAIN_DATA.append((sentence, {"entities": [(start_client, end_client, "CLIENT"),
                                               (start_asset, end_asset, "ASSET")]}))

# Step 6: Train the NER model
optimizer = nlp.begin_training()
for i in range(10):  # 10 epochs
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = spacy.util.minibatch(TRAIN_DATA, size=8)
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(texts, annotations, drop=0.3, losses=losses)
    print(f"Epoch {i+1} - Losses: {losses}")

# Step 7: Save the combined model
nlp.to_disk("combined_ner_model")

# Step 8: Test the model
nlp2 = spacy.load("combined_ner_model")
doc = nlp2("Emma Davis recently acquired Microsoft Corp.")
for ent in doc.ents:
    print(ent.text, ent.label_)
