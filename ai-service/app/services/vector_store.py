import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional

class VectorStore:
    def __init__(self, persist_directory: Optional[str] = None):
        if persist_directory is None:
            persist_directory = os.getenv("VECTOR_DB_PATH", "./data/vector_db")
            
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)
            
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="legal_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: List[Dict], 
        ids: List[str]
    ):
        """Add documents to vector store"""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(
        self, 
        query_text: str, 
        n_results: int = 5,
        where_filter: Optional[Dict] = None
    ) -> Dict:
        """Query vector store for similar documents"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_filter
        )
        return results

# Singleton instance
vector_store = None

def get_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = VectorStore()
    return vector_store
