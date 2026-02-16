# Oscar Legal Practitioners - System Architecture
## Technical Specifications & Infrastructure Design

> **Version**: 1.0 | **Date**: 2026-02-16 | **Status**: Design Phase

---

## 📐 Architecture Overview

### Modular Monolith Pattern

The system follows a **Modular Monolithic Architecture** where different modules are logically separated but deployed as a single unit. This approach provides:

- **Simplicity**: Easier deployment and management for MVP
- **Performance**: No network overhead between modules
- **Flexibility**: Can be split into microservices later if needed
- **Development Speed**: Faster iteration during development

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NGINX REVERSE PROXY                           │
│                     (Port 80/443 - Production)                       │
└────────────┬────────────────────────────────────┬────────────────────┘
             │                                    │
             ▼                                    ▼
┌────────────────────────┐           ┌───────────────────────────────┐
│   FRONTEND SERVICE     │           │     BACKEND API GATEWAY       │
│   (Static Files)       │           │      (Port 8000)              │
│   HTML/CSS/JS          │           │      FastAPI                  │
└────────────────────────┘           └───────────┬───────────────────┘
                                                  │
                    ┌─────────────────────────────┼─────────────────────────┐
                    │                             │                         │
                    ▼                             ▼                         ▼
         ┌──────────────────┐        ┌──────────────────┐    ┌──────────────────┐
         │  AUTH MODULE     │        │   CRM MODULE     │    │  BLOG MODULE     │
         │  - Registration  │        │   - Clients      │    │  - Posts         │
         │  - Login/Logout  │        │   - Cases        │    │  - Categories    │
         │  - JWT Tokens    │        │   - Tasks        │    │  - Newsletter    │
         └──────────────────┘        └──────────────────┘    └──────────────────┘
                    │
                    ▼
         ┌──────────────────────────────────────────────────────────────┐
         │                    AI SERVICE MODULE                          │
         │                      (Port 8001)                              │
         │                       FastAPI                                 │
         ├──────────────────────────────────────────────────────────────┤
         │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
         │  │ Research   │  │ Drafting   │  │ Analysis   │            │
         │  │ Assistant  │  │ Assistant  │  │ Assistant  │            │
         │  └────────────┘  └────────────┘  └────────────┘            │
         │  ┌────────────┐  ┌────────────────────────────┐            │
         │  │ Contract   │  │   Expert System (RAG)      │            │
         │  │ Review     │  │   - Vector Store           │            │
         │  └────────────┘  │   - LLM Integration        │            │
         │                  └────────────────────────────┘            │
         └──────────────────────────────────────────────────────────────┘
                    │                             │
                    ▼                             ▼
         ┌──────────────────┐        ┌──────────────────────┐
         │   PostgreSQL     │        │   ChromaDB           │
         │   (Port 5432)    │        │   (Vector Store)     │
         │   - User Data    │        │   - Embeddings       │
         │   - CRM Data     │        │   - Legal Docs       │
         │   - Documents    │        │   - Knowledge Base   │
         └──────────────────┘        └──────────────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │   Redis          │
         │   (Port 6379)    │
         │   - Caching      │
         │   - Sessions     │
         │   - Task Queue   │
         └──────────────────┘
```

---

## 🏛️ Module Architecture

### 1. Frontend Module

#### Technology Stack
- **HTML5**: Semantic markup
- **CSS3**: Custom properties, Grid, Flexbox
- **JavaScript ES6+**: Modules, async/await, Fetch API

#### Architecture Pattern: Component-Based

```
Frontend Architecture
├── Pages (Routes)
│   ├── Landing Page (/)
│   ├── Authentication (/signup, /signin)
│   ├── Dashboard (/dashboard)
│   ├── Research (/research)
│   ├── Drafting (/drafting)
│   ├── Analysis (/analysis)
│   ├── Contract Review (/contracts)
│   ├── CRM (/crm)
│   └── Blog (/blog)
│
├── Components (Reusable)
│   ├── Navigation
│   ├── Footer
│   ├── Modals
│   ├── Forms
│   ├── Cards
│   └── Tables
│
├── Services (API Communication)
│   ├── AuthService
│   ├── UserService
│   ├── CRMService
│   ├── AIService
│   └── BlogService
│
└── Utils
    ├── Validators
    ├── Formatters
    ├── Storage (localStorage)
    └── EventBus
