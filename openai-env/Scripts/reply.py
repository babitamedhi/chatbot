from fastapi import APIRouter, HTTPException, Cookie
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
from Scripts.start import sessions
from prompts import (
    relevance_and_harmfulness_prompt,
    additional_answers_prompt,
    next_question_prompt,
    avoid_repeating_questions_prompt
)

router = APIRouter()

# Load environment variables from .env
load_dotenv()

# OpenAI API key loaded from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

class ReplyRequest(BaseModel):
    message: str

class ReplyResponse(BaseModel):
    sessionId: str
    message: str
    end: bool

def generate_next_question(response: str, questions: list, answered_questions: list) -> str:
    unanswered_questions = [q for q in questions if q not in answered_questions]

    if not unanswered_questions:
        return "Thanks for taking this interview. Hope to see you soon"

    prompt = avoid_repeating_questions_prompt.format(
        response=response,
        answered_questions=answered_questions,
        unanswered_questions=unanswered_questions
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an interviewer conducting a job interview."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        next_question = response.choices[0].message['content'].strip()

        if next_question not in unanswered_questions:
            next_question = unanswered_questions[0]

    except Exception as e:
        print(f"OpenAI API error: {e}")
        next_question = unanswered_questions[0]

    return next_question


@router.post("/reply", response_model=ReplyResponse)
async def reply_to_interview(request: ReplyRequest, session_id: str = Cookie(None)):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    answered_questions = session.get("answered_questions", [])
    questions = session.get("questions", [])

    next_question = generate_next_question(request.message, questions, answered_questions)

    if next_question == "Thanks for taking this interview. Hope to see you soon":
        return ReplyResponse(sessionId=session_id, message=next_question, end=True)

    while next_question in answered_questions:
        next_question = generate_next_question(request.message, questions, answered_questions)

    session["answered_questions"] = answered_questions + [next_question]

    return ReplyResponse(sessionId=session_id, message=next_question, end=False)
