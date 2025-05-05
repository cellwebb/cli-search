"""CLI search bot that processes questions and provides answers."""

import argparse
import logging
import sys
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def search_web(query: str) -> List[Dict[str, str]]:
    """Perform a web search and return relevant results."""
    logger.info(f"Searching for: {query}")

    # This is a placeholder. In a real application, you would use a search API
    # Example with DuckDuckGo (note: this is simplified and might not work without proper headers)
    search_url = "https://duckduckgo.com/html/"
    params = {"q": query}

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        # Extract search results (simplified)
        for result in soup.select(".result__body")[:5]:  # Get first 5 results
            title_element = result.select_one(".result__title")
            snippet_element = result.select_one(".result__snippet")
            link_element = result.select_one(".result__url")

            if title_element and snippet_element:
                results.append(
                    {
                        "title": title_element.get_text(strip=True),
                        "snippet": snippet_element.get_text(strip=True),
                        "url": link_element.get_text(strip=True) if link_element else "",
                    }
                )

        return results
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return []


def generate_answer(question: str, search_results: List[Dict[str, str]]) -> str:
    """Generate an answer based on the search results."""
    logger.info(f"Generating answer for: {question}")

    if not search_results:
        return "I couldn't find any relevant information to answer your question."

    # Simple answer generation
    answer = f"Based on my search for '{question}', here's what I found:\n\n"

    for i, result in enumerate(search_results, 1):
        answer += f"{i}. {result['title']}\n"
        answer += f"   {result['snippet']}\n"
        if result["url"]:
            answer += f"   Source: {result['url']}\n"
        answer += "\n"

    answer += "This information should help answer your question."
    return answer


def main() -> None:
    """Process command line arguments and execute the search bot."""
    parser = argparse.ArgumentParser(description="CLI Search Bot")
    parser.add_argument("question", nargs="+", help="The question to answer")

    args = parser.parse_args()
    question = " ".join(args.question)

    search_results = search_web(question)
    answer = generate_answer(question, search_results)

    print(answer)


if __name__ == "__main__":
    main()