```

#### Key Design Patterns

**1. Module Pattern**
```javascript
// Example: AuthService
const AuthService = (function() {
    const API_URL = '/api/v1/auth';
    
    async function login(email, password) {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        return response.json();
    }
    
    return { login };
})();
```

**2. Component Pattern**
```javascript
// Example: Reusable Card Component
class Card {
    constructor(title, content, actions) {
        this.title = title;
        this.content = content;
        this.actions = actions;
    }
    
    render() {
        return `
            <div class="card">
                <h3>${this.title}</h3>
                <div class="card-content">${this.content}</div>
                <div class="card-actions">${this.actions}</div>
            </div>
        `;
    }
}
```

#### State Management
```javascript
// Simple state management
class StateManager {
    constructor() {
        this.state = {};
        this.listeners = {};
    }
    
    setState(key, value) {
        this.state[key] = value;
        this.notify(key, value);
    }
    
    subscribe(key, callback) {
        if (!this.listeners[key]) this.listeners[key] = [];
        this.listeners[key].push(callback);
    }
    
    notify(key, value) {
        if (this.listeners[key]) {
            this.listeners[key].forEach(cb => cb(value));
        }
    }
}
```

---

### 2. Backend Module

#### Technology Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy 2.0**: ORM with async support
- **Pydantic v2**: Data validation
- **Alembic**: Database migrations
- **PostgreSQL**: Primary database
- **Redis**: Caching and sessions

#### Architecture Pattern: Layered Architecture

```
Backend Layers
├── API Layer (Routes)
│   ├── Request validation
│   ├── Response formatting
│   └── Error handling
│
├── Service Layer (Business Logic)
│   ├── Business rules
│   ├── Orchestration
│   └── Transaction management
│
├── Repository Layer (Data Access)
│   ├── Database queries
│   ├── CRUD operations
│   └── Query optimization
│
└── Model Layer (Data Models)
    ├── SQLAlchemy models
    ├── Pydantic schemas
    └── Database relationships
```

#### Core Components

**1. Application Factory**
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, clients, cases, blog

def create_app() -> FastAPI:
    app = FastAPI(
        title="Oscar Legal Practitioners API",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(clients.router, prefix="/api/v1/clients", tags=["clients"])
    app.include_router(cases.router, prefix="/api/v1/cases", tags=["cases"])
    app.include_router(blog.router, prefix="/api/v1/blog", tags=["blog"])
    
    return app

app = create_app()
```

**2. Configuration Management**
```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Oscar Legal Practitioners"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # AI Service
    AI_SERVICE_URL: str = "http://localhost:8001"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**3. Database Models**
```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    CLIENT = "client"
    LAWYER = "lawyer"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
```

**4. Pydantic Schemas**
```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_verified: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**5. Service Layer**
```python
# backend/app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def register_user(self, user_data: UserCreate) -> User:
        # Check if user exists
        existing_user = self.db.query(User).filter(
            User.email == user_data.email
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=get_password_hash(user_data.password)
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> dict:
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
```

**6. API Routes**
```python
# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    auth_service = AuthService(db)
    return auth_service.authenticate_user(
        login_data.email, 
        login_data.password
    )
```

**7. Security Utilities**
```python
# backend/app/core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt
```

---

### 3. AI Service Module

