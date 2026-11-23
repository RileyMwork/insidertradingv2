# Development Cycle
---

`.venv\Scripts\Activate.ps1`\
`python -m pip install -e ".[dev]"`\
`python -m pip check`\
`ruff format .`\
`ruff check .`\
`mypy src`\
`pytest`

---