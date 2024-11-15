from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key= openai_api_key)
existing_vector_stores = client.beta.vector_stores.list()
vector_store = None
for store in existing_vector_stores.data:
    if store.name == "Margaret Database - 1":
        vector_store = store
        break
if vector_store is None:
    vector_store = client.beta.vector_stores.create(name="Margaret Database - 1")

# Ready the files for upload to OpenAI
file_paths = ["Ecommerce_FAQ_Chatbot_dataset.json"]  # Add files of any format here
file_streams = [open(path, "rb") for path in file_paths]
 
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)
# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)