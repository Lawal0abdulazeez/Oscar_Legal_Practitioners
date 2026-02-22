from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.blog import BlogStatus
from app.models.user import User, UserRole
from app.models import blog as blog_models
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Simple Schemas (Inline for speed, can be moved to schemas/ later)
class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: str = None
    category_id: int = None

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostResponse(BlogPostBase):
    id: int
    author_id: int
    status: BlogStatus
    created_at: datetime
    class Config: from_attributes = True

@router.get("/", response_model=List[BlogPostResponse])
def get_posts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10,
):
    """Get all published blog posts."""
    return db.query(blog_models.BlogPost)\
        .filter(blog_models.BlogPost.status == BlogStatus.PUBLISHED)\
        .offset(skip).limit(limit).all()

@router.post("/", response_model=BlogPostResponse)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: BlogPostCreate,
    current_user: User = Depends(deps.get_current_active_user),
):
    """Create a new blog post (Lawyers/Admins only)."""
    if current_user.role not in [UserRole.LAWYER, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_post = blog_models.BlogPost(
        **post_in.dict(),
        author_id=current_user.id,
        status=BlogStatus.PUBLISHED # For MVP auto-publish
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Newsletter & Contact
class NewsletterSubscribe(BaseModel):
    email: str

@router.post("/subscribe")
def subscribe_newsletter(
    data: NewsletterSubscribe,
    db: Session = Depends(deps.get_db)
):
    existing = db.query(blog_models.NewsletterSubscriber)\
        .filter(blog_models.NewsletterSubscriber.email == data.email).first()
    if existing:
        return {"message": "Already subscribed"}
    
    sub = blog_models.NewsletterSubscriber(email=data.email)
    db.add(sub)
    db.commit()
    return {"message": "Subscribed successfully"}
