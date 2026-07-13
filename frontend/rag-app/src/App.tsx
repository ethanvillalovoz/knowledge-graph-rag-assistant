import { FormEvent, useMemo, useRef, useState } from "react";

import { isDemoMode, runResearch } from "./api/research";
import { Composer } from "./components/Composer";
import { Conversation } from "./components/Conversation";
import { EvidencePanel } from "./components/EvidencePanel";
import { GraphCanvas } from "./components/GraphCanvas";
import type { ChatMessage, ResearchSource, RetrievalStep } from "./types";
import "./App.css";

const SUGGESTIONS = [
  "How does retrieval-augmented generation reduce hallucinations?",
  "Compare vector search with knowledge-graph retrieval.",
  "What makes a useful semantic embedding?",
];

function createMessage(role: ChatMessage["role"], content: string): ChatMessage {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    role,
    content,
  };
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [query, setQuery] = useState("");
  const [sources, setSources] = useState<ResearchSource[]>([]);
  const [steps, setSteps] = useState<RetrievalStep[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestId = useRef(0);

  const modeLabel = useMemo(
    () => (isDemoMode ? "Demo dataset" : "Connected to API"),
    [],
  );

  async function submitQuery(nextQuery: string) {
    const normalizedQuery = nextQuery.trim();
    if (!normalizedQuery || isLoading) return;

    const activeRequest = ++requestId.current;
    setMessages((current) => [
      ...current,
      createMessage("user", normalizedQuery),
    ]);
    setQuery("");
    setError(null);
    setSources([]);
    setSteps([
      { id: "query", label: "Understand query", status: "active" },
      { id: "graph", label: "Query knowledge graph", status: "pending" },
      { id: "vector", label: "Retrieve semantic context", status: "pending" },
      { id: "answer", label: "Synthesize answer", status: "pending" },
    ]);
    setIsLoading(true);

    try {
      const result = await runResearch(normalizedQuery, (nextSteps) => {
        if (requestId.current === activeRequest) setSteps(nextSteps);
      });

      if (requestId.current !== activeRequest) return;
      setMessages((current) => [
        ...current,
        createMessage("assistant", result.answer),
      ]);
      setSources(result.sources);
      setSteps(result.steps);
    } catch (requestError) {
      if (requestId.current !== activeRequest) return;
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The research pipeline could not complete this request.",
      );
      setSteps((current) =>
        current.map((step) =>
          step.status === "active" ? { ...step, status: "error" } : step,
        ),
      );
    } finally {
      if (requestId.current === activeRequest) setIsLoading(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void submitQuery(query);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Knowledge Graph RAG home">
          <span className="brand-network" aria-hidden="true"><i /><i /><i /></span>
          <span>
            <strong>Knowledge Graph RAG</strong>
            <small>Traceable retrieval workspace</small>
          </span>
        </a>
        <div className="topbar-actions">
          <span className="mode-indicator">
            <span aria-hidden="true" />
            {modeLabel}
          </span>
          <a
            className="repository-link"
            href="https://github.com/ethanvillalovoz/knowledge-graph-rag-assistant"
            target="_blank"
            rel="noreferrer"
          >
            Repository
          </a>
        </div>
      </header>

      <main className="workspace">
        <section className="conversation-region" aria-label="Research conversation">
          <Conversation
            messages={messages}
            suggestions={SUGGESTIONS}
            isLoading={isLoading}
            error={error}
            onSuggestion={submitQuery}
          />
          <Composer
            value={query}
            isLoading={isLoading}
            onChange={setQuery}
            onSubmit={handleSubmit}
          />
        </section>

        <div className="analysis-region">
          <GraphCanvas steps={steps} sources={sources} />
          <EvidencePanel steps={steps} sources={sources} />
        </div>
      </main>

      {isDemoMode && (
        <p className="demo-disclosure">
          Demo mode uses deterministic sample evidence. Configure
          <code> VITE_API_BASE_URL </code> to run the full pipeline.
        </p>
      )}
    </div>
  );
}

export default App;
