# Backend for embedding and retrieval
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from datetime import datetime

client = OpenAI()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this based on your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load or generate the embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)

@app.post("/query")
async def query(request: Request):
	data = await request.json()
	query_text = data.get("query")
	
	# Embed the query and perform similarity search
	similar_docs = db.similarity_search(query_text, k=5)

	# Use the retrieved documents as context for response generation
	try:
		response = generate_response(similar_docs, query_text)
	except Exception as e:
		if isinstance(e, OpenAI.RateLimitError):
			return {"error": "Rate limit exceeded. Please try again later or reduce the size of your query."}
		else:
			return {"error": f"An unexpected error occurred: {str(e)}"}

	return {"response": response}

# Function to generate response using retrieved docs as context
def generate_response(docs, query):
	# Use a language model (GPT or similar) to generate a response
	# from the retrieved documents.
	context = "\n".join([doc.page_content for doc in docs])
	
	# Limit the context size to avoid exceeding rate limits
	max_context_length = 3000  # Adjust this value as needed
	truncated_context = context[:max_context_length]
	
	try:
		completion = client.chat.completions.create(
			model="gpt-3.5-turbo",  # Use a smaller model
			messages=[
				{"role": "system", "content": "You are a helpful assistant. Use the following context to answer the user's query."},
				{"role": "user", "content": f"Context: {truncated_context}\n\nQuery: {query}"}
			],
			max_tokens=500  # Limit the response size
		)
		return completion.choices[0].message.content
	except Exception as e:
		raise e

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
	query = f"podcast date: {date.strftime('%Y-%m-%d')}"
	relevant_docs = db.similarity_search(query, k=10)  # Adjust k as needed

	if not relevant_docs:
		return {"summary": "No podcasts found for the specified date."}

	# Generate a summary using the retrieved documents
	try:
		summary = generate_podcast_summary(relevant_docs, date)
	except Exception as e:
		if isinstance(e, OpenAI.RateLimitError):
			return {"error": "Rate limit exceeded. Please try again later."}
		else:
			return {"error": f"An unexpected error occurred: {str(e)}"}

	return {"summary": summary}

def generate_podcast_summary(docs, date):
	context = "\n".join([doc.page_content for doc in docs])
	
	# Limit the context size to avoid exceeding rate limits
	max_context_length = 3000  # Adjust this value as needed
	truncated_context = context[:max_context_length]
	
	try:
		completion = client.chat.completions.create(
			model="gpt-3.5-turbo",
			messages=[
				{"role": "system", "content": "You are a helpful assistant. Summarize the main topics discussed in the podcasts for the given date."},
				{"role": "user", "content": f"Context: {truncated_context}\n\nSummarize the main topics discussed in the podcasts on {date.strftime('%Y-%m-%d')}:"}
			],
			max_tokens=500  # Limit the response size
		)
		return completion.choices[0].message.content
	except Exception as e:
		raise e