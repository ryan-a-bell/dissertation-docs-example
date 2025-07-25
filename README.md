# dissertation-docs-example

This repository demonstrates automated documentation generation with MkDocs.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate documentation:
   ```bash
   python scripts/generate_docs.py
   mkdocs serve
   ```

## Deployment

Documentation is deployed automatically via GitHub Actions on pushes to `main`.
