import uuid

class SessionManager:
    def __init__(self, max_size=5000):
        self.max_size = max_size
        self.__sessions = {}

    def create(self, init_transcription: str=''):
        session_id = str(uuid.uuid4())
        self.__sessions[session_id] = init_transcription
        return session_id
    
    def write(self, session_id: str, transcription: str):
        if session_id in self.__sessions:
            self.__sessions[session_id] += transcription
        else:
            raise ValueError("Session ID not found")
        
    def get(self, session_id: str):
        if session_id in self.__sessions:
            return self.__sessions[session_id]
        else:
            raise ValueError("Session ID not found")
        
    def clear(self, session_id: str):
        if session_id in self.__sessions:
            self.__sessions[session_id] = ""
        else:
            raise ValueError("Session ID not found")
        
    def delete(self, session_id: str):
        if session_id in self.__sessions:
            del self.__sessions[session_id]
        else:
            raise ValueError("Session ID not found")
