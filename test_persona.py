import sys
import pprint
from pathlib import Path

# Add src to Python path so we can import friday
sys.path.append(str(Path(__file__).parent / "src"))

from friday.persona.loader import load_persona

if __name__ == "__main__":
    yaml_path = Path("persona/templates/kavi.yaml")
    print(f"Loading {yaml_path}...")
    try:
        result = load_persona(yaml_path)
        print("\nLoaded successfully:")
        pprint.pprint(result)
    except Exception as e:
        print(f"\nError loading persona: {e}")
