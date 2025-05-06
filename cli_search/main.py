"""CLI search bot that processes questions and provides answers using LlamaIndex."""

import logging
import os
import sys
from typing import List, Set

import click
import requests
import urllib3
from bs4 import BeautifulSoup
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.llms.openai import OpenAI

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_LOG_LEVEL = "WARNING"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(
    level=DEFAULT_LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def search_web(query: str, num_results: int = 3) -> List[str]:
    """Perform a web search and return a list of URLs."""
    search_url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # noqa: E501
    }

    try:
        response = requests.get(search_url, params=params, headers=headers, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select(".result"):
            url = None
            if link := result.select_one("a.result__a"):
                url = link.get("href")
            elif link := result.select_one("a.result__url"):
                url = link.get("href")

            if url and len(results) < num_results and url.startswith("http"):
                results.append(url)

        logger.info(f"Found {len(results)} search results")
        return results
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return []


def fetch_content_and_create_document(url: str) -> Document:
    """Fetch content from a URL and create a Document object."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # noqa: E501
        }
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "meta", "link", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())
        text = text[:10000]

        return Document(text=text, metadata={"url": url})
    except Exception as e:
        logger.warning(f"Error fetching {url}: {str(e)}")
        return Document(text=f"Failed to fetch content from {url}", metadata={"url": url})


def search_and_answer(question: str) -> str:
    """Search the web and generate an answer for the given question using LlamaIndex."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not found in environment variables.")
        return "Please set your OPENAI_API_KEY environment variable to use this tool."

    logger.info(f"Processing question: {question}")

    try:
        Settings.llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
        Settings.node_parser = SentenceSplitter(chunk_size=1024)

        logger.info("Searching the web...")
        urls = search_web(question, num_results=3)

        if not urls:
            return "I couldn't find any search results for your question."

        logger.info(f"Found URLs: {urls}")

        documents = [fetch_content_and_create_document(url) for url in urls]
        logger.info(f"Created {len(documents)} documents")

        index = VectorStoreIndex.from_documents(documents)

        query_engine = CitationQueryEngine.from_args(
            index,
            similarity_top_k=3,
            include_text=False,
        )

        logger.info("Generating answer...")
        response = query_engine.query(question)

        answer = f"{response.response}\n\nSources:\n"

        unique_sources: Set[str] = set()
        for source_node in response.source_nodes:
            source = source_node.node.metadata.get("url", "Unknown source")
            unique_sources.add(source)

        for i, source in enumerate(unique_sources, 1):
            answer += f"{i}. {source}\n"

        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return f"I encountered an error while processing your question: {str(e)}"


@click.command()
@click.argument("question", nargs=-1, required=True)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    default=DEFAULT_LOG_LEVEL,
    help=f"Set the logging level (default: {DEFAULT_LOG_LEVEL})",
)
def main(question: tuple[str, ...], log_level: str) -> None:
    """CLI Search Bot using LlamaIndex. Ask a question to get an answer from web search."""
    log_level_value = getattr(logging, log_level.upper())
    logger.setLevel(log_level_value)
    logging.getLogger().setLevel(log_level_value)

    full_question = " ".join(question)
    answer = search_and_answer(full_question)
    click.echo(answer)


if __name__ == "__main__":
    main()
