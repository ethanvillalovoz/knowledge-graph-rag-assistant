import type { ChatMessage } from "../types";

type ConversationProps = {
  messages: ChatMessage[];
  suggestions: string[];
  isLoading: boolean;
  error: string | null;
  onSuggestion: (suggestion: string) => void;
};

export function Conversation({
  messages,
  suggestions,
  isLoading,
  error,
  onSuggestion,
}: ConversationProps) {
  return (
    <div className="conversation-scroll" aria-live="polite">
      {messages.length === 0 ? (
        <div className="empty-state">
          <h1>Research query</h1>
          <p>
            Ask a technical question, then inspect the passages, graph entities,
            and retrieval stages used to answer it.
          </p>
          <div className="suggestion-list" aria-label="Suggested questions">
            {suggestions.map((suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() => onSuggestion(suggestion)}
              >
                <span>{suggestion}</span>
                <span aria-hidden="true">&#8594;</span>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <ol className="message-list">
          {messages.map((message) => (
            <li className={`message ${message.role}`} key={message.id}>
              <span className="message-role">
                {message.role === "user" ? "Question" : "Answer"}
              </span>
              <p>{message.content}</p>
            </li>
          ))}
          {isLoading && (
            <li className="message assistant loading-message">
              <span className="message-role">Answer</span>
              <span className="loading-dots" aria-label="Researching">
                <i />
                <i />
                <i />
              </span>
            </li>
          )}
        </ol>
      )}
      {error && <div className="request-error">{error}</div>}
    </div>
  );
}
