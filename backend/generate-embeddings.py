import os
import requests
import uuid
from dotenv import load_dotenv
from utils import UPLOAD_URL, get_access_token, boundary

# Load environment variables from .env file
load_dotenv()


print("Starting embedding generation process...")

# Path to your transcript directories
base_dir = "../output"

# Define directory to save Chroma embeddings
persist_dir = "chroma_db"

# File to track processed transcripts
processed_files_path = "processed_files.txt"

# Load the list of already processed files
if os.path.exists(processed_files_path):
    with open(processed_files_path, "r") as f:
        processed_files = set(f.read().splitlines())
else:
    processed_files = set()

def upload_file(file_path):
    access_token = get_access_token()
    print(access_token)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': f"multipart/form-data; boundary={boundary}",
        'Accept': 'application/json',
    }

    with open(file_path, "rb") as binary_file:
        payload = (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"file\"; filename=\"{file_path.removeprefix('../').split('/')[1]+'_'+str(uuid.uuid4())}\"\r\n"
            "\r\n"
            f"{binary_file.read()}\r\n"
            f"--{boundary}--\r\n"
        )

        print(payload)

        print(f"Uploading file: {file_path}")

        response = requests.post(UPLOAD_URL, headers=headers, data=payload.encode('utf-8'))

        if response.status_code == 201:
            print(f"Successfully uploaded {file_path}")
        else:
            print(f"Failed to index {file_path}. Status code: {response.status_code}, Response: {response.text}")


def process_podcast_transcripts():
    total_podcasts = 0
    total_transcripts = 0
    new_transcripts = 0

    for podcast in os.listdir(base_dir):
        podcast_path = os.path.join(base_dir, podcast, 'transcripts')
        if os.path.isdir(podcast_path):
            total_podcasts += 1
            print(f"Processing podcast: {podcast}")
            for transcript_file in os.listdir(podcast_path):
                if transcript_file not in processed_files:
                    new_transcripts += 1
                    total_transcripts += 1
                    print(f"  Processing new transcript: {transcript_file}")
                    upload_file(os.path.join(podcast_path, transcript_file))
                    # with open(os.path.join(podcast_path, transcript_file), 'r', encoding='utf-8') as f:
                    #     content = f.read()
                    #     # Wrap the content in a Document object
                    #     document = Document(page_content=content)
                    #     # Add the document to the database
                    #     db.add_documents([document])

                    # Add the file to processed list
                    with open(processed_files_path, "a") as f:
                        f.write(transcript_file + "\n")
                    processed_files.add(transcript_file)

    print(f"Finished processing {total_podcasts} podcasts and {new_transcripts} new transcripts (out of {total_transcripts} total).")

# Call the processing function
print("Starting to process podcast transcripts...")
process_podcast_transcripts()

# # Save the embeddings to disk
# print("Saving embeddings to disk...")
# db.persist()

print("Embedding generation process completed.")