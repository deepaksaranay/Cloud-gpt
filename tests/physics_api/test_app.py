from fastapi.testclient import TestClient

from cloud_gpt.physics_api.app import app

client = TestClient(app)

SAMPLE_ANSWER = {
    "title": "Newton's laws of motion",
    "extract": "Newton's laws of motion are three physical laws that describe motion.",
    "url": "https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion",
}


def test_root_describes_the_api():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "cloud-gpt physics API"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_answer_for_physics_question(monkeypatch):
    monkeypatch.setattr(
        "cloud_gpt.physics_api.app.fetch_answer",
        lambda query, client=None: SAMPLE_ANSWER,
    )

    response = client.post("/ask", json={"question": "What is Newton's second law of motion?"})

    assert response.status_code == 200
    body = response.json()
    assert body["question"] == "What is Newton's second law of motion?"
    assert body["answer"] == {
        "title": SAMPLE_ANSWER["title"],
        "summary": SAMPLE_ANSWER["extract"],
        "url": SAMPLE_ANSWER["url"],
    }


def test_ask_rejects_non_physics_question():
    response = client.post("/ask", json={"question": "What is the capital of France?"})

    assert response.status_code == 422


def test_ask_rejects_empty_question():
    response = client.post("/ask", json={"question": "   "})

    assert response.status_code == 400


def test_ask_returns_404_when_no_article_found(monkeypatch):
    monkeypatch.setattr(
        "cloud_gpt.physics_api.app.fetch_answer",
        lambda query, client=None: None,
    )

    response = client.post("/ask", json={"question": "What is quantum foo bar nonsense energy?"})

    assert response.status_code == 404
