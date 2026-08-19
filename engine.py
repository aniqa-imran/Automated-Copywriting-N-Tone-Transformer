import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schemas import CopywritingOutput

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env file!")

def build_master_prompt(product_name: str, description: str, platform: str, tone: str) -> str:
    return f"""
    You are an expert enterprise copywriter.

    [PRODUCT NAME]: {product_name}
    [DESCRIPTION]: {description}
    [TARGET PLATFORM]: {platform}
    [TARGET TONE]: {tone}

    Generate high-converting promotional copy that strictly respects platform formatting.
    Ensure you output a valid JSON matching the schema.
    """

async def generate_single_copy_async(
    semaphore: asyncio.Semaphore,
    product_name: str,
    description: str,
    platform: str,
    tone: str,
    temperature: float = 0.7,
    max_tokens: int = 1500
) -> CopywritingOutput:
    async with semaphore:
        prompt = build_master_prompt(product_name, description, platform, tone)
        
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            response_mime_type="application/json",
            response_schema=CopywritingOutput
        )
        
        try:
            # Fresh client per request to avoid event loop mismatch
            client = genai.Client(api_key=API_KEY)
            
            response = await client.aio.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=config
            )
            
            if not response.text or not response.text.strip():
                raise ValueError("API returned an empty response.")
                
            return CopywritingOutput.model_validate_json(response.text)
        except Exception as e:
            print(f"Generation Error: {e}")
            raise e

async def run_batch_pipeline(items: list[dict], max_concurrency: int = 3, temperature: float = 0.7, max_tokens: int = 1500):
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [
        generate_single_copy_async(
            semaphore=semaphore,
            product_name=item.get("product_name", "Product"),
            description=item.get("description", ""),
            platform=item.get("platform", "LinkedIn"),
            tone=item.get("tone", "Professional"),
            temperature=temperature,
            max_tokens=max_tokens
        )
        for item in items
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)