#### Technology Stack
- **FastAPI**: API framework
- **LangChain**: LLM orchestration
- **OpenAI/Anthropic**: LLM providers
- **ChromaDB**: Vector database
- **Sentence Transformers**: Embeddings
- **PyPDF2/python-docx**: Document processing

#### Architecture Pattern: Service-Oriented

```
AI Service Architecture
├── API Gateway
│   └── Route requests to appropriate services
│
├── Core Services
│   ├── Research Service
│   ├── Drafting Service
│   ├── Analysis Service
│   ├── Contract Service
│   └── Expert Service (RAG)
│
├── RAG Pipeline
│   ├── Document Ingestion
│   ├── Chunking & Embedding
│   ├── Vector Storage
│   ├── Retrieval
│   └── Generation
│
└── Utilities
    ├── Document Parser
    ├── Text Processor
    └── Prompt Templates
```

#### RAG Implementation

**1. Vector Store Setup**
```python
# ai-service/app/rag/vector_store.py
import chromadb
from chromadb.config import Settings
from typing import List, Dict

class VectorStore:
    def __init__(self, persist_directory: str = "./data/vector_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
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
        filter_dict: Dict = None
    ) -> Dict:
        """Query vector store"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=filter_dict
        )
        return results
```

**2. Embeddings Service**
```python
# ai-service/app/rag/embeddings.py
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        return self.model.encode(text).tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts"""
        return self.model.encode(texts).tolist()
```

**3. Document Retriever**
```python
# ai-service/app/rag/retriever.py
from app.rag.vector_store import VectorStore
from typing import List, Dict

class DocumentRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = 5,
        filters: Dict = None
    ) -> List[Dict]:
        """Retrieve relevant documents"""
        results = self.vector_store.query(
            query_text=query,
            n_results=top_k,
            filter_dict=filters
        )
        
        documents = []
        for i in range(len(results['ids'][0])):
            documents.append({
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return documents
```

**4. Response Generator**
```python
# ai-service/app/rag/generator.py
from openai import OpenAI
from typing import List, Dict

class ResponseGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def generate(
        self, 
        query: str, 
        context_documents: List[Dict],
        system_prompt: str = None
    ) -> Dict:
        """Generate response using retrieved context"""
        
        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['content']}"
            for i, doc in enumerate(context_documents)
        ])
        
        # Default system prompt
        if not system_prompt:
            system_prompt = """You are a legal research assistant. 
            Provide accurate, well-researched answers based on the provided context.
            Always cite your sources and include relevant case law or statutes.
            If you're unsure, say so. Never provide definitive legal advice."""
        
        # Create messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
        
        # Generate response
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )
        
        return {
            "answer": response.choices[0].message.content,
            "sources": [doc['metadata'] for doc in context_documents],
            "model": response.model,
            "tokens_used": response.usage.total_tokens
        }
```

**5. Legal Research Service**
```python
# ai-service/app/services/research_service.py
from app.rag.vector_store import VectorStore
from app.rag.retriever import DocumentRetriever
from app.rag.generator import ResponseGenerator
from typing import Dict, List

class ResearchService:
    def __init__(
        self, 
        vector_store: VectorStore,
        openai_api_key: str
    ):
        self.retriever = DocumentRetriever(vector_store)
        self.generator = ResponseGenerator(openai_api_key)
    
    async def research_query(
        self, 
        query: str,
        jurisdiction: str = None,
        top_k: int = 5
    ) -> Dict:
        """Process legal research query"""
        
        # Build filters
        filters = {}
        if jurisdiction:
            filters['jurisdiction'] = jurisdiction
        
        # Retrieve relevant documents
        documents = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters if filters else None
        )
        
        # Generate response
        result = self.generator.generate(
            query=query,
            context_documents=documents
        )
        
        return {
            "query": query,
            "answer": result["answer"],
            "sources": result["sources"],
            "retrieved_documents": len(documents),
            "tokens_used": result["tokens_used"]
        }
```

