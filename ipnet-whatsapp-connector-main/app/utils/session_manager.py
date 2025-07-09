import uuid
from time import time

class SessionManager:
    """Gerencia os session_ids dos usuários no Dialogflow CX."""
    
    def __init__(self):
        self.sessions = {}
    
    def get_session_id(self, user_id: str) -> str:
        if user_id in self.sessions:
            return self.sessions[user_id]["session_id"]
        
        session_id = str(uuid.uuid4().hex)
        self.sessions[user_id] = {"session_id": session_id, "timestamp": time()}
        return session_id

    def clear_expired_sessions(self, expiration_time: int = 1800):
        "Remove sessões expiradas (inatividade > expiration_time segundos)"
        current_time = time()
        self.sessions = {
            user_id: session
            for user_id, session in self.sessions.items()
            if current_time - session["timestamp"] < expiration_time
        }
