"""
AIClient — LLM wrapper for Venture Architect (Phase 7).

T-025: Gemini/OpenAI wrapper with structured JSON output.
- Primary: Gemini (google-generativeai, gemini-2.0-flash)
- Fallback: OpenAI (config-driven)
- Env vars: GEMINI_API_KEY, OPENAI_API_KEY (via dotenv / os.getenv)
"""
import json
import logging
import re
import os
from typing import Any, Dict, Optional, Type, TypeVar

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar("T")


class AIClient:
    """
    Thin LLM wrapper. Sends system + user prompt, returns parsed JSON.
    No business logic — all intelligence is in the prompts.
    """

    def __init__(
        self,
        provider: str = "gemini",
        model: str = "gemini-2.0-flash",
        api_key: Optional[str] = None,
    ):
        """
        Initialize AIClient.

        Args:
            provider: "gemini" or "openai"
            model: Model identifier (e.g. gemini-2.0-flash, gpt-4o-mini)
            api_key: API key, or None to use GEMINI_API_KEY / OPENAI_API_KEY env var

        Raises:
            ValueError: If no API key is available for the chosen provider
        """
        self.provider = provider.lower()
        self.model = model
        self._client = None
        self._api_key = api_key or (
            os.getenv("GEMINI_API_KEY") if self.provider == "gemini" else os.getenv("OPENAI_API_KEY")
        )
        if not self._api_key:
            raise ValueError(
                f"{self.provider.upper()} API key required. "
                "Set GEMINI_API_KEY or OPENAI_API_KEY env var, or pass api_key."
            )
        self._init_client()

    def _init_client(self) -> None:
        """Initialize the underlying LLM client."""
        if self.provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self._api_key)
                self._client = genai.GenerativeModel(self.model)
            except ImportError as e:
                raise ImportError(
                    "google-generativeai not installed. Run: pip install google-generativeai"
                ) from e
        elif self.provider == "openai":
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self._api_key)
            except ImportError as e:
                raise ImportError("openai not installed. Run: pip install openai") from e
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Optional[Dict] = None,
        response_model: Optional[Type[T]] = None,
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        """
        Send prompt and parse JSON response.

        Args:
            system_prompt: Persona + instructions
            user_prompt: Data context (evidence, ICP, system_map)
            response_schema: Optional JSON schema for structured output
            response_model: Optional Pydantic model for validation
            temperature: Low (0.2-0.4) for analytical reasoning
            max_tokens: Max response length

        Returns:
            Parsed JSON dict from LLM response

        Raises:
            ValueError: If response is not valid JSON after retries
        """
        full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

        # Note: Gemini deprecated SDK doesn't support $defs in response_schema;
        # we rely on prompt + Pydantic validation instead.
        json_schema = None

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((ValueError, json.JSONDecodeError)),
        )
        def _call() -> str:
            raw = self._generate_raw(full_prompt, temperature, max_tokens, json_schema)
            _ = self._parse_json_response(raw)  # Validate parseable
            return raw

        try:
            raw_text = _call()
        except Exception as e:
            logger.error("LLM failed after retries: %s", e)
            raise ValueError(f"LLM returned invalid JSON after retries: {e}") from e

        data = self._parse_json_response(raw_text)

        if response_model is not None:
            try:
                validated = response_model.model_validate(data)
                return validated.model_dump()
            except Exception as e:
                raise ValueError(f"Pydantic validation failed: {e}") from e

        return data

    def _generate_raw(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        response_schema: Optional[Dict] = None,
    ) -> str:
        """Call the underlying LLM and return raw text."""
        if self.provider == "gemini":
            return self._generate_gemini(prompt, temperature, max_tokens, response_schema)
        if self.provider == "openai":
            return self._generate_openai(prompt, temperature, max_tokens)
        raise ValueError(f"Unknown provider: {self.provider}")

    def _generate_gemini(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        response_schema: Optional[Dict] = None,
    ) -> str:
        """Call Gemini API. (response_schema unused - deprecated SDK rejects $defs)"""
        from google.generativeai.types import GenerationConfig

        config = GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            response_mime_type="application/json",
        )
        response = self._client.generate_content(prompt, generation_config=config)
        if not response.text:
            raise ValueError("Gemini returned empty response")
        return response.text.strip()

    def _generate_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Call OpenAI API."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned empty response")
        return content.strip()

    def _parse_json_response(self, raw_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response. Handles ```json fences."""
        if not raw_text or not raw_text.strip():
            raise ValueError("Empty response")

        text = raw_text.strip()

        # Strip markdown code fences
        fence_pattern = r"^```(?:json)?\s*\n?(.*?)\n?```\s*$"
        match = re.search(fence_pattern, text, re.DOTALL)
        if match:
            text = match.group(1).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e
