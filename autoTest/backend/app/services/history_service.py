from sqlalchemy.orm import Session
from app.models.history import History
from typing import List, Optional

class HistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_history(self, user_id: str, query: str, response: str, testcases: str = None) -> History:
        history = History(
            user_id=user_id,
            query=query,
            response=response,
            testcases=testcases
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_user_history(self, user_id: str, skip: int = 0, limit: int = 10) -> List[History]:
        return self.db.query(History)\
            .filter(History.user_id == user_id)\
            .order_by(History.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_history_by_id(self, history_id: int) -> Optional[History]:
        return self.db.query(History).filter(History.id == history_id).first()

    def delete_history(self, history_id: int) -> bool:
        history = self.get_history_by_id(history_id)
        if history:
            self.db.delete(history)
            self.db.commit()
            return True
        return False 