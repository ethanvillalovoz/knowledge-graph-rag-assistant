import logging
from functools import lru_cache

import spacy
from fastapi import APIRouter, HTTPException
from backend.app.models.basic_query import Query
from backend.app.handlers.llm_handler import LLMHandler

router = APIRouter()
logger = logging.getLogger(__name__)


@lru_cache
def get_nlp():
    return spacy.load("en_core_web_sm")


@lru_cache
def get_llm_handler():
    return LLMHandler()


def detect_harmful_intent(doc):
    '''
    Detects harmful intent within a processed document by checking for keywords associated with harmful actions.
    :param doc: <spacy.tokens.Doc> Processed text document.
    :return: <bool> True if harmful intent keywords are found; False otherwise.
    '''
    harmful_keywords = ["kill", "attack", "destroy", "harm"]
    for token in doc:
        if token.lemma_.lower() in harmful_keywords:
            return True
    return False


def extract_entities(doc):
    '''
    Extracts named entities from the processed document for further use.
    :param doc: <spacy.tokens.Doc> Processed text document.
    :return: <list of dict> List of entities with 'text' and 'label' for each.
    '''
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]


def tokenize_text(doc):
    '''
    Tokenizes the document text into individual words and punctuation marks.
    :param doc: <spacy.tokens.Doc> Processed text document.
    :return: <list of str> List of token strings.
    '''

    return [token.text for token in doc]


def generate_sparql_query(entities):
    '''
    Generates a SPARQL query to retrieve abstract information for the first identified entity in the document.
    :param entities: <list of dict> List of extracted entities with 'text' and 'label'.
    :return: <str or None> SPARQL query string if entities exist, otherwise None.
    '''

    if entities:
        entity = entities[0]["text"].replace("\\", "\\\\").replace('"', '\\"')
        return f"""
        SELECT ?abstract WHERE {{
            ?subject rdfs:label "{entity}"@en .
            ?subject dbo:abstract ?abstract .
            FILTER (lang(?abstract) = 'en')
        }}
        """
    return None


@router.post("/process_query")
def process_query(query: Query):
    '''
    Processes a user query by performing various NLP tasks including tokenization, entity extraction, 
    harmful intent detection, and optionally generating a SPARQL query if entities are found.
    :param query: <Query> Pydantic model containing the user's input text as 'query'.
    :return: <dict> Dictionary with tokens, entities, harmful intent status, and a SPARQL query if applicable.
    '''

    doc = get_nlp()(query.query)
    tokens = tokenize_text(doc)
    entities = extract_entities(doc)
    is_harmful = detect_harmful_intent(doc)

    sparql_query = generate_sparql_query(entities)

    return {
        "tokens": tokens,
        "entities": entities,
        "is_harmful": is_harmful,
        "sparql_query": sparql_query
    }

@router.post("/llm_response")
def llm_respond(query: Query):
    """
    Processes an LLM response for the given query and supporting data.
    
    :param query: <Query> Pydantic model containing the user's input text as 'query'.
    :param vector_search_results: <string[]> Results from a vector search.
    :param kg_results: <string> Results from a knowledge graph query.
    :return: <string> LLM response or an error message.
    """
    try:
        # Format query and get LLM response
        formatted_query = llm_handler.format_query(query.query, query.vector_search_results, query.kg_results)
        response = get_llm_handler().query_llm(formatted_query)

        return { "response": response }

    except (ValueError, AttributeError) as exc:
        raise HTTPException(status_code=400, detail="The request could not be processed.") from exc
    except Exception as exc:
        logger.exception("LLM response generation failed")
        raise HTTPException(status_code=502, detail="Response generation is unavailable.") from exc
