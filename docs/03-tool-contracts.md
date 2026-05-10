# Tools v0

Use JSON schema only. No long descriptions.

web_search:
  params: {"query": "string"}
  returns: [{"title","snippet","url"}] max 3 results

set_reminder:
  params: {"text": "string", "time": "ISO8601"}
  returns: {"id","status"}

LLM output format:
{"tool":"web_search","args":{...}}

Keep tool descriptions <25 words each in system prompt.
