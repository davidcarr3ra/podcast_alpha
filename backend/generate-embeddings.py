import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

print("Starting embedding generation process...")

# Define the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Embedding model initialized.")

# Path to your transcript directories
base_dir = "../output"

# Define directory to save Chroma embeddings
persist_dir = "chroma_db"

# Initialize Chroma DB
db = Chroma(persist_directory=persist_dir, embedding_function=embedding_model)
print(f"Chroma DB initialized with persist directory: {persist_dir}")

# File to track processed transcripts
processed_files_path = "processed_files.txt"

# Load the list of already processed files
if os.path.exists(processed_files_path):
    with open(processed_files_path, "r") as f:
        processed_files = set(f.read().splitlines())
else:
    processed_files = set()

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
                    with open(os.path.join(podcast_path, transcript_file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Wrap the content in a Document object
                        document = Document(page_content=content)
                        # Add the document to the database
                        db.add_documents([document])

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