# CLI Search Bot

A simple command-line search bot that answers questions based on web search results.

## Installation

1. Clone this repository
2. Install the package using pip:

```bash
pip install -e .
```

## Usage

```bash
answer "What is the capital of France?"
```

The bot will search the web for information about your question and provide an answer based on the search results.

## Notes

This implementation uses a simple web scraper approach. For a production-ready application, consider:

1. Using an official search API (Google, Bing, DuckDuckGo)
2. Implementing rate limiting and caching
3. Adding more robust error handling

## License

MIT
