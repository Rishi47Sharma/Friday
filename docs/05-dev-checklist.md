# Before coding, verify

- [ ] persona.yaml < 150 tokens
- [ ] system prompt built < 300 tokens
- [ ] tool schemas total < 200 tokens
- [ ] history window = 6
- [ ] memory recall <=5
- [ ] token logger enabled

Run: `poetry run python -m ai_companion --debug-tokens`
