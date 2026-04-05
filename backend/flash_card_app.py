from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Simple Flashcard API")

# Define the origins that are allowed to talk to your server
origins = [
    "http://localhost:3000",  # Default React port
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Default Vite/React port
    "http://127.0.0.1:5173",
]

# Used for pre-built middleware classes (like CORS or GZip)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Data Model
class FlashcardItem(BaseModel):
    id: int  # use int to match the JavaScript Date.now() output
    question: str
    answer: str
    isFlipped: bool = False


# Define the internal "Database" as a list
flashcard_db = []

# --- Endpoints ---


@app.get("/flashcards", response_model=List[FlashcardItem])
async def get_all_flashcards():
    """Fetch the entire flashcard deck."""
    return flashcard_db


@app.post("/flashcards", response_model=FlashcardItem)
async def create_flashcard(item: FlashcardItem):
    """Add a new flashcard to the deck."""
    # Check if ID already exists
    if any(x.id == item.id for x in flashcard_db):
        raise HTTPException(status_code=400, detail="ID already exists")

    flashcard_db.append(item)
    return item


@app.put("/flashcards/{flashcard_id}", response_model=FlashcardItem)
async def update_flashcard(flashcard_id: int, updated_item: FlashcardItem):
    """Update an existing flashcard by its ID."""
    for index, item in enumerate(flashcard_db):
        if item.id == flashcard_id:
            flashcard_db[index] = updated_item
            return updated_item

    raise HTTPException(status_code=404, detail="Flashcard not found")


@app.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(flashcard_id: int):
    """Remove a flashcard from the deck."""
    for index, item in enumerate(flashcard_db):
        if item.id == flashcard_id:
            flashcard_db.pop(index)
            return {"message": f"Flashcard {flashcard_id} deleted successfully"}

    raise HTTPException(status_code=404, detail="Flashcard not found")


@app.put("/flashcards/{flashcard_id}/flip", response_model=FlashcardItem)
async def flip_flashcard(flashcard_id: int):
    """Toggle the flip state of a flashcard."""
    for index, item in enumerate(flashcard_db):
        if item.id == flashcard_id:
            flashcard_db[index].isFlipped = not flashcard_db[index].isFlipped
            return flashcard_db[index]

    raise HTTPException(status_code=404, detail="Flashcard not found")