**6. Contract Review Service**
```python
# ai-service/app/services/contract_service.py
from openai import OpenAI
from typing import Dict, List
import PyPDF2
from io import BytesIO

class ContractReviewService:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF"""
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    async def review_contract(
        self, 
        contract_text: str,
        contract_type: str = "general"
    ) -> Dict:
        """Review contract and identify issues"""
        
        system_prompt = """You are a contract review specialist.
        Analyze the contract and identify:
        1. Key clauses and their implications
        2. Potential risks or unfavorable terms
        3. Missing standard clauses
        4. Ambiguous language
        5. Recommendations for improvement
        
        Provide a structured analysis."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contract Type: {contract_type}\n\nContract:\n{contract_text}"}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=0.2,
            max_tokens=2000
        )
        
        # Extract clauses (simplified)
        clauses = self._extract_clauses(contract_text)
        
        return {
            "analysis": response.choices[0].message.content,
            "clauses_identified": len(clauses),
            "contract_type": contract_type,
            "tokens_used": response.usage.total_tokens
        }
    
    def _extract_clauses(self, text: str) -> List[Dict]:
        """Extract clauses from contract (simplified)"""
        # This is a simplified version
        # In production, use more sophisticated NLP
        clauses = []
        sections = text.split('\n\n')
        
        for i, section in enumerate(sections):
            if len(section.strip()) > 50:  # Minimum clause length
                clauses.append({
                    "id": i + 1,
                    "content": section.strip(),
                    "type": "general"  # Would classify in production
                })
        
        return clauses
```

---

## 🗄️ Database Design

### Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    Users    │         │   Clients   │         │    Cases    │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │────┐    │ id (PK)     │────┐    │ id (PK)     │
│ email       │    │    │ lawyer_id   │    │    │ client_id   │
│ password    │    └───▶│ name        │    └───▶│ lawyer_id   │
│ first_name  │         │ email       │         │ case_number │
│ last_name   │         │ phone       │         │ title       │
│ role        │         │ address     │         │ description │
│ is_verified │         │ status      │         │ status      │
│ created_at  │         │ created_at  │         │ priority    │
└─────────────┘         └─────────────┘         │ created_at  │
                                                 └─────────────┘
       │                                                │
       │                                                │
       ▼                                                ▼
