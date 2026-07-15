import {
  Background,
  BackgroundVariant,
  MarkerType,
  Position,
  ReactFlow,
  type Edge,
  type Node,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import type { ResearchSource, RetrievalStep } from "../types";

type GraphCanvasProps = {
  onSourceSelect: (sourceId: string) => void;
  selectedSourceId: string | null;
  steps: RetrievalStep[];
  sources: ResearchSource[];
};

const fallbackSources = [
  { id: "graph", label: "Knowledge graph", detail: "entities + relations" },
  { id: "vector", label: "Vector index", detail: "semantic passages" },
  { id: "answer-evidence", label: "Source context", detail: "ranked evidence" },
];

function nodeLabel(index: string, label: string, detail: string) {
  return (
    <span className="flow-node-label">
      <span>{index}</span>
      <strong>{label}</strong>
      <small>{detail}</small>
    </span>
  );
}

export function GraphCanvas({
  onSourceSelect,
  selectedSourceId,
  steps,
  sources,
}: GraphCanvasProps) {
  const evidence = sources.length ? sources.slice(0, 3) : fallbackSources;
  const activeStep = steps.find((step) => step.status === "active");

  const nodes: Node[] = [
    {
      id: "query",
      className: "flow-node query-flow-node",
      data: { label: nodeLabel("Q", "Question", "natural language") },
      position: { x: 20, y: 116 },
      sourcePosition: Position.Right,
      selectable: false,
    },
    ...evidence.map((source, index) => {
      const detail = "kind" in source ? source.kind : source.detail;
      const score = "score" in source ? source.score : undefined;
      return {
        id: source.id,
        className: `flow-node source-flow-node source-flow-node-${index + 1}${selectedSourceId === source.id ? " is-selected" : ""}`,
        data: {
          label: nodeLabel(
            String(index + 1).padStart(2, "0"),
            "title" in source ? source.title : source.label,
            `${detail}${typeof score === "number" ? ` / ${Math.round(score * 100)}%` : ""}`,
          ),
        },
        position: { x: 250, y: 20 + index * 96 },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
        selectable: sources.length > 0,
      };
    }),
    {
      id: "answer",
      className: "flow-node answer-flow-node",
      data: { label: nodeLabel("A", "Answer", "source constrained") },
      position: { x: 540, y: 116 },
      targetPosition: Position.Left,
      selectable: false,
    },
  ];

  const edges: Edge[] = evidence.flatMap((source, index) => [
    {
      id: `query-${source.id}`,
      source: "query",
      target: source.id,
      type: "smoothstep",
      animated: sources.length > 0,
      className: "retrieval-edge",
    },
    {
      id: `${source.id}-answer`,
      source: source.id,
      target: "answer",
      type: "smoothstep",
      animated: sources.length > 0,
      className: "retrieval-edge",
      markerEnd: { type: MarkerType.ArrowClosed },
    },
  ]);

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
        <ReactFlow
          edges={edges}
          fitView
          fitViewOptions={{ padding: 0.13 }}
          minZoom={0.72}
          maxZoom={1.45}
          nodes={nodes}
          nodesConnectable={false}
          nodesDraggable={false}
          onNodeClick={(_, node) => {
            if (sources.some((source) => source.id === node.id)) onSourceSelect(node.id);
          }}
          panOnDrag
          preventScrolling={false}
          proOptions={{ hideAttribution: true }}
          zoomOnDoubleClick={false}
        >
          <Background color="#c8c5bd" gap={18} size={1} variant={BackgroundVariant.Dots} />
        </ReactFlow>
      </div>
    </section>
  );
}
