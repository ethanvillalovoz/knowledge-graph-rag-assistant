import pytest
import warnings
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.routers.nlp_router import generate_sparql_query

warnings.filterwarnings("ignore", category=DeprecationWarning)
client = TestClient(app)


@pytest.fixture
def test_data():
    return {
        "query": "Tell me about Albert Einstein",
        "expected_entity": "Albert Einstein",
        "harmful_query": "I want to destroy everything",
        "abstract": "Albert Einstein (/ˈaɪnstaɪn/ EYEN-styne; German: [ˈalbɛʁt ˈʔaɪnʃtaɪn]; 14 March 1879 – 18 April 1955) was a German-born theoretical physicist, widely acknowledged to be one of the greatest and most influential physicists of all time. Einstein is best known for developing the theory of relativity, but he also made important contributions to the development of the theory of quantum mechanics. Relativity and quantum mechanics are the two pillars of modern physics. His mass–energy equivalence formula E = mc2, which arises from relativity theory, has been dubbed \"the world's most famous equation\". His work is also known for its influence on the philosophy of science. He received the 1921 Nobel Prize in Physics \"for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect\", a pivotal step in the development of quantum theory. His intellectual achievements and originality resulted in \"Einstein\" becoming synonymous with \"genius\". In 1905, a year sometimes described as his annus mirabilis ('miracle year'), Einstein published four groundbreaking papers. These outlined the theory of the photoelectric effect, explained Brownian motion, introduced special relativity, and demonstrated mass-energy equivalence. Einstein thought that the laws of classical mechanics could no longer be reconciled with those of the electromagnetic field, which led him to develop his special theory of relativity. He then extended the theory to gravitational fields; he published a paper on general relativity in 1916, introducing his theory of gravitation. In 1917, he applied the general theory of relativity to model the structure of the universe. He continued to deal with problems of statistical mechanics and quantum theory, which led to his explanations of particle theory and the motion of molecules. He also investigated the thermal properties of light and the quantum theory of radiation, which laid the foundation of the photon theory of light. However, for much of the later part of his career, he worked on two ultimately unsuccessful endeavors. First, despite his great contributions to quantum mechanics, he opposed what it evolved into, objecting that \"God does not play dice\". Second, he attempted to devise a unified field theory by generalizing his geometric theory of gravitation to include electromagnetism. As a result, he became increasingly isolated from the mainstream of modern physics. Einstein was born in the German Empire, but moved to Switzerland in 1895, forsaking his German citizenship(as a subject of the Kingdom of Württemberg) the following year. In 1897, at the age of 17, he enrolled in the mathematics and physics teaching diploma program at the Swiss Federal polytechnic school in Zürich, graduating in 1900. In 1901, he acquired Swiss citizenship, which he kept for the rest of his life, and in 1903 he secured a permanent position at the Swiss Patent Office in Bern. In 1905, he was awarded a PhD by the University of Zurich. In 1914, Einstein moved to Berlin in order to join the Prussian Academy of Sciences and the Humboldt University of Berlin. In 1917, Einstein became director of the Kaiser Wilhelm Institute for Physics; he also became a German citizen again, this time Prussian. In 1933, while Einstein was visiting the United States, Adolf Hitler came to power in Germany. Einstein, as a Jew, objected to the policies of the newly elected Nazi government; he settled in the United States and became an American citizen in 1940. On the eve of World War II, he endorsed a letter to President Franklin D. Roosevelt alerting him to the potential German nuclear weapons program and recommending that the US begin similar research. Einstein supported the Allies but generally denounced the idea of nuclear weapons."
    }


def test_process_query_tokenize(test_data):
    response = client.post("/nlp/process_query",
                           json={"query": test_data["query"]})
    assert response.status_code == 200
    data = response.json()

    # Test tokens
    tokens = data["tokens"]
    assert "Albert" in tokens and "Einstein" in tokens


def test_process_query_extract_entities(test_data):
    response = client.post("/nlp/process_query",
                           json={"query": test_data["query"]})
    assert response.status_code == 200
    data = response.json()

    # Test entities
    entities = data["entities"]
    assert any(ent["text"] == test_data["expected_entity"] for ent in entities)


def test_process_query_detect_harmful_intent(test_data):
    # Test non-harmful intent
    response = client.post("/nlp/process_query",
                           json={"query": test_data["query"]})
    data = response.json()
    assert not data["is_harmful"]

    # Test harmful intent
    harmful_response = client.post(
        "/nlp/process_query", json={"query": test_data["harmful_query"]})
    harmful_data = harmful_response.json()
    assert harmful_data["is_harmful"]


def test_normal_nlp_to_dbpedia(test_data, mock_dbpedia):
    doc = client.post("/nlp/process_query",
                      json={"query": test_data["query"]}).json()
    entities = doc["entities"]
    sparql_query = generate_sparql_query(entities)

    assert sparql_query is not None
    assert test_data["expected_entity"] in sparql_query

    response = client.post("/dbpedia/querykg",
                           json={"query": sparql_query})
    assert response.status_code == 200
    result = response.json()

    assert "results" in result, "Expected 'results' key in the DBpedia response"
    assert len(result["results"]["bindings"]
               ) > 0, "Expected non-empty bindings from DBpedia"
    abstract_value = result["results"]["bindings"][0]["abstract"]["value"]
    assert "Albert Einstein" in abstract_value
