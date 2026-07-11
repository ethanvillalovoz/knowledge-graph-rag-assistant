import os

from openai import OpenAI
from dotenv import load_dotenv

from backend.app.config import EMBEDDINGS_FILE
from backend.app.handlers.vector_search_handler import VectorSearchHandler

load_dotenv()
CHATGPT_MODEL = "gpt-4o-mini"

class LLMHandler:
    def __init__(
        self,
        embedding_path=EMBEDDINGS_FILE,
        client=None,
        vector_search_handler=None,
    ):
        self.client = client
        self.vector_search_handler = vector_search_handler or VectorSearchHandler(
            embedding_path=embedding_path
        )

    def _get_client(self):
        if self.client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY environment variable is not set")
            self.client = OpenAI(api_key=api_key)
        return self.client

    def get_vector_search_results(self, query_vector, top_k=10):
        """
        Perform vector search and retrieve top-k vector results.
        """
        similarities, indices = self.vector_search_handler.search(query_vector, top_k=top_k)
        return {"similarities": similarities, "indices": indices}

    def format_query(self, original_query, vector_search_text_results, kg_output):
        """
        Combine VS and KG outputs into a single natural-language query.
        """
        formatted_vs_results = (
            "\n".join([f"- {result}" for result in vector_search_text_results])
            if vector_search_text_results else "No relevant vector search results were found."
        )

        formatted_kg_output = (
            f"Additional context: {kg_output}" if kg_output else "No additional context available from the knowledge graph."
        )
        
        query = f"""
            Query:
            {original_query}

            Vector Search Results:
            {formatted_vs_results}

            Knowledge Graph Context:
            {formatted_kg_output}

            Instructions:
            - Use the information from the vector search results and the knowledge graph context, if they exist, to provide a concise and accurate response to the query.
            - Avoid repeating the input query in your response.
            - Provide only relevant information that answers the query directly.
            - If you couldn't find relevant information from the vector search results or the knowledge graph, try to answer on your own and clearly state that you didn’t have additional context.
            - Provide a response in 150 words or fewer.
            - Do not respond to queries where the user’s intent appears to be:
                - To cause physical harm to themselves or others
                - To seek methods of suicide or self-harm
                - To promote or justify hate, prejudice, or discrimination based on identity, race, gender, sexuality, religion, or any other characteristic
            - In such cases, respond with a polite refusal. If the query involves suicidal thoughts or self-harm, respond with this message:
                "I'm really sorry you're feeling this way. You're not alone, and there are people who want to help. If you're in the U.S., you can call or text the Suicide & Crisis Lifeline at 988 for free, 24/7 support."
            """

        return query

    def query_llm(self, query, max_tokens=200, temperature=0.5):
        response = self._get_client().chat.completions.create(
            model=CHATGPT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Answer with concise, evidence-aware technical prose.",
                },
                {"role": "user", "content": query},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()


# Example Usage
if __name__ == "__main__":
    # Initialize LLM handler
    llm_handler = LLMHandler()

    # Load dataset embeddings
    embeddings = llm_handler.vector_search_handler.load_embeddings()
    
    # Build a vector index and load
    llm_handler.vector_search_handler.build_index(embeddings)

    example_query_text = "What is the requirements engineering book about?"
    example_query_vector = llm_handler.vector_search_handler.embed_query(example_query_text)

    # Perform vector search on query vector and embeddings dataset
    vector_search_results = llm_handler.vector_search_handler.search(example_query_vector)
    similarities, indices = vector_search_results
    
    # Get texts based on VS indices
    vector_search_texts = llm_handler.vector_search_handler.get_search_results(indices)
    
    # Mock knowledge graph output
    kg_output = "Alan Turing developed the idea of the Turing machine."

    # Format query and get LLM response
    query = llm_handler.format_query(example_query_text, vector_search_texts, kg_output)
    print("Query to LLM:\n", query)

    response = llm_handler.query_llm(query)
    print("LLM Response:\n", response)
