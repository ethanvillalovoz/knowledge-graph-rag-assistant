import { render, screen } from '@testing-library/react';
import App from './App';

test('renders chat input controls', () => {
  render(<App />);
  expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
});
