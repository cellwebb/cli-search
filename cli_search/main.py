"""CLI search bot that processes questions and provides answers using LlamaIndex."""

import argparse
import logging
import os
import sys

from llama_index.core import Settings
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.readers.web import SimpleWebPageReader

DEFAULT_LOG_LEVEL = "WARNING"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(
    level=DEFAULT_LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


def search_and_answer(question: str) -> str:
    """Search the web and generate an answer for the given question using LlamaIndex."""
    if not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not found in environment variables.")
        return "Please set your OPENAI_API_KEY environment variable to use this tool."

    logger.info(f"Processing question: {question}")

    try:
        # Configure LlamaIndex settings
        Settings.llm = OpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
        Settings.node_parser = SentenceSplitter(chunk_size=1024)

        # Search web for relevant content
        logger.info("Searching the web...")
        search_results = SimpleWebPageReader(search_kwargs={"query": question, "num_results": 3}).load_data()

        logger.info(f"Found {len(search_results)} search results")

        # Create index from search results
        index = VectorStoreIndex.from_documents(search_results)

        # Create query engine with citations
        query_engine = CitationQueryEngine.from_args(
            index,
            similarity_top_k=3,
            include_text=False,
        )

        # Generate answer with citations
        logger.info("Generating answer...")
        response = query_engine.query(question)

        # Format the response with sources
        answer = f"{response.response}\n\nSources:\n"
        for i, source_node in enumerate(response.source_nodes, 1):
            source = source_node.node.metadata.get("url", "Unknown source")
            answer += f"{i}. {source}\n"

        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return f"I encountered an error while processing your question: {str(e)}"


def main() -> None:
    """Process command line arguments and execute the search bot."""
    parser = argparse.ArgumentParser(description="CLI Search Bot using LlamaIndex")
    parser.add_argument("question", nargs="+", help="The question to answer")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=DEFAULT_LOG_LEVEL,
        help=f"Set the logging level (default: {DEFAULT_LOG_LEVEL})",
    )

    args = parser.parse_args()
    question = " ".join(args.question)

    # Set the logging level
    log_level = getattr(logging, args.log_level)
    logger.setLevel(log_level)
    logging.getLogger().setLevel(log_level)

    # Process the question and print the answer
    answer = search_and_answer(question)
    print(answer)


if __name__ == "__main__":
    main()