┌─────────────┐                                 ┌─────────────┐
│  Documents  │                                 │    Tasks    │
├─────────────┤                                 ├─────────────┤
│ id (PK)     │                                 │ id (PK)     │
│ user_id     │                                 │ case_id     │
│ template_id │                                 │ assigned_to │
│ title       │                                 │ title       │
│ content     │                                 │ description │
│ version     │                                 │ due_date    │
│ status      │                                 │ status      │
│ created_at  │                                 │ priority    │
└─────────────┘                                 └─────────────┘

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Blog Posts │         │ Categories  │         │ Subscribers │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id (PK)     │         │ id (PK)     │         │ id (PK)     │
│ author_id   │         │ name        │         │ email       │
│ title       │         │ slug        │         │ status      │
│ slug        │         │ description │         │ subscribed  │
│ content     │         │ created_at  │         │ created_at  │
│ category_id │────────▶│             │         └─────────────┘
│ status      │         └─────────────┘
│ published   │
└─────────────┘
```

### Complete Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'client' CHECK (role IN ('client', 'lawyer', 'admin')),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Verification Tokens
CREATE TABLE verification_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    token_type VARCHAR(50) NOT NULL CHECK (token_type IN ('email_verification', 'password_reset')),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_tokens_user ON verification_tokens(user_id);
CREATE INDEX idx_tokens_token ON verification_tokens(token);

-- Clients
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    lawyer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_clients_lawyer ON clients(lawyer_id);
CREATE INDEX idx_clients_status ON clients(status);

-- Cases
CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    lawyer_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    case_number VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'closed', 'archived')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE,
    closed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_cases_client ON cases(client_id);
CREATE INDEX idx_cases_lawyer ON cases(lawyer_id);
CREATE INDEX idx_cases_status ON cases(status);

-- Tasks
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_tasks_case ON tasks(case_id);
CREATE INDEX idx_tasks_assigned ON tasks(assigned_to);
CREATE INDEX idx_tasks_status ON tasks(status);

-- Communications
CREATE TABLE communications (
    id SERIAL PRIMARY KEY,
    case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('email', 'phone', 'meeting', 'note')),
    subject VARCHAR(255),
    content TEXT,
    direction VARCHAR(20) CHECK (direction IN ('inbound', 'outbound')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_comms_case ON communications(case_id);
CREATE INDEX idx_comms_client ON communications(client_id);

-- Document Templates
CREATE TABLE document_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    content_template TEXT NOT NULL,
    required_fields JSONB,
    jurisdiction VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- User Documents
CREATE TABLE user_documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES document_templates(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'final', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_docs_user ON user_documents(user_id);

-- Document Versions
CREATE TABLE document_versions (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES user_documents(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    changed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Research Sessions
CREATE TABLE research_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    filters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Research Results
CREATE TABLE research_results (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES research_sessions(id) ON DELETE CASCADE,
    document_id VARCHAR(255),
    relevance_score FLOAT,
    snippet TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Contracts
CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    contract_type VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'approved', 'rejected')),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Contract Reviews
CREATE TABLE contract_reviews (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER REFERENCES contracts(id) ON DELETE CASCADE,
    overall_risk VARCHAR(20) CHECK (overall_risk IN ('low', 'medium', 'high', 'critical')),
    findings JSONB,
    recommendations TEXT,
    reviewed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Blog Categories
CREATE TABLE blog_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Blog Posts
CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    category_id INTEGER REFERENCES blog_categories(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_posts_author ON blog_posts(author_id);
CREATE INDEX idx_posts_category ON blog_posts(category_id);
CREATE INDEX idx_posts_status ON blog_posts(status);

-- Newsletter Subscribers
CREATE TABLE newsletter_subscribers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'unsubscribed')),
    subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    unsubscribed_at TIMESTAMP WITH TIME ZONE
);

-- Contact Inquiries
CREATE TABLE contact_inquiries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'resolved', 'closed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_inquiries_status ON contact_inquiries(status);

-- Expert Queries (RAG)
CREATE TABLE expert_queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    context TEXT,
    response TEXT,
    sources JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Query Feedback
CREATE TABLE query_feedback (
    id SERIAL PRIMARY KEY,
    query_id INTEGER REFERENCES expert_queries(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🐳 Docker Infrastructure

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: oscar_legal_db
    environment:
      POSTGRES_DB: oscar_legal
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis
  redis:
    image: redis:7-alpine
    container_name: oscar_legal_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend Service
  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    container_name: oscar_legal_backend
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/oscar_legal
      REDIS_URL: redis://redis:6379
      SECRET_KEY: ${SECRET_KEY}
      AI_SERVICE_URL: http://ai-service:8001
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # AI Service
  ai-service:
    build:
      context: ./ai-service
      dockerfile: ../docker/Dockerfile.ai
    container_name: oscar_legal_ai
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      VECTOR_DB_PATH: /app/data/vector_db
    ports:
      - "8001:8001"
    volumes:
      - ./ai-service:/app
      - vector_data:/app/data/vector_db
    command: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

  # Nginx (Production)
  nginx:
    image: nginx:alpine
    container_name: oscar_legal_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - ai-service

volumes:
  postgres_data:
  redis_data:
  vector_data:
```

### Backend Dockerfile

```dockerfile
# docker/Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/app ./app
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### AI Service Dockerfile

```dockerfile
# docker/Dockerfile.ai
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ai-service/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download sentence transformers model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application
COPY ai-service/app ./app

# Expose port
EXPOSE 8001

