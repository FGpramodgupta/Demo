import json

label_studio_data = []

sample_data = [
    {
        "keyword": "example",
        "filename": "file1.txt",
        "text": "John Doe lives in New York.",
        "entities": [
            {"start": 0, "end": 8, "label": "Person"},
            {"start": 18, "end": 26, "label": "Location"}
        ]
    }
]


for item in sample_data:
    annotations = []
    for ent in item['entities']:
        annotations.append({
            "value": {
                "start": ent["start"],
                "end": ent["end"],
                "text": item["text"][ent["start"]:ent["end"]],
                "labels": [ent["label"]]
            },
            "from_name": "label",
            "to_name": "text",
            "type": "labels"
        })

    label_studio_data.append({
        "data": {
            "text": item["text"],
            "filename": item["filename"],  # Optional extra field
            "keyword": item["keyword"]     # Optional extra field
        },
        "annotations": [
            {
                "result": annotations
            }
        ]
    })

# Save to file
with open("label_studio_input.json", "w") as f:
    json.dump(label_studio_data, f, indent=2)
