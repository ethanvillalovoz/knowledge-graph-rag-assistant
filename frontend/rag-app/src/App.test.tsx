import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, test, vi } from "vitest";

import App from "./App";

describe("Knowledge Graph RAG workspace", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  test("renders a usable demo workspace without backend configuration", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: /research query/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/ask the knowledge base/i)).toBeInTheDocument();
    expect(screen.getByText(/demo mode uses deterministic sample evidence/i)).toBeInTheDocument();
  });

  test("runs a suggested question through the demo retrieval trace", async () => {
    vi.useFakeTimers();
    render(<App />);

    fireEvent.click(
      screen.getByRole("button", {
        name: /compare vector search with knowledge-graph retrieval/i,
      }),
    );
    await act(async () => {
      await vi.advanceTimersByTimeAsync(2_000);
    });

    expect(screen.getByText(/vector search finds passages/i)).toBeInTheDocument();
    expect(screen.getByText(/3 sources/i)).toBeInTheDocument();
  });
});
