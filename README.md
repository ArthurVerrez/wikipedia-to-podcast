# wikipedia-to-podcast

A simple Python tool to fetch a Wikipedia page, generate a podcast-style script from its content using an LLM, and convert that script into an audio file using Text-to-Speech.

**Example Podcast On LLMs:**

- **[Listen to Example Podcast](https://gabalpha.github.io/read-audio/?p=https://raw.githubusercontent.com/ArthurVerrez/wikipedia-to-podcast/main/example_llm_podcast.mp3)**

## Features

- Fetches content from a specified Wikipedia page.
- Uses LiteLLM to generate a coherent podcast script based on the Wikipedia content.
- Uses OpenAI's TTS API to synthesize the script into an audio file.
- Configurable models, voices, and prompts via `config.py`.
- Saves the generated script as a Markdown file.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ArthurVerrez/wikipedia-to-podcast.git
    cd wikipedia-to-podcast
    ```

2.  **Install dependencies:**
    _(Ensure you have Python 3.8+ installed)_

    ```bash
    pip install -r requirements.txt
    ```

    _(Note: A `requirements.txt` file should be created containing packages like `openai`, `litellm`, `wikipedia-api`, `python-dotenv`)_

3.  **Configure API Keys:**

    - The tool uses **OpenAI** for Text-to-Speech (TTS) and **LiteLLM** for Text Generation. By default, LiteLLM is configured to use a **Gemini** model (`gemini/gemini-1.5-flash-latest`), which is recommended for its strong performance and cost-effectiveness, especially with long Wikipedia articles.
    - You will need API keys for the services you use.

    - **OpenAI API Key (for TTS):**

      - Set as an environment variable:
        ```bash
        export OPENAI_API_KEY='your-openai-api-key'
        ```
      - Or add to a `.env` file:
        ```
        OPENAI_API_KEY=your-openai-api-key
        ```

    - **Gemini API Key (for Text Generation - Default):**

      - If using the default Gemini model, set your Google AI Studio API key:
      - Set as an environment variable:
        ```bash
        export GEMINI_API_KEY='your-gemini-api-key'
        ```
      - Or add to a `.env` file:
        ```
        GEMINI_API_KEY=your-gemini-api-key
        ```

    - **Other Models (via LiteLLM):**

      - If you configure `config.py` to use a different model via LiteLLM (e.g., Anthropic Claude), you will need to set the corresponding API key (e.g., `ANTHROPIC_API_KEY`). Refer to the [LiteLLM documentation](https://docs.litellm.ai/docs/providers) for required environment variables.

    - _(Ensure `.env` is added to your `.gitignore`)_

4.  **(Optional) Customize Configuration:**
    - Edit `config.py` to change the text generation model (`MODEL`), TTS model (`TTS_MODEL`), voice (`TTS_VOICE`), system prompt (`SYSTEM_PROMPT`), etc. See comments in the file for options.

## Usage

Run the script from the command line, providing the Wikipedia query and the desired output audio filename:

```bash
python run.py "<Wikipedia Page Query>" <output_audio_filename.mp3> [--markdown-output <output_script.md>]
```

- `<Wikipedia Page Query>`: The topic to search for on Wikipedia (e.g., "Large language model").
- `<output_audio_filename.mp3>`: The name for the generated audio file (e.g., `llm_podcast.mp3`). This will be saved in the directory specified by `AUDIO_OUTPUT_DIR` in `config.py` (default is `output/`).
- `--markdown-output` (Optional): Specify a filename for the generated script in Markdown format. If omitted, it defaults to `<output_audio_filename>.md`. This file will also be saved in the `AUDIO_OUTPUT_DIR`.

## Example

```bash
python run.py "Python (programming language)" python_podcast.mp3
```

This command will:

1.  Fetch the Wikipedia page for "Python (programming language)".
2.  Generate a podcast script based on the content.
3.  Save the script to `output/python_podcast.md`.
4.  Generate an audio file `output/python_podcast.mp3` using the configured TTS settings.
