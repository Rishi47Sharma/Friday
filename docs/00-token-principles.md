# Token Budget Principles

Goal: v0 < 1.5k tokens per turn.

Rules:
1. System prompt max 300 tokens. Persona data compress karo, examples docs me rakho.
2. History: last 6 turns only. Older turns summarize.
3. Memory: top 5 facts, each <20 words.
4. Tools: JSON schema only, no description fluff.
5. No repeating instructions. Load once at startup.
6. Use short keys: sys, usr, mem, tools.

Measure: log tokens per turn in dev mode.
