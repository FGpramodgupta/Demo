import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations.authoring import ConversationAuthoringClient
from azure.ai.language.conversations import ConversationAnalysisClient

# 📌 Replace these with your actual values
ENDPOINT = "https://<your-resource-name>.<region>.cognitiveservices.azure.com/"
KEY = "<your-subscription-key>"
PROJECT_NAME = "my-clu-project"
DEPLOYMENT_NAME = "production"
LANGUAGE = "en"

# 📥 Load your project JSON (CLU format)
with open("project.json", "r") as file:
    project_data = json.load(file)

# 🌱 Initialize Authoring Client
authoring_client = ConversationAuthoringClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)

# 1️⃣ Create Project
print("🔧 Creating project...")
authoring_client.create_project(
    project_name=PROJECT_NAME,
    project={
        "language": LANGUAGE,
        "projectKind": "Conversation",
        "settings": {"confidenceThreshold": 0.5}
    }
)

# 2️⃣ Import Project Data
print("📤 Importing training data...")
authoring_client.import_project(
    project_name=PROJECT_NAME,
    project=project_data
)

# 3️⃣ Advanced Training
print("🧠 Starting advanced training...")
poller = authoring_client.train_model(
    project_name=PROJECT_NAME,
    training_mode="Advanced"
)
poller.wait()
print("✅ Training completed.")

# 4️⃣ Deploy Model
print("🚀 Deploying model...")
authoring_client.deploy_project(
    project_name=PROJECT_NAME,
    deployment_name=DEPLOYMENT_NAME,
    trained_model_label="Latest"
)
print("✅ Deployment completed.")

# 5️⃣ Test Prediction
print("🧪 Sending test query...")

runtime_client = ConversationAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)

query_text = "Book me a flight to Mumbai"

response = runtime_client.analyze_conversation(
    task={
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "participantId": "user1",
                "id": "1",
                "modality": "text",
                "language": LANGUAGE,
                "text": query_text
            },
            "isLoggingEnabled": False
        },
        "parameters": {
            "projectName": PROJECT_NAME,
            "deploymentName": DEPLOYMENT_NAME
        }
    }
)

print("🎯 Prediction result:")
print(json.dumps(response, indent=2))
