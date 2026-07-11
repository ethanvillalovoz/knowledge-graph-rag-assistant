import type { ResearchSource, RetrievalStep } from "../types";

type EvidencePanelProps = {
  steps: RetrievalStep[];
  sources: ResearchSource[];
};

export function EvidencePanel({ steps, sources }: EvidencePanelProps) {
  return (
    <aside className="evidence-panel" aria-label="Retrieved evidence">
      <div className="panel-heading">
        <span>Evidence</span>
        <small>{sources.length ? `${sources.length} sources` : "Awaiting query"}</small>
      </div>

      <section className="trace-section" aria-labelledby="trace-title">
        <h2 id="trace-title">Retrieval trace</h2>
        {steps.length ? (
          <ol className="trace-list">
            {steps.map((step, index) => (
              <li data-status={step.status} key={step.id}>
                <span className="trace-number">{String(index + 1).padStart(2, "0")}</span>
                <span>
                  <strong>{step.label}</strong>
                  {step.detail && <small>{step.detail}</small>}
                </span>
              </li>
            ))}
          </ol>
        ) : (
          <p className="panel-empty">
            Run a question to inspect each stage of the retrieval pipeline.
          </p>
        )}
      </section>

      <section className="source-section" aria-labelledby="source-title">
        <h2 id="source-title">Source context</h2>
        {sources.length ? (
          <ol className="source-list">
            {sources.map((source) => (
              <li key={source.id}>
                <div>
                  <span className="source-kind">{source.kind}</span>
                  {typeof source.score === "number" && (
                    <span className="source-score">
                      {Math.round(source.score * 100)}% match
                    </span>
                  )}
                </div>
                <strong>{source.title}</strong>
                <p>{source.excerpt}</p>
              </li>
            ))}
          </ol>
        ) : (
          <p className="panel-empty">
            Retrieved passages and graph entities will appear here.
          </p>
        )}
      </section>
    </aside>
  );
}
