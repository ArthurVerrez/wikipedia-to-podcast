import argparse
import logging
import sys
import os
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Add utils directory to Python path to allow imports
script_dir = os.path.dirname(os.path.realpath(__file__))
utils_dir = os.path.join(script_dir, "utils")
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

try:
    from utils.wikipedia import get_wikipedia_page_as_markdown
    from utils.text_gen import generate_text, GenerationResponse
    from utils.audio_gen import generate_audio, AudioGenerationResponse
    from config import AUDIO_OUTPUT_DIR  # Import for constructing full path message
except ImportError as e:
    logging.error(f"Failed to import utility modules: {e}")
    logging.error(
        "Ensure 'utils' directory is in the same directory as run.py and contains required modules."
    )
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a podcast episode from a Wikipedia article."
    )
    parser.add_argument(
        "query", type=str, help="The search query for the Wikipedia page."
    )
    parser.add_argument(
        "output_filename",
        type=str,
        help=f"The desired name for the output audio file (e.g., 'podcast.mp3'). It will be saved in '{AUDIO_OUTPUT_DIR}'.",
    )
    parser.add_argument(
        "--markdown-output",
        type=str,
        default=None,
        help="Optional path to save the generated podcast script as a markdown file. Defaults to the audio filename with .md extension.",
    )
    # Add more arguments here if needed in the future (e.g., language, voice selection)

    args = parser.parse_args()

    logging.info(f"Starting podcast generation for query: '{args.query}'")

    # 1. Fetch Wikipedia Content
    logging.info("Fetching Wikipedia content...")
    wiki_result = get_wikipedia_page_as_markdown(args.query)
    if not wiki_result:
        logging.error("Failed to retrieve Wikipedia content. Exiting.")
        sys.exit(1)

    page_url, markdown_content = wiki_result
    logging.info(f"Successfully fetched content from: {page_url}")
    # logging.debug(f"Markdown Content:\n{{{markdown_content[:500]}...") # Optional: log snippet

    # 2. Generate Podcast Script
    logging.info("Generating podcast script from Wikipedia content...")
    try:
        text_gen_response: Optional[GenerationResponse] = generate_text(
            markdown_content
        )
        if text_gen_response is None:
            logging.error("Text generation failed or returned no response.")
            sys.exit(1)

        logging.info(
            f"Text generation complete. Tokens: {text_gen_response.total_tokens}, Est. Cost: ${text_gen_response.estimated_cost_usd:.4f}"
        )
        podcast_script = text_gen_response.text
        # logging.debug(f"Generated Script:\n{{{podcast_script[:500]}...") # Optional: log snippet
    except Exception as e:
        logging.error(f"Failed during text generation: {e}")
        sys.exit(1)

    if not podcast_script:
        logging.error("Text generation resulted in an empty script. Exiting.")
        sys.exit(1)

    # 2.5. Save Markdown Script (Optional)
    markdown_output_path = args.markdown_output
    if not markdown_output_path:
        # Default filename based on audio output
        base_name, _ = os.path.splitext(args.output_filename)
        # Prepend the output directory to the default markdown filename
        markdown_output_path = os.path.join(AUDIO_OUTPUT_DIR, f"{base_name}.md")
    else:
        # If a path was provided, ensure it's placed in the output dir as well
        # (or decide if an absolute path should override this)
        # For simplicity, let's assume relative paths should go into AUDIO_OUTPUT_DIR
        if not os.path.isabs(markdown_output_path):
            markdown_output_path = os.path.join(AUDIO_OUTPUT_DIR, markdown_output_path)

    try:
        # Ensure the directory exists (might be redundant if audio step already did)
        os.makedirs(os.path.dirname(markdown_output_path), exist_ok=True)
        with open(markdown_output_path, "w", encoding="utf-8") as md_file:
            md_file.write(podcast_script)
        logging.info(f"Podcast script saved to markdown file: {markdown_output_path}")
    except IOError as e:
        logging.warning(f"Could not save markdown file to {markdown_output_path}: {e}")
        # Continue without saving markdown, as it's optional

    # 3. Generate Audio
    logging.info(
        f"Generating audio for the script, saving to {args.output_filename}..."
    )
    try:
        audio_gen_response: AudioGenerationResponse = generate_audio(
            podcast_script, args.output_filename
        )
        if audio_gen_response.success and audio_gen_response.filepath:
            full_audio_path = os.path.abspath(audio_gen_response.filepath)
            logging.info(
                f"Podcast audio successfully generated and saved to: {full_audio_path}"
            )
        else:
            logging.error("Audio generation failed.")
            sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred during audio generation: {e}")
        sys.exit(1)

    logging.info("Podcast generation process completed successfully.")


if __name__ == "__main__":
    main()
