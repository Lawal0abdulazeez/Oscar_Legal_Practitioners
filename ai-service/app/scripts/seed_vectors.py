import os
import sys

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.vector_store import get_vector_store

def seed_vectors():
    vs = get_vector_store()
    
    docs = [
        "The Constitution of the Federal Republic of Nigeria 1999 (as amended) is the supreme law of the land.",
        "A Non-Disclosure Agreement (NDA) is a legally binding contract that establishes a confidential relationship.",
        "In Nigerian labor law, an employer must provide a written contract of employment within 3 months of engagement.",
        "The Tenancy Law of Lagos State 2011 regulates the relationship between landlords and tenants.",
        "Burden of proof in civil cases lies with the plaintiff on the preponderance of evidence."
    ]
    
    metadatas = [
        {"jurisdiction": "nigeria", "title": "Constitution", "source": "Statute"},
        {"jurisdiction": "all", "title": "NDA Basics", "source": "General Law"},
        {"jurisdiction": "nigeria", "title": "Labor Act", "source": "Statute"},
        {"jurisdiction": "nigeria", "title": "Tenancy Law Lagos", "source": "Statute"},
        {"jurisdiction": "all", "title": "Evidence Act", "source": "Statute"}
    ]
    
    ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    
    vs.add_documents(documents=docs, metadatas=metadatas, ids=ids)
    print("Vector database seeded with initial legal documents.")

if __name__ == "__main__":
    seed_vectors()
