import asyncio
from pathlib import Path
import sys

# Ensure src is in the path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from persona.loader import load_persona
from llm.registry import get_llm

async def run_benchmark():
    # 1. Define the combinations we want to test
    test_models = [
        {"provider": "gemini", "model": "gemini-2.5-flash"}
    ]
    
    # Assuming you have kavi.yaml and maybe a second one for testing
    test_personas = [
        Path("src/persona/templates/kavi.yaml")
    ]
    
    test_message = "Hi, can you introduce yourself?"

    print(f"{'Model':<25} | {'Persona':<10} | {'Prompt Tokens':<15} | {'Total Tokens'}")
    print("-" * 75)

    for persona_path in test_personas:
        # Load the compressed <300 token system prompt
        system_prompt = load_persona(persona_path)
        
        for config in test_models:
            llm = get_llm(config)
            
            # Build the exact message structure the Companion uses
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test_message}
            ]
            
            try:
                # Call the model
                response = await llm.chat(messages)

                print(response.choices[0].message.content)
                
                # LiteLLM standardizes the usage statistics across all providers
                usage = response.usage
                prompt_tokens = usage.prompt_tokens
                total_tokens = usage.total_tokens
                
                print(f"{config['provider']}/{config['model']:<15} | {persona_path.stem:<10} | {prompt_tokens:<15} | {total_tokens}")
            
            except Exception as e:
                print(f"{config['provider']}/{config['model']:<15} | {persona_path.stem:<10} | FAILED: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_benchmark())