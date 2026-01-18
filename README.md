# Starter API Automation Repo (Phase 1)

This is a **simple, interview-friendly** API automation project using Python + pytest.
It is intentionally lightweight so you can understand and explain every file.

## What it tests
- GET a post (positive + basic negative)
- POST create a post (positive)
- A lightweight negative payload test

Demo API used: https://jsonplaceholder.typicode.com

## How to run
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
python run_tests.py
```

## Project structure
- `config/config.json` stores base_url, endpoints, headers, and test data
- `tests/` contains pytest tests
- `utils/` contains helpers for config loading and URL formatting
- `auth/` includes a placeholder token generator for real APIs
