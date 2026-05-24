import logging
from typing import List, Dict
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """Search DuckDuckGo for policy-related information."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "link": result.get("href", ""),
                "snippet": result.get("body", "")
            })

        logger.info(f"Found {len(formatted_results)} search results for: {query}")
        return formatted_results

    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return []


def format_search_results(results: List[Dict]) -> str:
    """Format search results for LLM context."""
    if not results:
        return ""

    formatted = "### Web Search Results\n"
    for i, result in enumerate(results, 1):
        formatted += f"\n{i}. **{result['title']}**\n"
        formatted += f"   Link: {result['link']}\n"
        formatted += f"   {result['snippet'][:200]}...\n"

    return formatted


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = search_web("Pakistan education policy reform")
    for r in results:
        print(f"- {r['title']}")
        print(f"  {r['snippet'][:100]}...")
