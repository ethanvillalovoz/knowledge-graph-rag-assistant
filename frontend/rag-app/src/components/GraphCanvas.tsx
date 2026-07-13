import type { ResearchSource, RetrievalStep } from "../types";

type GraphCanvasProps = {
  steps: RetrievalStep[];
  sources: ResearchSource[];
};

type CanvasNode = {
  id: string;
  label: string;
  detail: string;
  index: number;
  score?: number;
};

const fallbackNodes = [
  { id: "graph", label: "Knowledge graph", detail: "entities + relations" },
  { id: "vector", label: "Vector index", detail: "semantic passages" },
  { id: "answer", label: "Grounded answer", detail: "constrained synthesis" },
];

export function GraphCanvas({ steps, sources }: GraphCanvasProps) {
  const nodes: CanvasNode[] = sources.length
    ? sources.slice(0, 3).map((source, index) => ({
        id: source.id,
        label: source.title,
        detail: source.kind,
        score: source.score,
        index,
      }))
    : fallbackNodes.map((node, index) => ({ ...node, index }));

  const activeStep = steps.find((step) => step.status === "active");

  return (
    <section className="graph-panel" aria-labelledby="graph-title">
      <header className="graph-heading">
        <div>
          <span>Retrieval map</span>
          <h2 id="graph-title">Evidence topology</h2>
        </div>
        <small>{activeStep?.label ?? (sources.length ? "Trace complete" : "Awaiting query")}</small>
      </header>

      <div className={`graph-map${sources.length ? " has-results" : ""}`}>
        <svg aria-hidden="true" viewBox="0 0 720 300" preserveAspectRatio="none">
          <path d="M118 148 C220 148 220 62 332 62" />
          <path d="M118 148 C230 148 230 150 332 150" />
          <path d="M118 148 C220 148 220 238 332 238" />
          <path d="M466 62 C548 62 548 148 620 148" />
          <path d="M466 150 C548 150 548 148 620 148" />
          <path d="M466 238 C548 238 548 148 620 148" />
        </svg>

        <div className="graph-node query-node">
          <span>Q</span>
          <strong>Question</strong>
          <small>natural language</small>
        </div>

        {nodes.map((node) => (
          <div className={`graph-node source-node node-${node.index + 1}`} key={node.id}>
            <span>{String(node.index + 1).padStart(2, "0")}</span>
            <strong>{node.label}</strong>
            <small>{node.detail}{typeof node.score === "number" ? ` / ${Math.round(node.score * 100)}%` : ""}</small>
          </div>
        ))}

        <div className="graph-node answer-node">
          <span>A</span>
          <strong>Answer</strong>
          <small>source constrained</small>
        </div>
      </div>
    </section>
  );
}
