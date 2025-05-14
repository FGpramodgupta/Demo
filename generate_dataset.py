import re

def generate_ner_data(text, assets, clients):
    train_data = []
    entities = []

    # Search for exact matches using regex word boundaries
    for name in assets:
        for match in re.finditer(r'\b' + re.escape(name) + r'\b', text, flags=re.IGNORECASE):
            start, end = match.span()
            entities.append((start, end, "ASSET"))

    for name in clients:
        for match in re.finditer(r'\b' + re.escape(name) + r'\b', text, flags=re.IGNORECASE):
            start, end = match.span()
            entities.append((start, end, "CLIENT"))

    # Remove overlaps
    entities = sorted(entities, key=lambda x: x[0])
    clean_entities = []
    last_end = -1
    for start, end, label in entities:
        if start >= last_end:  # Avoid overlapping entities
            clean_entities.append((start, end, label))
            last_end = end

    train_data.append((text, {"entities": clean_entities}))
    return train_data
