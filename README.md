# ACME10-HE-RAGApp

## Project summary

### One-sentence description of the project

We developed a RAG (Retrieval-Augmented Generation) application for [HackerEarth](https://www.hackerearth.com/) that utilizes vector search, knowledge graphs, and an LLM to answer questions and generate content from a knowledge base of more than 10,000 Wikipedia articles.

### Project Demo

[Demo link](https://www.youtube.com/watch?v=YWdR3FAdq1o)

### Additional information about the project

- **Client:**
  - [HackerEarth](https://www.hackerearth.com/), based in San Francisco, offers enterprise software for technical hiring. Organizations use their platform to create coding assessments, conduct remote video interviews, and ensure unbiased, AI-powered evaluation of candidates
- **RAG application:**
  - Retrieval Augmented Generation (RAG) means supplying a Large Language Model (LLM) with the appropriate processed data from an outside knowledge base. We will use Knowledge Graphs and vector search to optimize data retrieval
- **Knowledge Graph used:**
  - DBpedia
- **Vector Search tool used:**
  - FAISS
- **LLM used:**
  - OpenAI

## Running the Application with Docker

If you prefer to use the pre-built Docker images instead of setting up the project manually, follow these steps.

### Prerequisites

- **Install Docker Desktop:** Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- **Install Docker Compose:** Ensure you have `docker-compose` installed. You can install it via Python:

  ```bash
  pip install docker-compose
  ```

- **LLM API Key:** Ensure you have an OpenAI key 

### Running the Application

1. **Pull the Frontend Image:**

   ```bash
   docker pull ghcr.io/mollyiverson/acme10-he-ragapp-frontend:latest
   ```

2. **Pull the Backend Image:**

   ```bash
   docker pull ghcr.io/mollyiverson/acme10-he-ragapp-backend:latest
   ```

3. **Download the `docker-compose.yml` File:**

   ```bash
   curl -O https://raw.githubusercontent.com/mollyiverson/ACME10-HE-RAGApp/main/docker-compose.yml
   ```

   Or, download it manually from the repository. Keep it in the same location you used to pull the docker images.

4. **Add your OpenAI API key to the docker-compose.yml file**

5. **Start the Containers:**

   ```bash
   docker-compose up
   ```

6. **Access the Application:**
   - Open your browser and go to `http://localhost:3000`.

### Stopping and Cleaning Up

- **Shut down the application:**

  ```bash
  docker-compose down
  ```

- **Remove Docker Images (if needed):**
  The images take up more than 10 GB, so you may want to remove them after use.
  ```bash
  docker rmi ghcr.io/mollyiverson/acme10-he-ragapp-frontend:latest
  docker rmi ghcr.io/mollyiverson/acme10-he-ragapp-backend:latest
  ```

---

## Installation (For Local Development)

If you prefer to run the application locally by cloning the repository, follow the steps below.

### Prerequisites

- **Git:** Ensure that you have Git installed to clone the repository. You can install Git from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Python 3.9+:** Required to run the backend services of the RAG application
- **Node.js:** For running the frontend, you need to have Node.js installed. Get it from [here](https://nodejs.org/en/)
- **LLM API Key:** Ensure you have an OpenAI key saved in your environment

```bash
# For Linux
export OPEN_API_KEY=value
```

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/mollyiverson/ACME10-HE-RAGApp.git
   cd ACME10-HE-RAGApp
   ```
2. **Download Embeddings:** Download the required embedding files from this [Hugging Face repository](https://huggingface.co/datasets/miverson9/acme10-he-ragapp-embeddings/tree/main)
    - Place `text_embeddings.npy` in `backend/app/data_processing/embeddings_data/`
    - Place `index.faiss` in `backend/app/data_processing/vector_search_data/`

Set up two terminals.

3. **Install Backend Dependencies in terminal 1:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows: `venv\Scripts\activate`
   # On Linux: `source venv/Scripts/activate`
   cd backend
   pip install -r requirements.txt
   ```

4. **Run Backend in terminal 1:**

   ```bash
   python -m uvicorn app.main:app --reload

   """
     if you get the error: `ModuleNotFoundError: No module named 'backend'`,
     then `cd ..` into the root of the project,
     then `export PYTHONPATH=$(pwd)/backend` for macOS/Linux or `set PYTHONPATH=%cd%` for Windows.
     Then, do Step 4 again.
   """
   ```

5. **Run Frontend in terminal 2:**

    - Download [Node.js (LTS)](https://nodejs.org/en)
    ```bash
    cd frontend/rag-app
    npm install
    npm start
    ```

The application should now be running on `localhost:3000` for both frontend and backend.

6. **Run Tests:**
   ```bash
   cd ACME10-HE-RAGApp
   set PYTHONPATH=%cd%
   # On macOS/Linux: `export PYTHONPATH=$(pwd)`
   pytest -s  # -s is optional if you want print statements to show
   ```

## Functionality

The RAG application allows users to enter queries and receive accurate, context-rich responses from a combination of vector search and knowledge graphs. It uses both the large Wikipedia dataset and a custom dataset of class notes to highlight the immense potential of the RAG model.

### Walkthrough

1. Open the application in your browser
2. Input a question or query related to the Wikipedia dataset
3. The application retrieves relevant information using vector embeddings
4. The knowledge graph adds contextual insights to the response
5. The LLM generates a coherent answer based on the retrieved data

## Known Limitations

- **Vector Search Inaccuracies:** With over 10,000 articles, vector search has difficulty finding the most relevant information.
- **Error Handling with Knowledge Graph Queries:** If a SPARQL query to the knowledge graph fails, the system may return incomplete information
- **Missing Responses:** In rare cases, the system might generate an "I don't know" response when the knowledge base doesn't have enough data to provide an accurate answer

## Additional Documentation

- [Project Report](docs/project-report/RAGApp-FinalReport.pdf)
- [Project Abstract](docs/project-report/Project-Abstract.pdf)
- [Sprint reports](docs/sprint-reports/)

## License

See `LICENSE.txt`
