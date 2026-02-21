# dci_website_ai_qa

Lightweight CLI tool that analyzes a website, captures a screenshot and DOM tree, and uses an AI generator to produce automated test code stored under `tests/generated_test.py`.

## Project Structure

- `agent.py` - CLI entrypoint: prompts for a URL, runs analysis, and writes generated tests.
- `analyzer.py` - website analysis utilities (captures screenshot and DOM tree).
- `ai_test_generator.py` - AI-based test-case generation logic.
- `tests/generated_test.py` - output file created by `agent.py` containing generated tests.

## Prerequisites

- Python 3.10+ (or the Python version used by your environment).
- A virtual environment is strongly recommended.
- Any project-specific dependencies (see `requirements.txt` if present).

## Installation (Windows)

1. Open PowerShell and create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. (Optional) If a `requirements.txt` file exists, install dependencies:

```powershell
pip install -r requirements.txt
```

3. If there is no `requirements.txt`, install any packages your environment needs (examples):

```powershell
pip install requests beautifulsoup4 playwright selenium pytest
```

Tip: To generate a `requirements.txt` after installing packages, run:

```powershell
pip freeze > requirements.txt
```

## Usage / Workflow

High-level workflow performed by `agent.py`:

1. User runs the CLI and provides a website URL when prompted.
2. `analyzer.analyze_website(URL)` visits the site and returns a screenshot and a DOM/tree representation.
3. `ai_test_generator.generate_tests(URL, screenshot, tree)` produces a Python test file as a string.
4. `agent.py` writes that code to `tests/generated_test.py` and reports completion.

Typical run (from project root, with venv active):

```powershell
python agent.py
# Enter the URL when prompted (e.g. https://example.com)
```

After completion you should see `tests/generated_test.py` created or updated.

## Running the Generated Tests

If the generated tests use `pytest`-style tests, run:

```powershell
pip install pytest
pytest tests/generated_test.py
```

Adjust the test runner or command depending on how `ai_test_generator` formats tests.

## Development Notes

- If you want the project to pin dependencies, add a `requirements.txt` and include the packages used by `analyzer.py` and `ai_test_generator.py`.
- To customize the generation behavior, edit `ai_test_generator.py`.
- To change how pages are analyzed (different browser, screenshot size, or DOM extraction), edit `analyzer.py`.

## Troubleshooting

- If `agent.py` fails when importing modules, ensure your venv is activated and required packages are installed.
- If screenshot or DOM capture fails, check that the analyzer's browser driver or headless tool (Playwright/Selenium) is installed and configured.

## Contributing

Open an issue or submit a pull request with changes. Keep changes minimal and document any added dependencies in `requirements.txt`.

---

Generated README for the repository. If you'd like, I can also create a `requirements.txt` skeleton or run the project to verify the workflow locally.
