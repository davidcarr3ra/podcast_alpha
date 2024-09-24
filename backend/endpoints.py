# Backend for embedding and retrieval
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from datetime import datetime
import requests

from utils import get_access_token, boundary, QUERY_URL

# client = OpenAI()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load or generate the embeddings
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# db = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)

def query_vectara(query):
	access_token = get_access_token()
	headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
	print(QUERY_URL+f"?query={query.encode('utf-8')}")
	response = requests.request("GET", QUERY_URL+f"?query={query.encode('utf-8')}", headers=headers, data={})
	if response.status_code == 200:
		print(f"Successfully queried {query}, response: {response.json()}")
	else:
		print(f"Failed to index {query}. Status code: {response.status_code}, Response: {response.text}")


@app.post("/query")
async def query(request: Request):
	data = await request.json()
	query_text = data.get("query")
	query_vectara(query_text)
	
# # Function to generate response using retrieved docs as context
# def generate_response(docs, query):
# 	# Use a language model (GPT or similar) to generate a response
# 	# from the retrieved documents.
# 	context = "\n".join([doc.page_content for doc in docs])
	
# 	# Limit the context size to avoid exceeding rate limits
# 	max_context_length = 3000  # Adjust this value as needed
# 	truncated_context = context[:max_context_length]
	
# 	try:
# 		completion = client.chat.completions.create(
# 			model="gpt-3.5-turbo",  # Use a smaller model
# 			messages=[
# 				{"role": "system", "content": "You are a helpful assistant. Use the following context to answer the user's query."},
# 				{"role": "user", "content": f"Context: {truncated_context}\n\nQuery: {query}"}
# 			],
# 			max_tokens=500  # Limit the response size
# 		)
# 		return completion.choices[0].message.content
# 	except Exception as e:
# 		raise e

@app.post("/summarize_podcasts")
async def summarize_podcasts(request: Request):
	data = await request.json()
	date_str = data.get("date")
	
	try:
		# Convert the input date string to a datetime object
		date = datetime.strptime(date_str, "%Y-%m-%d")
	except ValueError:
		return {"error": "Invalid date format. Please use YYYY-MM-DD."}

	# Query the database for documents from the specified date
	query = f"What is the summary for the date: {date.strftime('%Y-%m-%d')}"
	query_vectara(query)

# def generate_podcast_summary(docs, date):
# 	context = "\n".join([doc.page_content for doc in docs])
	
# 	# Limit the context size to avoid exceeding rate limits
# 	max_context_length = 3000  # Adjust this value as needed
# 	truncated_context = context[:max_context_length]
	
# 	try:
# 		completion = client.chat.completions.create(
# 			model="gpt-3.5-turbo",
# 			messages=[
# 				{"role": "system", "content": "You are a helpful assistant. Summarize the main topics discussed in the podcasts for the given date."},
# 				{"role": "user", "content": f"Context: {truncated_context}\n\nSummarize the main topics discussed in the podcasts on {date.strftime('%Y-%m-%d')}:"}
# 			],
# 			max_tokens=500  # Limit the response size
# 		)
# 		return completion.choices[0].message.content
# 	except Exception as e:
# 		raise e
