from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Oscar Legal AI Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel
from typing import Optional
from app.services.research_service import research_service
from app.services.drafting_service import drafting_service
from typing import List, Optional

class ResearchRequest(BaseModel):
    query: str
    jurisdiction: Optional[str] = None
    top_k: int = 5

class DraftingRequest(BaseModel):
    template_type: str
    party_a: str
    party_b: str
    jurisdiction: str
    additional_clauses: Optional[List[str]] = None

class AnalysisRequest(BaseModel):
    issue: str
    context: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Oscar Legal AI Service is running", "status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/research")
async def legal_research(request: ResearchRequest):
    return await research_service.perform_research(
        query=request.query,
        jurisdiction=request.jurisdiction,
        top_k=request.top_k
    )

@app.post("/api/v1/draft")
async def generate_draft(request: DraftingRequest):
    return await drafting_service.generate_document(
        template_type=request.template_type,
        party_a=request.party_a,
        party_b=request.party_b,
        jurisdiction=request.jurisdiction,
        additional_clauses=request.additional_clauses
    )

@app.post("/api/v1/analyze")
async def analyze_legal_issue(request: AnalysisRequest):
    return await drafting_service.analyze_legal_issue(
        issue=request.issue,
        context=request.context
    )
