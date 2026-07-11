import type { ResearchResult, RetrievalStep } from "../types";

const wait = (duration: number) =>
  new Promise((resolve) => window.setTimeout(resolve, duration));

function progressSteps(
  steps: RetrievalStep[],
  activeId: RetrievalStep["id"],
  detail: string,
) {
  const order = ["query", "graph", "vector", "answer"];
  const activeIndex = order.indexOf(activeId);
  return steps.map((step) => ({
    ...step,
    status:
      step.id === activeId
        ? ("active" as const)
        : order.indexOf(step.id) < activeIndex
          ? ("complete" as const)
          : step.status,
    detail: step.id === activeId ? detail : step.detail,
  }));
}

export async function createDemoResult(
  query: string,
  initialSteps: RetrievalStep[],
  onProgress: (steps: RetrievalStep[]) => void,
): Promise<ResearchResult> {
  let steps = initialSteps;
  await wait(260);
  steps = progressSteps(steps, "graph", "2 related entities found");
  onProgress(steps);
  await wait(360);
  steps = progressSteps(steps, "vector", "3 passages above similarity threshold");
  onProgress(steps);
  await wait(420);
  steps = progressSteps(steps, "answer", "Composing a grounded response");
  onProgress(steps);
  await wait(480);

  const normalized = query.toLowerCase();
  const answer = normalized.includes("vector") && normalized.includes("graph")
    ? "Vector search finds passages that are semantically similar to a question, even when the wording differs. A knowledge graph contributes explicit entities and relationships. Used together, the vector index provides broad recall while the graph adds structured context that is easier to inspect and constrain."
    : normalized.includes("hallucination")
      ? "Retrieval-augmented generation reduces unsupported answers by giving the model relevant external context at inference time. It does not eliminate hallucinations on its own: retrieval quality, source coverage, prompt construction, and whether the answer is required to stay within the evidence all remain important."
      : "A useful semantic embedding places text with similar meaning near each other in vector space. Its quality depends on the training objective, the domain of the source material, chunk boundaries, and whether the similarity metric matches the downstream retrieval task.";

  return {
    answer,
    sources: [
      {
        id: "demo-graph",
        title: "Retrieval-augmented generation",
        kind: "Knowledge graph",
        excerpt:
          "A generation pipeline can combine parametric model knowledge with information retrieved from an external corpus.",
      },
      {
        id: "demo-vector-1",
        title: "Semantic retrieval passage",
        kind: "Vector index",
        excerpt:
          "Dense retrieval represents queries and documents as vectors and ranks passages using geometric similarity.",
        score: 0.91,
      },
      {
        id: "demo-vector-2",
        title: "Knowledge graph passage",
        kind: "Vector index",
        excerpt:
          "Knowledge graphs encode entities and relationships in a structure that supports explicit traversal and queries.",
        score: 0.86,
      },
    ],
    steps: steps.map((step) => ({ ...step, status: "complete" })),
  };
}
