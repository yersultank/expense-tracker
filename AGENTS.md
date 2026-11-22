# AGENTS.md — Repository Instructions

## Project Purpose & Architecture
- **Purpose:** Lightweight Python CLI/library for tracking expenses, calculating category summaries, applying discount strategies, and exporting plain-text reports.
- **Structure:**
  - `calculator.py`: Core business logic (expense management, discount calculations, category aggregation, report export).
  - `test_calculator.py`: Automated `pytest` unit test suite.
  - `requirements.txt`: Python dependencies.
  - `README.md`: Setup and usage documentation.

## Setup & Safe Commands
- Install dependencies: `pip install -r requirements.txt`
- Run test suite: `pytest -v`
- Check git status/diff: `git status`, `git diff`

## Coding Conventions & Test Expectations
- Follow PEP 8 naming conventions and include Python type hints on all function signatures.
- Keep business logic decoupled from file I/O.
- Every behavior change or bug fix must keep all existing acceptance tests passing and include a targeted unit test for the new behavior.

## Forbidden Actions
- **No secrets:** Never read, create, or commit `.env` files, API keys, or credentials.
- **No production deployments:** Do not run deployment scripts or publish packages.
- **No destructive commands:** Never execute `rm -rf`, `git reset --hard`, or `git push --force`.
- **No unreviewed dependency changes:** Do not install or add new third-party packages without explicit human approval.