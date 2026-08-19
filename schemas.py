from pydantic import BaseModel, Field
from typing import List, Optional

class CopywritingOutput(BaseModel):
    headline: str = Field(description="Attention-grabbing headline matching requested platform tone.")
    body_text: str = Field(description="Core marketing copy optimized for conversion.")
    call_to_action: str = Field(description="Clear CTA guiding the user on next steps.")
    hashtags: Optional[List[str]] = Field(default=[], description="Relevant platform-specific hashtags.")