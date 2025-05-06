# CLI Search Bot

A concise command-line search bot that answers questions based on web search results, using LlamaIndex and OpenAI to create intelligent responses with proper citations.

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

1. Search the web using DuckDuckGo for relevant pages
2. Process and extract text content from the top results
3. Index the content using LlamaIndex vector storage
4. Generate a comprehensive answer with proper citations using OpenAI's GPT-4o
5. Display deduplicated source links

If the OPENAI_API_KEY environment variable is not set, the bot will return an error message.

### Controlling Log Output

You can control the verbosity of the logs using the `--log-level` option:

```bash
answer --log-level DEBUG "What is the capital of France?"  # Most verbose
answer --log-level INFO "What is the capital of France?"   # Show progress information
answer --log-level WARNING "What is the capital of France?" # Less verbose (default)
answer --log-level ERROR "What is the capital of France?"   # Errors only
```

Available log levels in order of verbosity:

- `DEBUG`: Show all details, including search results and API responses
- `INFO`: Show general progress information
- `WARNING`: Show only warnings and issues (default)
- `ERROR`: Show only errors
- `CRITICAL`: Show only critical errors

## How It Works

The CLI search bot uses:

- **LlamaIndex**: For document processing, indexing and retrieval
- **OpenAI**: For generating comprehensive answers via GPT-4o
- **DuckDuckGo**: For finding relevant web pages
- **BeautifulSoup**: For parsing web content
- **Click**: For a modern command-line interface

This implementation is designed to be concise and efficient, with features like:

- SSL verification handling to work with a wide range of websites
- Source deduplication to avoid repetition in citations
- Error handling to gracefully manage web connectivity issues
- HTML content processing to extract meaningful text

## License

MIT
