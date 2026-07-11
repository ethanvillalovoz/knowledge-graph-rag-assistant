import type { FormEvent } from "react";

type ComposerProps = {
  value: string;
  isLoading: boolean;
  onChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export function Composer({
  value,
  isLoading,
  onChange,
  onSubmit,
}: ComposerProps) {
  return (
    <form className="composer" onSubmit={onSubmit}>
      <label htmlFor="research-query">Ask the knowledge base</label>
      <div className="composer-row">
        <textarea
          id="research-query"
          rows={2}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              event.currentTarget.form?.requestSubmit();
            }
          }}
          placeholder="Ask a technical question..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !value.trim()}>
          {isLoading ? "Working" : "Ask"}
        </button>
      </div>
      <p>Enter to submit. Shift + Enter for a new line.</p>
    </form>
  );
}
