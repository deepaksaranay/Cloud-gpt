import httpx
import pytest

from cloud_gpt.physics_api.wikimedia import fetch_answer, get_summary, search_titles

SAMPLE_TITLE = "Newton's laws of motion"
SAMPLE_EXTRACT = "Newton's laws of motion are three physical laws that describe motion."
SAMPLE_URL = "https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion"


def _handler(request: httpx.Request) -> httpx.Response:
    params = request.url.params
    if params.get("list") == "search":
        return httpx.Response(200, json={"query": {"search": [{"title": SAMPLE_TITLE}]}})
    if params.get("prop") == "extracts|info":
        return httpx.Response(
            200,
            json={
                "query": {
                    "pages": {
                        "12345": {
                            "title": SAMPLE_TITLE,
                            "extract": SAMPLE_EXTRACT,
                            "fullurl": SAMPLE_URL,
                        }
                    }
                }
            },
        )
    return httpx.Response(404)


def _empty_search_handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"query": {"search": []}})


@pytest.fixture
def mock_client():
    with httpx.Client(transport=httpx.MockTransport(_handler)) as client:
        yield client


def test_search_titles_returns_best_match(mock_client):
    assert search_titles("newton's second law", mock_client) == [SAMPLE_TITLE]


def test_get_summary_returns_title_extract_and_url(mock_client):
    summary = get_summary(SAMPLE_TITLE, mock_client)

    assert summary == {"title": SAMPLE_TITLE, "extract": SAMPLE_EXTRACT, "url": SAMPLE_URL}


def test_fetch_answer_combines_search_and_summary(mock_client):
    result = fetch_answer("what is newton's second law?", client=mock_client)

    assert result == {"title": SAMPLE_TITLE, "extract": SAMPLE_EXTRACT, "url": SAMPLE_URL}


def test_fetch_answer_returns_none_when_no_article_found():
    with httpx.Client(transport=httpx.MockTransport(_empty_search_handler)) as client:
        assert fetch_answer("asdkjaksjdalksjd nonsense query", client=client) is None