# Start server
CMD uvicorn app.main:app --host 0.0.0.0 --port 8001
```

---

## 🔐 Security Architecture

### Authentication Flow

```
1. User Registration
   ├─▶ Frontend: Submit registration form
   ├─▶ Backend: Validate input
   ├─▶ Backend: Hash password (bcrypt)
   ├─▶ Backend: Create user record
   ├─▶ Backend: Generate verification token
   ├─▶ Backend: Send verification email
   └─▶ Frontend: Show success message

2. Email Verification
   ├─▶ User: Click verification link
   ├─▶ Backend: Validate token
   ├─▶ Backend: Mark user as verified
   └─▶ Frontend: Redirect to login

3. User Login
   ├─▶ Frontend: Submit login credentials
   ├─▶ Backend: Validate credentials
   ├─▶ Backend: Verify password hash
   ├─▶ Backend: Generate JWT token
   ├─▶ Backend: Return token + user data
   └─▶ Frontend: Store token (localStorage)

4. Authenticated Requests
   ├─▶ Frontend: Include JWT in Authorization header
   ├─▶ Backend: Validate JWT signature
   ├─▶ Backend: Check token expiration
   ├─▶ Backend: Extract user from token
   ├─▶ Backend: Verify user permissions
   └─▶ Backend: Process request
```

### Security Best Practices

1. **Password Security**
   - Minimum 8 characters
   - Bcrypt hashing with salt
   - No password in logs or responses

2. **JWT Tokens**
   - Short expiration (30 minutes)
   - Refresh token mechanism
   - Secure secret key
   - HTTPS only in production

3. **Input Validation**
   - Pydantic schemas for all inputs
   - SQL injection prevention (ORM)
   - XSS protection (sanitize outputs)
   - CSRF tokens for forms

4. **API Security**
   - Rate limiting
   - CORS configuration
   - API key for AI service
   - Request size limits

5. **Data Protection**
   - Encrypted database connections
   - Sensitive data encryption at rest
   - Secure file uploads
   - Regular backups

---

## 📊 Performance Considerations

### Caching Strategy

```python
# Redis caching for expensive operations
from redis import Redis
import json

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = Redis.from_url(redis_url)
    
    def get(self, key: str):
        value = self.redis.get(key)
        return json.loads(value) if value else None
    
    def set(self, key: str, value: dict, ttl: int = 3600):
        self.redis.setex(key, ttl, json.dumps(value))
    
    def delete(self, key: str):
        self.redis.delete(key)
```

### Database Optimization

1. **Indexing**
   - Index foreign keys
   - Index frequently queried columns
   - Composite indexes for common queries

2. **Query Optimization**
   - Use select_related/joinedload for relationships
   - Pagination for large result sets
   - Avoid N+1 queries

3. **Connection Pooling**
   - SQLAlchemy connection pool
   - Max connections: 20
   - Pool timeout: 30s

---

## 📈 Monitoring & Logging

### Logging Configuration

```python
# backend/app/core/logging.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/app.log')
        ]
    )
    
    # Suppress noisy loggers
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
```

---

## 🚀 Deployment Strategy

### Environment Configuration

```bash
# .env.example
# Application
APP_NAME=Oscar Legal Practitioners
DEBUG=False
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/oscar_legal

# Redis
REDIS_URL=redis://localhost:6379

# AI Service
OPENAI_API_KEY=your-openai-key
AI_SERVICE_URL=http://localhost:8001

# Email (Future)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## ✅ Next Steps

1. **Review Architecture**: Ensure all stakeholders understand the design
2. **Set Up Repository**: Initialize with proposed structure
3. **Environment Setup**: Install dependencies and tools
4. **Database Setup**: Create database and run migrations
5. **Begin Phase 1**: Start with authentication and core infrastructure

---

**Document Version**: 1.0  
**Last Updated**: 2026-02-16  
**Status**: Ready for Implementation
