from .providers.litellm_adapter import LiteLLMAdapter
from .base import BaseLLM

def get_llm(config: dict) -> BaseLLM:
    """Factory to instantiate the LLM adapter based on user config."""
    provider = config.get("provider", "openai")
    model = config.get("model", "gpt-3.5-turbo")
    return LiteLLMAdapter(provider, model)