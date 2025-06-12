import requests
import json
import time

# 🔧 Setup
ENDPOINT = "https://<your-resource-name>.<region>.cognitiveservices.azure.com"
API_KEY = "<your-subscription-key>"
PROJECT_NAME = "my-clu-project"
DEPLOYMENT_NAME = "production"
HEADERS = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/json"
}
API_VERSION = "2022-05-01"

# 1️⃣ Create Project
print("🔧 Creating project...")
project_url = f"{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT_NAME}?api-version={API_VERSION}"
project_body = {
    "projectKind": "Conversation",
    "settings": {
        "confidenceThreshold": 0.5
    },
    "language": "en"
}
response = requests.put(project_url, headers=HEADERS, json=project_body)
print("✅ Project created:", response.status_code)

# 2️⃣ Import Dataset (project.json)
print("📤 Importing dataset...")
import_url = f"{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT_NAME}/import?api-version={API_VERSION}"
with open("project.json", "r") as f:
    data = f.read()
response = requests.post(import_url, headers=HEADERS, data=data)
print("✅ Import started:", response.status_code)

# Wait for import to complete (poll status if needed)

# 3️⃣ Train Model (Advanced)
print("🧠 Starting training...")
train_url = f"{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT_NAME}/train?api-version={API_VERSION}"
train_body = {
    "modelLabel": "Latest",
    "trainingMode": "Advanced"  # 👈 Advanced training mode
}
train_response = requests.post(train_url, headers=HEADERS, json=train_body)
operation_url = train_response.headers["operation-location"]

# ⏳ Poll until training completes
while True:
    poll = requests.get(operation_url, headers=HEADERS)
    status = poll.json()["status"]
    print(f"Training status: {status}")
    if status in ["succeeded", "failed"]:
        break
    time.sleep(5)

# 4️⃣ Deploy Model
print("🚀 Deploying model...")
deploy_url = f"{ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT_NAME}/deployments/{DEPLOYMENT_NAME}?api-version={API_VERSION}"
deploy_body = {
    "modelLabel": "Latest"
}
response = requests.put(deploy_url, headers=HEADERS, json=deploy_body)
print("✅ Deployment triggered:", response.status_code)

# 5️⃣ Test Prediction
print("🔍 Running test query...")
predict_url = f"{ENDPOINT}/language/:analyze-conversations?api-version={API_VERSION}"
query = "Book me a flight to Delhi"
predict_body = {
    "kind": "Conversation",
    "analysisInput": {
        "conversationItem": {
            "participantId": "user1",
            "id": "1",
            "modality": "text",
            "language": "en",
            "text": query
        },
        "isLoggingEnabled": False
    },
    "parameters": {
        "projectName": PROJECT_NAME,
        "deploymentName": DEPLOYMENT_NAME,
        "verbose": True
    }
}
runtime_headers = {
    "Ocp-Apim-Subscription-Key": API_KEY,
    "Content-Type": "application/json"
}
response = requests.post(predict_url, headers=runtime_headers, json=predict_body)
print("🎯 Prediction response:\n", json.dumps(response.json(), indent=2))
