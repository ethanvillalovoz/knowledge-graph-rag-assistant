from backend.app.models.basic_query import Query
from backend.app.routers import nlp_router


class _FakeHandler:
    def __init__(self):
        self.formatted_query = None

    def format_query(self, query, vector_results, graph_results):
        self.formatted_query = (query, vector_results, graph_results)
        return "grounded prompt"

    def query_llm(self, prompt):
        assert prompt == "grounded prompt"
        return "Grounded response"


def test_llm_route_uses_the_cached_handler_for_formatting_and_generation(monkeypatch):
    handler = _FakeHandler()
    monkeypatch.setattr(nlp_router, "get_llm_handler", lambda: handler)
    query = Query(
        query="How does graph retrieval help?",
        vector_search_results=["Semantic passage"],
        kg_results="Entity relationship",
    )

    result = nlp_router.llm_respond(query)

    assert result == {"response": "Grounded response"}
    assert handler.formatted_query == (
        "How does graph retrieval help?",
        ["Semantic passage"],
        "Entity relationship",
    )
