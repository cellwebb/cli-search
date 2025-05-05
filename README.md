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
2. Search the web using DuckDuckGo and fetch content from top results
3. Use OpenAI to generate a comprehensive answer based on the retrieved information

If the OPENAI_API_KEY environment variable is not set, the bot will fall back to a simple template-based response.

### Controlling Log Output

You can control the verbosity of the logs using the `--log-level` argument:

```bash
answer --log-level DEBUG "What is the capital of France?"  # Most verbose
answer --log-level INFO "What is the capital of France?"   # Default
answer --log-level WARNING "What is the capital of France?" # Less verbose
answer --log-level ERROR "What is the capital of France?"   # Errors only
```

Available log levels in order of verbosity:

- `DEBUG`: Show all details, including search results and API responses
- `INFO`: Show general progress information (default)
- `WARNING`: Show only warnings and issues
- `ERROR`: Show only errors
- `CRITICAL`: Show only critical errors

## How It Works

The CLI search bot uses:

- **OpenAI**: For generating optimal search terms and comprehensive answers
- **DuckDuckGo**: For finding relevant web pages
- **BeautifulSoup**: For parsing web content
- **Direct Content Fetching**: For retrieving full article text from top search results

This approach provides several benefits:

- Enhanced search queries through AI
- Rich context for answer generation
- Comprehensive answers synthesized from multiple sources
- Fallback mechanisms for reliability

## License

MIT
