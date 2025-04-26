import os
import logging
from openai import OpenAI  # Import the synchronous client
from dataclasses import dataclass  # Add dataclass import
from config import (
    TTS_MODEL,
    TTS_VOICE,
    TTS_INSTRUCTIONS,
    TTS_RESPONSE_FORMAT,
    AUDIO_OUTPUT_DIR,
)


client = OpenAI()


@dataclass
class AudioGenerationResponse:
    """Holds the result of an audio generation attempt."""

    filepath: str | None
    success: bool


def generate_audio(input_text: str, output_filename: str) -> AudioGenerationResponse:
    """Generates audio from text using the synchronous OpenAI TTS API and saves it directly to a file.

    Args:
        input_text: The text to convert to speech.
        output_filename: The desired name for the output audio file (e.g., "podcast_intro.mp3")
                         relative to AUDIO_OUTPUT_DIR.

    Returns:
        An AudioGenerationResponse object indicating success and the filepath.
    """
    if not client:
        logging.error("OpenAI client not initialized. Cannot generate audio.")
        return AudioGenerationResponse(filepath=None, success=False)

    if not input_text:
        logging.warning("No input text provided for audio generation.")
        return AudioGenerationResponse(filepath=None, success=False)

    # Ensure the output directory exists
    try:
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    except OSError as e:
        logging.error(f"Failed to create output directory {AUDIO_OUTPUT_DIR}: {e}")
        return AudioGenerationResponse(filepath=None, success=False)

    output_filepath = os.path.join(AUDIO_OUTPUT_DIR, output_filename)

    logging.info(
        f"Generating audio for: '{input_text[:50]}...' using {TTS_MODEL} ({TTS_VOICE}) -> {output_filepath}"
    )

    try:
        # Use the synchronous client's method
        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=input_text,
            instructions=TTS_INSTRUCTIONS,
            response_format=TTS_RESPONSE_FORMAT,
        )

        # Stream the binary audio content directly to the output file
        response.stream_to_file(output_filepath)

        logging.info(f"Audio saved successfully to {output_filepath}")
        return AudioGenerationResponse(filepath=output_filepath, success=True)

    except Exception as e:
        logging.error(f"Error generating or saving audio to {output_filepath}: {e}")
        # Log more details if available (similar to the other function)
        if hasattr(e, "response") and e.response is not None:
            logging.error(
                f"OpenAI API Error Status: {getattr(e.response, 'status_code', 'N/A')}"
            )
            try:
                error_text = e.response.text
                logging.error(f"OpenAI API Error Response: {error_text}")
            except Exception:
                logging.error("Could not read OpenAI API error response text.")
        elif hasattr(e, "body"):
            logging.error(f"OpenAI API Error Body: {e.body}")
        # Clean up potentially partially written file on error
        if os.path.exists(output_filepath):
            try:
                os.remove(output_filepath)
                logging.info(f"Cleaned up partially written file: {output_filepath}")
            except OSError as rm_err:
                logging.error(f"Failed to clean up file {output_filepath}: {rm_err}")
        return AudioGenerationResponse(filepath=None, success=False)
