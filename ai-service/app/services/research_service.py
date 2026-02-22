from openai import OpenAI
import os
from typing import List, Dict, Optional
from app.services.vector_store import get_vector_store

class ResearchService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.vector_store = get_vector_store()

    async def perform_research(
        self, 
        query: str, 
        jurisdiction: Optional[str] = None,
        top_k: int = 5
    ) -> Dict:
        """
        Perform legal research using RAG.
        1. Retrieve relevant documents from vector store.
        2. Generate response using OpenAI.
        """
        # 1. Retrieval
        where_filter = {"jurisdiction": jurisdiction} if jurisdiction else None
        search_results = self.vector_store.query(
            query_text=query,
            n_results=top_k,
            where_filter=where_filter
        )

        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]

        # 2. Preparation of Context
        context = ""
        for doc, meta in zip(documents, metadatas):
            source = meta.get("source", "Unknown Source")
            title = meta.get("title", "Untitled")
            context += f"SOURCE: {title} ({source})\nCONTENT: {doc}\n\n"

        if not context:
            context = "No relevant legal documents found in the internal database."

        # 3. Generation
        system_prompt = """You are a senior legal research assistant for 'Oscar Legal Practitioners'. 
Your task is to provide accurate, well-cited, and academic legal research based on the context provided.
Always cite your sources clearly. Use a professional and formal tone.
If the context doesn't contain the answer, use your internal knowledge but clearly state what is from external knowledge.
WARNING: This is for academic purposes only. Does not constitute real legal advice."""

        user_prompt = f"CONTEXT:\n{context}\n\nRESEARCH QUESTION: {query}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )

            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": metadatas,
                "query": query
            }
        except Exception as e:
            return {
                "error": str(e),
                "answer": "Failed to generate research results due to an error.",
                "query": query
            }

research_service = ResearchService()
