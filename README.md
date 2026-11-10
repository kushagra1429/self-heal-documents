# Self-Healing Technical Documentation

A reusable Docker-based GitHub Action and Python CLI that identifies Markdown sections potentially affected by Python code changes.

**Current stage:** deterministic Git + AST + Markdown candidate detection. It does not yet prove claims stale, call an LLM, edit files, or create PRs. Findings are review candidates only.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

## Consumer repository workflow

After publishing this repository, replace `YOUR_GITHUB_USERNAME` in `examples/consumer-repo/.github/workflows/documentation-review.yml` and copy that workflow into a repository you want to protect.

Configure branch protection on `main`: require a pull request, one approval, and the `Documentation review` check. The current check verifies that analysis ran; it does not fail merely because it found a candidate, because candidates are not confirmed defects.

## Local demo

Create two commits in a test repository: commit a Python function and README, then change a documented default argument and commit again. Run:

```bash
self-healing-docs --repo . --base <BASE_SHA> --head HEAD --docs README.md --output report.json
```

The JSON report includes AST-classified symbol changes and matching Markdown sections.

## Security

The action uses read-only repository permissions, does not execute target code, and does not need secrets. Do not use `pull_request_target`. Pin third-party actions to reviewed SHAs for production.
