import os
import docx2txt
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB collection
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="document_chunks",
    embedding_function = SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/all-MiniLM-L6-v2")

)

def extract_text(file_path, doc_type):
    if doc_type == "pdf":
        reader = PdfReader(file_path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif doc_type == "docx":
        return docx2txt.process(file_path)
    elif doc_type == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def embed_and_store_chunks(chunks, doc_id):
    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{"doc_id": doc_id, "chunk_index": idx}],
            ids=[f"{doc_id}_{idx}"]
        )

def query_rag(doc_id, question, top_k=3):
    question_embedding = embed_model.encode(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
        where={"doc_id": doc_id}
    )
    context = "\n".join(results['documents'][0])
    # This is a mock answer for demonstration
    answer = f"Answer based on context:\n{context}"
    return answer
