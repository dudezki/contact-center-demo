"""Personas served by the single shared LiveKit agent.

The LiveKit workspace allows one deployed agent, so CONNECT. and HAVEN. share it. Each site's token
service puts {"persona": "<key>"} in the agent dispatch metadata; anything missing or unknown falls
back to the CONNECT. contact-center assistant.
"""
import json
from dataclasses import dataclass

from . import haven_prompt, miel_prompt, prompt


@dataclass(frozen=True)
class Persona:
    instructions: str
    greeting: str
    farewell: str


PERSONAS: dict[str, Persona] = {
    "connect": Persona(prompt.SYSTEM_PROMPT, prompt.GREETING, prompt.FAREWELL),
    "haven": Persona(haven_prompt.SYSTEM_PROMPT, haven_prompt.GREETING, haven_prompt.FAREWELL),
    "miel": Persona(miel_prompt.SYSTEM_PROMPT, miel_prompt.GREETING, miel_prompt.FAREWELL),
}
DEFAULT = "connect"


def resolve(metadata: str | None) -> tuple[str, Persona]:
    """Pick the persona from dispatch metadata. Never raises: bad input means the default."""
    try:
        key = json.loads(metadata or "{}").get("persona", DEFAULT)
    except (ValueError, AttributeError):
        key = DEFAULT
    if key not in PERSONAS:
        key = DEFAULT
    return key, PERSONAS[key]
