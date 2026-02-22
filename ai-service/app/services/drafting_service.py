from datetime import datetime
from typing import List, Dict, Optional
from openai import OpenAI
import os

class DraftingService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    async def generate_document(
        self, 
        template_type: str, 
        party_a: str, 
        party_b: str, 
        jurisdiction: str,
        additional_clauses: List[str] = None
    ) -> Dict:
        """Generate a legal document based on template and details."""
        
        system_prompt = f"""You are a senior legal drafting expert specializing in {jurisdiction} law.
Your task is to draft a high-quality, professional, and legally robust {template_type}.
Use precise legal terminology and ensure proper formatting.
WARNING: Academic project only. Not for real legal use."""

        user_prompt = f"""Draft a {template_type} between {party_a} and {party_b}.
Jurisdiction: {jurisdiction}
Additional Requirements: {", ".join(additional_clauses) if additional_clauses else "Standard clauses only."}

Please include:
1. Preamble and Recitals
2. Definitions
3. Core Obligations
4. Term and Termination
5. Dispute Resolution
6. Execution block"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=3000
            )

            content = response.choices[0].message.content
            
            return {
                "document_type": template_type,
                "content": content,
                "jurisdiction": jurisdiction,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    async def analyze_legal_issue(self, issue: str, context: Optional[str] = None) -> Dict:
        """Perform deep legal analysis of a situation or case."""
        
        system_prompt = """You are a senior legal analyst for 'Oscar Legal Practitioners'.
Provide a detailed legal analysis including potential risks, applicable laws (where known), and strategic recommendations.
Structure your response into:
1. Situation Overview
2. Legal Issues Identified
3. Applicable Principles
4. Risk Assessment
5. Strategic Advice"""

        user_prompt = f"ISSUE: {issue}\n\nCONTEXT: {context if context else 'No additional context provided.'}"

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return {"analysis": response.choices[0].message.content}
        except Exception as e:
            return {"error": str(e)}

drafting_service = DraftingService()
