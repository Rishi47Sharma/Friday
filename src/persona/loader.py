import yaml
from pathlib import Path

def load_persona(yaml_path: str | Path) -> str:
    """Loads persona.yaml and builds a dense, token-efficient system prompt."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    name = data.get('name', 'Assistant')
    core = data.get('core_prompt', '')
    voice = ", ".join(data.get('voice', []))
    user_info = data.get('user_info', '')
    
    # Flatten style rules for token efficiency
    rules_list = data.get('style_rules', [])
    rules = ", ".join([f"{list(r.keys())[0]}: {list(r.values())[0]}" if isinstance(r, dict) else str(r) for r in rules_list])
    
    boundaries = ", ".join(data.get('boundaries', []))

    # Template strictly follows 02-persona-spec.md
    sys_prompt = f"You are {name}. {core} Voice: {voice}. "
    if rules:
        sys_prompt += f"Rules: {rules}. "
    if boundaries:
        sys_prompt += f"Boundaries: {boundaries}."
    if user_info:
        sys_prompt += f"User Info: {user_info}."

    return sys_prompt.strip()