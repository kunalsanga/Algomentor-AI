import os
from google import genai
from pydantic import BaseModel
from typing import Type, TypeVar, Any
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

class GeminiClient:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY is not set. Gemini API calls will fail.")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        """
        Calls Gemini to generate content matching a specific Pydantic schema asynchronously.
        We retry once if parsing fails.
        """
        logger.info(f"Generating structured data with schema: {schema.__name__}")
        
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.2, # Low temperature for more deterministic/logical outputs
                ),
            )
            
            if hasattr(response, 'parsed') and response.parsed is not None:
                if isinstance(response.parsed, dict):
                    return schema.model_validate(response.parsed)
                return response.parsed
            else:
                return schema.model_validate_json(response.text)
                
        except Exception as e:
            logger.error(f"Failed to generate structured data: {e}. Retrying once...")
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.2,
                ),
            )
            if hasattr(response, 'parsed') and response.parsed is not None:
                if isinstance(response.parsed, dict):
                    return schema.model_validate(response.parsed)
                return response.parsed
            else:
                return schema.model_validate_json(response.text)

gemini_client = GeminiClient()
