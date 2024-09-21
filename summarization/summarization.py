import os
import openai

# Set up OpenAI API key
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
OUTPUT_FILE = "output.txt"

client = openai.OpenAI(
    api_key=api_key
)


def query_gpt4(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="o1-mini"
        )
        response = response.choices[0].message.content
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def read_files_from_folder(foldername):
    try:
        files = os.listdir(foldername)
        return [os.path.join(foldername, f) for f in files if os.path.isfile(os.path.join(foldername, f))]
    except FileNotFoundError as e:
        return f"Folder not found: {str(e)}"

def write_output(response):
    with open(OUTPUT_FILE, "w") as outfile:
        outfile.write(response)

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def process_files_in_folder(foldername):
    for root, dirs, _ in os.walk(foldername):
        if 'transcripts' in dirs:
            transcripts_folder = os.path.join(root, 'transcripts')
            for transcript_file in os.listdir(transcripts_folder):
                file_path = os.path.join(transcripts_folder, transcript_file)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r") as f:
                            file_content = f.read()
                            print(f"Processing file: {file_path}")
                            response = query_gpt4("For every crypto company referred in the transcript, summarize everything covered in this conversation. Create a table and don't say anything else.\n" + file_content)
                            response = query_gpt4("Take the union of all information present in these two tables.\n" + read_file("output.txt") + "\n" + response)
                            # write_output(response, file_path.replace(".txt", "_summary.txt"))
                            write_output(response)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {str(e)}")

if __name__ == "__main__":
    foldername = "../data"
    process_files_in_folder(foldername)
    print("Processing complete. Responses saved to output.txt.")
