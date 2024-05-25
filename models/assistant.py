from pydantic import BaseModel
from typing import Optional

class RunSessionRequest(BaseModel):
    session_id: str