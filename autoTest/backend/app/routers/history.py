from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.history_service import HistoryService
from app.models.history import History
from pydantic import BaseModel

router = APIRouter(prefix="/api/history", tags=["history"])

class HistoryCreate(BaseModel):
    user_id: str
    query: str
    response: str

class HistoryResponse(BaseModel):
    id: int
    user_id: str
    query: str
    response: str
    created_at: str

    class Config:
        from_attributes = True

@router.post("/", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    history_service = HistoryService(db)
    return history_service.create_history(
        user_id=history.user_id,
        query=history.query,
        response=history.response
    )

@router.get("/user/{user_id}", response_model=List[HistoryResponse])
def get_user_history(user_id: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    history_service = HistoryService(db)
    return history_service.get_user_history(user_id, skip, limit)

@router.get("/{history_id}", response_model=HistoryResponse)
def get_history(history_id: int, db: Session = Depends(get_db)):
    history_service = HistoryService(db)
    history = history_service.get_history_by_id(history_id)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@router.delete("/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history_service = HistoryService(db)
    if not history_service.delete_history(history_id):
        raise HTTPException(status_code=404, detail="History not found")
    return {"message": "History deleted successfully"} 