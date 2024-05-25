from pydantic import BaseModel
from typing import List


class AudioChunk(BaseModel):
    audio_data: List[int]
    sample_rate: int

class CreateSessionResponse(BaseModel):
    session_id: str

class DurationResponse(BaseModel):
    message: str
    duration: float