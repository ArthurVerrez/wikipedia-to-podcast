from config import MODEL, SYSTEM_PROMPT, REASONING_EFFORT
from litellm import completion, completion_cost
from dataclasses import dataclass
import logging
from typing import Optional


@dataclass
class GenerationResponse:
    text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float


def generate_text(input_text: str) -> Optional[GenerationResponse]:
    try:
        response = completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": input_text},
            ],
            reasoning_effort=REASONING_EFFORT,
        )

        # Extract information from the response
        content = response.choices[0].message.content
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        # Calculate cost
        cost = completion_cost(completion_response=response)

        return GenerationResponse(
            text=content,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=cost,
        )
    except Exception as e:
        logging.error(f"Error during text generation with litellm: {e}")
        if hasattr(e, "message"):
            logging.error(f"LiteLLM Error Details: {e.message}")
        return None
