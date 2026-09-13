"""
content_generator.py

Takes a product spec (from spec.py) and calls an LLM to generate
real content for each section. Returns a structured dict that
pdf_builder.py and metadata_generator.py can both consume.
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"  # adjust to whichever model you have access to


def build_prompt(spec: dict) -> str:
    """Turn the spec into a single prompt asking for JSON content per section."""
    section_lines = "\n".join(
        f"- {s['name']}: {s['purpose']}" for s in spec["sections"]
    )
    principles = ", ".join(spec["design_principles"])

    return f"""You are creating content for a printable digital product: "{spec['title']}".

The product has these sections:
{section_lines}

Design principles to keep in mind: {principles}

For each section, write the actual content that will appear in the printed
product — prompts, labels, short instructional text, or example entries as
appropriate for that section. Keep tone supportive and non-clinical.

Respond ONLY with valid JSON in this exact shape, no preamble, no markdown fences:
{{
  "section_name": "generated content as a string (use \\n for line breaks)",
  ...
}}
Use the exact section names given above as the keys.
"""


def generate_content(spec: dict) -> dict:
    """Call the LLM and return a dict of {section_name: content}."""
    prompt = build_prompt(spec)

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text.strip()

    # Defensive cleanup in case the model wraps output in fences anyway
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        content = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model did not return valid JSON. Raw output:\n{raw_text}"
        ) from e

    return content


if __name__ == "__main__":
    # Quick manual test: run this file directly to sanity-check output
    from spec import get_spec

    spec = get_spec("adhd_daily_planner")
    content = generate_content(spec)

    print(json.dumps(content, indent=2))