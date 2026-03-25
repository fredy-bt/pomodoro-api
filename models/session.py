from datetime import datetime

sessions_db: dict = {}

class Session:
    def __init__(self, id: str, task_id: str, session_type: str, started_at: datetime, finished_at: datetime):
        self.id = id
        self.task_id = task_id
        self.session_type = session_type
        self.started_at = started_at
        self.finished_at = finished_at

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "session_type": self.session_type,
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat()
        }