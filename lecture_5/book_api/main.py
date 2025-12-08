from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from pydantic import BaseModel, Field
from typing import Optional, List

"""Connection to the Database."""
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

"""Definition og the Database and ORM Model."""
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)

"""Creating of tables."""
Base.metadata.create_all(bind=engine)

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=0, le=2100)

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int]

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=0, le=2100)

"""Creating of FastAPI Application."""
app = FastAPI(
    title="Book Collection API",
    description="A simple API to manage book collection",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Adding of endpoints."""
@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the collection."""
    db_book = BookDB(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=List[BookResponse])
def get_all_books(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
        db: Session = Depends(get_db)
):
    """Get all books with pagination."""
    books = db.query(BookDB).offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID."""
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """Update book details."""
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    update_data = book_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book by ID."""
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return None

@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
        title: Optional[str] = Query(None, description="Search by title (partial match)"),
        author: Optional[str] = Query(None, description="Search by author (partial match)"),
        year: Optional[int] = Query(None, description="Search by exact year"),
        db: Session = Depends(get_db)
):
    """Search books by title, author, or year."""
    query = db.query(BookDB)
    if title:
        query = query.filter(BookDB.title.contains(title))
    if author:
        query = query.filter(BookDB.author.contains(author))
    if year:
        query = query.filter(BookDB.year == year)
    return query.all()

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Book Collection API",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "POST /books/": "Add a new book",
            "GET /books/": "Get all books (with pagination)",
            "GET /books/{id}": "Get specific book",
            "PUT /books/{id}": "Update book",
            "DELETE /books/{id}": "Delete book",
            "GET /books/search/": "Search books"
        }
    }