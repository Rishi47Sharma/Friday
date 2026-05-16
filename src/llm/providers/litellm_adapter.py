import litellm
from typing import List, Dict, Any
from ..base import BaseLLM

class LiteLLMAdapter(BaseLLM):
    def __init__(self, provider: str, model: str):
        # LiteLLM expects 'provider/model' format (e.g., 'groq/llama3-8b-8192')
        self.model_str = f"{provider}/{model}" if provider else model

    async def chat(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> Any:
        kwargs = {"model": self.model_str, "messages": messages}
        if tools:
            kwargs["tools"] = tools
            
        # litellm.acompletion handles the async call to the respective provider API
        return await litellm.acompletion(**kwargs)