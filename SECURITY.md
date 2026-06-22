# Security

## Reporting

If you find a security issue, please open a private security advisory on GitHub when available, or contact the repository maintainer directly.

Please do not publish working exploits, API keys, or sensitive runtime details in public issues.

## Supported Status

This repository is a maintained public fork of a student capstone prototype. Security updates are best-effort and focused on dependency hygiene, secret handling, and safe public documentation.

## Secret Handling

The app expects an OpenAI API key through `OPENAI_API_KEY`. Keep keys in a local `.env` file or environment variable and never commit them to the repository.
