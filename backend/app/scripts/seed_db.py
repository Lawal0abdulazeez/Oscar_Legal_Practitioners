import sys
import os

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.client import Client
from app.models.case import Case, CasePriority, CaseStatus
from app.core.security import get_password_hash

def seed():
    db = SessionLocal()
    try:
        # Create a Lawyer
        lawyer_email = "counselor@oscarlegal.com"
        existing_lawyer = db.query(User).filter(User.email == lawyer_email).first()
        if not existing_lawyer:
            lawyer = User(
                email=lawyer_email,
                hashed_password=get_password_hash("password123"),
                full_name="Oscar Counselor",
                role=UserRole.LAWYER,
                is_active=True
            )
            db.add(lawyer)
            db.commit()
            db.refresh(lawyer)
            print(f"Created Lawyer: {lawyer_email}")
        else:
            lawyer = existing_lawyer
            print(f"Lawyer already exists: {lawyer_email}")

        # Create a Client User
        client_user_email = "john.doe@example.com"
        existing_client_user = db.query(User).filter(User.email == client_user_email).first()
        if not existing_client_user:
            client_user = User(
                email=client_user_email,
                hashed_password=get_password_hash("password123"),
                full_name="John Doe",
                role=UserRole.CLIENT,
                is_active=True
            )
            db.add(client_user)
            db.commit()
            db.refresh(client_user)
            print(f"Created Client User: {client_user_email}")
        
        # Create a CRM Client
        existing_client = db.query(Client).filter(Client.email == "info@techcorp.com").first()
        if not existing_client:
            client = Client(
                name="TechCorp Solutions Ltd",
                email="info@techcorp.com",
                phone="+234 801 234 5678",
                address="123 Innovation Drive, Lagos",
                status="active"
            )
            db.add(client)
            db.commit()
            db.refresh(client)
            print(f"Created CRM Client: {client.name}")
        else:
            client = existing_client

        # Create a Case
        existing_case = db.query(Case).filter(Case.case_number == "LD-2024-500").first()
        if not existing_case:
            new_case = Case(
                title="Intellectual Property Dispute",
                case_number="LD-2024-500",
                client_id=client.id,
                priority=CasePriority.HIGH,
                status=CaseStatus.OPEN,
                description="Dispute over software copyright infringement."
            )
            db.add(new_case)
            db.commit()
            print(f"Created Case: {new_case.title}")

    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database...")
    seed()
    print("Seeding complete.")
