import wikipedia
import re
from typing import Optional, Tuple


def get_wikipedia_page_as_markdown(query: str) -> Optional[Tuple[str, str]]:
    """
    Fetches a Wikipedia page based on the query and returns its content
    formatted as Markdown.

    Args:
        query: The search query for the Wikipedia page.

    Returns:
        A tuple containing the page URL and the content as a Markdown string,
        or None if the page cannot be fetched or processed.
    """
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            print(f"No Wikipedia pages found for query: {query}")
            return None

        # Take the first search result
        page_title = search_results[0]

        # Attempt to get the page, disable auto_suggest to be explicit
        page = wikipedia.page(page_title, auto_suggest=False)

    except wikipedia.exceptions.DisambiguationError as e:
        # This might happen if the query itself is ambiguous
        print(f"Disambiguation error for query '{query}'. Options: {e.options}")
        return None
    except wikipedia.exceptions.PageError:
        # This might happen if the title from search results doesn't resolve correctly
        print(
            f"PageError: Could not find a page for '{page_title}' derived from query '{query}'."
        )
        return None
    except Exception as e:  # Catch other potential errors (network, etc.)
        print(f"An unexpected error occurred during Wikipedia fetch: {e}")
        return None

    # Start markdown with the definitive page title
    markdown_text = f"# {page.title}\n\n"

    content = page.content

    # Replace Wikipedia heading styles with Markdown heading styles
    content = re.sub(r"=== ([^=]+) ===", r"### \1", content)
    content = re.sub(r"== ([^=]+) ==", r"## \1", content)

    # Append the formatted content
    markdown_text += content

    return (page.url, markdown_text)
