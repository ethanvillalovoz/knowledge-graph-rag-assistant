export type MessageRole = "user" | "assistant";

export type ChatMessage = {
  id: string;
  role: MessageRole;
  content: string;
};

export type StepStatus = "pending" | "active" | "complete" | "error";

export type RetrievalStep = {
  id: "query" | "graph" | "vector" | "answer";
  label: string;
  status: StepStatus;
  detail?: string;
};

export type ResearchSource = {
  id: string;
  title: string;
  kind: "Knowledge graph" | "Vector index";
  excerpt: string;
  score?: number;
};

export type ResearchResult = {
  answer: string;
  sources: ResearchSource[];
  steps: RetrievalStep[];
};
