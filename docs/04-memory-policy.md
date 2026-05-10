# Memory v0

Store only facts, not chat.

Schema: key, value, updated_at

Recall policy:
- always: name, preferences, language
- query match: top 3 by keyword
- limit: 5 facts total

Summarization:
After 10 turns, LLM summarize to 3 bullet facts (<60 tokens). Replace old history.

Compression prompt:
"Summarize user facts in 3 bullets, <15 words each."
