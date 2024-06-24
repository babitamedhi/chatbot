from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

router = APIRouter()

class StartRequest(BaseModel):
    resumeData: dict
    questions: list[str]

class StartResponse(BaseModel):
    sessionId: str
    message: str
    end: bool

sessions = {}

@router.post("/start", response_model=StartResponse)
async def start_interview(request: StartRequest):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "questions": request.questions,
        "answered_questions": [],  # Track questions that have been asked
        "current_question_index": 0
    }
    welcome_message = (
        f"Hi {request.resumeData.get('name')}, Welcome to Redyhire interview. "
        "I'm Angella from Redyhire. I'll take your interview today. "
        "Can you give a brief introduction about yourself?"
    )
    return StartResponse(sessionId=session_id, message=welcome_message, end=False)