# CLI Search Bot

A simple command-line search bot that answers questions based on web search results, using OpenAI to enhance search terms and generate responses.

## Installation

1. Clone this repository
2. Install the package using uv:

```bash
uv pip install -e .
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

```bash
answer "What is the capital of France?"
```

The bot will:

1. Use OpenAI to generate optimized search terms based on your question
2. Search the web for information using DuckDuckGo
3. Use OpenAI to generate a comprehensive answer based on the search results

If the OPENAI_API_KEY environment variable is not set, the bot will fall back to using the original question as search terms and provide a simple template-based response.

## Notes

This implementation uses a simple web scraper approach. For a production-ready application, consider:

1. Using an official search API (Google, Bing, DuckDuckGo)
2. Implementing rate limiting and caching
3. Adding more robust error handling

## License

MIT
