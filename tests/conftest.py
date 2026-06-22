import pytest

from backend.app.routers import dbpedia_query_router


class _FakeDbpediaResult:
    def __init__(self, query_text):
        self.query_text = query_text

    def convert(self):
        if "NonExistentEntityXYZ" in self.query_text:
            bindings = []
        else:
            bindings = [
                {
                    "abstract": {
                        "type": "literal",
                        "xml:lang": "en",
                        "value": "Albert Einstein was a German-born theoretical physicist.",
                    }
                }
            ]

        return {"results": {"bindings": bindings}}


class _FakeDbpediaClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.query_text = ""

    def setReturnFormat(self, return_format):
        self.return_format = return_format

    def setQuery(self, query_text):
        self.query_text = query_text

    def query(self):
        return _FakeDbpediaResult(self.query_text)


@pytest.fixture
def mock_dbpedia(monkeypatch):
    monkeypatch.setattr(dbpedia_query_router, "SPARQLWrapper", _FakeDbpediaClient)
