<<<<<<< HEAD
# QA API Automation Portfolio Project

This repository contains a **Python-based API automation test suite** designed to demonstrate
**backend QA automation skills**, clean project structure, and automation best practices.

The project focuses on **API testing and validation**, rather than UI automation, to reflect
real-world testing commonly performed by backend and data-focused QA teams.

---

## 🎯 Project Goals
- Demonstrate API automation using Python
- Validate REST API endpoints using automated tests
- Show clean, maintainable automation structure
- Cover positive, negative, and edge test scenarios
- Provide a clear, interview-friendly example of QA automation work

---

## 🛠 Tech Stack
- Python
- Requests
- Pytest
- JSON configuration files

---

## 📂 Project Structure
```text
starter_api_automation_repo/
├── config/
│   └── config.json
├── auth/
│   └── token_generator.py
├── tests/
│   ├── test_get_post.py
│   ├── test_create_post.py
│   └── test_negative_cases.py
├── utils/
│   └── helpers.py
├── requirements.txt
├── run_tests.py
└── README.md
=======
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
>>>>>>> b70eb2b (Update config with realistic application data)
