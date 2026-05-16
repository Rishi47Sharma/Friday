import asyncio
import yaml
from pathlib import Path
from dotenv import load_dotenv
import sys

# Load environment variables (API keys)
load_dotenv()

# Ensure the root directory is in the path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.companion import Companion

async def main():
    # 1. Read the config from the YAML file dynamically
    with open("configs/default.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 2. Initialize Companion
    # (Adjust the path to kavi.yaml if necessary based on your exact folder structure)
    bot = Companion("src/persona/templates/kavi.yaml", config)
    
    print("==================================================")
    print("Friday v0 is online! Type 'exit' or 'quit' to stop.")
    print("==================================================\n")
    
    # 3. Interactive Chat Loop
    while True:
        user_input = input("Batman: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Friday: Shutting down. Goodbye!")
            break
            
        reply = await bot.chat(user_input, user_id="user_123")
        print(f"Friday: {reply}\n")

if __name__ == "__main__":
    asyncio.run(main())