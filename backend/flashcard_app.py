from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

from flashcard_crud import (
    connect_to_mongo,
    close_mongo_connection,
    Flashcard,
    db_get_flashcards,
    db_update_flashcard,
    db_create_flashcard,
    db_delete_flashcard,
    db_get_flashcard,
)

app = FastAPI(title="Flashcard API")

# Define the origins that are allowed to talk to your server
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Pydantic model for request/response
class FlashcardSchema(BaseModel):
    id: str
    question: str
    answer: str
    isFlipped: bool = False


# Startup and shutdown events
@app.on_event("startup")
async def startup():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()


# --- Endpoints ---

@app.get("/flashcards", response_model=List[FlashcardSchema])
async def get_all_flashcards(skip: int = 0, limit: int = 100):
    """Fetch the entire flashcard deck."""
    try:
        flashcards = await db_get_flashcards(skip=skip, limit=limit)
        return [FlashcardSchema(**fc.to_dict()) for fc in flashcards]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/flashcards", response_model=FlashcardSchema)
async def create_flashcard(flashcard: FlashcardSchema):
    """Add a new flashcard to the deck."""
    try:
        fc = Flashcard(
            id=flashcard.id,
            question=flashcard.question,
            answer=flashcard.answer,
            isFlipped=flashcard.isFlipped
        )
        created = await db_create_flashcard(fc)
        return FlashcardSchema(**created.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/flashcards/{flashcard_id}", response_model=FlashcardSchema)
async def update_flashcard(flashcard_id: str, updated_object: FlashcardSchema):
    """Update an existing flashcard by its ID."""
    try:
        fc = Flashcard(
            id=updated_object.id,
            question=updated_object.question,
            answer=updated_object.answer,
            isFlipped=updated_object.isFlipped
        )
        db_flashcard = await db_update_flashcard(flashcard_id, fc)
        if not db_flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        return FlashcardSchema(**db_flashcard.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/flashcards/{flashcard_id}/flip", response_model=FlashcardSchema)
async def flip_flashcard(flashcard_id: str):
    """Toggle the flip state of a flashcard."""
    try:
        flashcard = await db_get_flashcard(flashcard_id)
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        flashcard.isFlipped = not flashcard.isFlipped
        updated = await db_update_flashcard(flashcard_id, flashcard)
        return FlashcardSchema(**updated.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/flashcards/{flashcard_id}")
async def delete_flashcard(flashcard_id: str):
    """Remove a flashcard from the deck."""
    try:
        success = await db_delete_flashcard(flashcard_id)
        if not success:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))