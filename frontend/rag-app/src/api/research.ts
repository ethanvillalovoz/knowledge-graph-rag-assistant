import type {
  ResearchResult,
  ResearchSource,
  RetrievalStep,
} from "../types";
import { createDemoResult } from "../data/demo";

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = (configuredBaseUrl || "http://localhost:8000").replace(
  /\/$/,
  "",
);

export const isDemoMode =
  import.meta.env.VITE_DEMO_MODE === "true" || !configuredBaseUrl;

type NlpResponse = {
  tokens: string[];
  entities: Array<{ text: string; label: string }>;
  is_harmful: boolean;
  sparql_query: string;
};

type VectorResponse = {
  results: Array<{ text: string; similarity: number }>;
};

async function requestJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Request failed (${response.status}) while calling ${path}.`);
  }

  return (await response.json()) as T;
}

function setStep(
  steps: RetrievalStep[],
  id: RetrievalStep["id"],
  detail: string,
): RetrievalStep[] {
  const order: RetrievalStep["id"][] = ["query", "graph", "vector", "answer"];
  const activeIndex = order.indexOf(id);
  return steps.map((step) => {
    const stepIndex = order.indexOf(step.id);
    if (step.id === id) return { ...step, status: "active", detail };
    if (stepIndex < activeIndex) return { ...step, status: "complete" };
    return step;
  });
}

export async function runResearch(
  query: string,
  onProgress: (steps: RetrievalStep[]) => void,
): Promise<ResearchResult> {
  const initialSteps: RetrievalStep[] = [
    { id: "query", label: "Understand query", status: "active" },
    { id: "graph", label: "Query knowledge graph", status: "pending" },
    { id: "vector", label: "Retrieve semantic context", status: "pending" },
    { id: "answer", label: "Synthesize answer", status: "pending" },
  ];

  if (isDemoMode) return createDemoResult(query, initialSteps, onProgress);

  const nlp = await requestJson<NlpResponse>("/nlp/process_query", { query });
  let steps = setStep(
    initialSteps,
    "graph",
    nlp.entities.length
      ? `${nlp.entities.length} named entities found`
      : "No named entities required",
  );
  onProgress(steps);

  let graphExcerpt = "No structured context returned.";
  if (nlp.sparql_query) {
    const graph = await requestJson<{
      results?: { bindings?: Array<{ abstract?: { value?: string } }> };
    }>("/dbpedia/querykg", { query: nlp.sparql_query });
    graphExcerpt =
      graph.results?.bindings?.[0]?.abstract?.value || graphExcerpt;
  }

  steps = setStep(steps, "vector", "Searching Wikipedia embeddings");
  onProgress(steps);
  const vector = await requestJson<VectorResponse>("/vector_search/search", {
    query_text: query,
  });
  const vectorTexts = vector.results.map((result) => result.text);

  steps = setStep(steps, "answer", "Grounding answer in retrieved evidence");
  onProgress(steps);
  const answer = await requestJson<{ response: string }>("/nlp/llm_response", {
    query,
    vector_search_results: vectorTexts,
    kg_results: graphExcerpt,
  });

  const sources: ResearchSource[] = [
    {
      id: "graph-1",
      title: "DBpedia entity context",
      kind: "Knowledge graph",
      excerpt: graphExcerpt,
    },
    ...vector.results.slice(0, 3).map((result, index) => ({
      id: `vector-${index}`,
      title: `Wikipedia passage ${index + 1}`,
      kind: "Vector index" as const,
      excerpt: result.text,
      score: result.similarity,
    })),
  ];

  return {
    answer: answer.response,
    sources,
    steps: steps.map((step) => ({ ...step, status: "complete" })),
  };
}
