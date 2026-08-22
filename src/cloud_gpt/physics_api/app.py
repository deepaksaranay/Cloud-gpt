"""FastAPI service that answers physics questions using Wikipedia (Wikimedia) as its source."""

from __future__ import annotations

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from cloud_gpt.physics_api.physics import is_physics_question
from cloud_gpt.physics_api.wikimedia import fetch_answer

app = FastAPI(title="cloud-gpt physics API", version="0.1.0")


class QuestionRequest(BaseModel):
    question: str


class Answer(BaseModel):
    title: str
    summary: str
    url: str


class QuestionResponse(BaseModel):
    question: str
    answer: Answer


@app.get("/")
def root() -> dict:
    return {
        "name": "cloud-gpt physics API",
        "description": "Answers physics questions using Wikipedia (Wikimedia) as its source.",
        "endpoints": {
            "POST /ask": "body: {\"question\": \"...\"} -> answer sourced from Wikipedia",
            "GET /health": "liveness check",
            "GET /docs": "interactive API documentation",
        },
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ask", response_model=QuestionResponse)
def ask(request: QuestionRequest) -> QuestionResponse:
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question must not be empty.")
    if not is_physics_question(question):
        raise HTTPException(status_code=422, detail="This API only answers physics questions.")

    with httpx.Client(timeout=10.0) as client:
        result = fetch_answer(question, client=client)

    if result is None:
        raise HTTPException(status_code=404, detail="No matching Wikipedia article found.")

    return QuestionResponse(
        question=question,
        answer=Answer(title=result["title"], summary=result["extract"], url=result["url"]),
    )


def main() -> None:
    import uvicorn

    uvicorn.run("cloud_gpt.physics_api.app:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
