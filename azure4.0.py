
from azure.identity import CertificateCredential
from azure.storage.blob import BlobServiceClient

# Azure AD details
TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
CERT_PATH = "path-to-your-certificate.pem"  # Ensure it's in PEM format

# Storage details
STORAGE_ACCOUNT_NAME = "yourstorageaccount"
CONTAINER_NAME = "your-container"
BLOB_NAME = "uploaded-file.txt"
FILE_PATH = "path-to-your-local-file.txt"

# Authenticate using Certificate
credential = CertificateCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID, certificate_path=CERT_PATH)

# Create Blob Service Client
blob_service_client = BlobServiceClient(account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=credential)

# Get Container Client
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Upload File
with open(FILE_PATH, "rb") as data:
    container_client.upload_blob(name=BLOB_NAME, data=data, overwrite=True)

print("File uploaded successfully!")
