import os
import shutil
from pathlib import Path
import pandas as pd
import yaml

SRC_DIR = Path('src')
DOCS_DIR = Path('docs')
GENERATED_DIR = DOCS_DIR / 'generated'
ASSETS_PDF_DIR = DOCS_DIR / 'assets/pdfs'


def clean_generated():
    if GENERATED_DIR.exists():
        shutil.rmtree(GENERATED_DIR)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_PDF_DIR.mkdir(parents=True, exist_ok=True)


def process_notebook(src_path, rel_path):
    dest = GENERATED_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest)


def process_markdown(src_path, rel_path):
    dest = GENERATED_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest)


def process_csv(src_path, rel_path):
    dest = GENERATED_DIR / rel_path.with_suffix('.md')
    dest.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(src_path)
    with dest.open('w') as f:
        f.write('# ' + rel_path.name + '\n\n')
        f.write(df.to_markdown(index=False))
        f.write('\n')


def process_pdf(src_path, rel_path):
    asset_dest = ASSETS_PDF_DIR / rel_path.name
    shutil.copy2(src_path, asset_dest)
    page_dest = GENERATED_DIR / rel_path.with_suffix('.md')
    page_dest.parent.mkdir(parents=True, exist_ok=True)
    with page_dest.open('w') as f:
        f.write(f'# {rel_path.stem}\n\n')
        f.write(f'<iframe src="../assets/pdfs/{rel_path.name}" class="embed-pdf"></iframe>\n\n')
        f.write(f'[Download PDF](../assets/pdfs/{rel_path.name})\n')


def generate_index(processed_paths):
    index_path = GENERATED_DIR / 'index.md'
    with index_path.open('w') as f:
        f.write('# Generated Documentation Index\n\n')
        for rel in sorted(processed_paths):
            page = rel.with_suffix('.md') if rel.suffix != '.ipynb' else rel
        f.write(f'- [{page.stem}]({page.as_posix()})\n')


def _insert_nav(nav_list, parts, target):
    """Recursively insert a file path into the nav structure."""
    title = parts[0].replace('-', ' ').title()
    if len(parts) == 1:
        nav_list.append({title: target})
        return

    # locate or create sublist for this directory
    for item in nav_list:
        if isinstance(item, dict) and title in item:
            sub = item[title]
            break
    else:
        sub = []
        nav_list.append({title: sub})

    _insert_nav(sub, parts[1:], target)


def generate_nav():
    """Walk DOCS_DIR and build a nav structure."""
    files = []
    for path in DOCS_DIR.rglob('*'):
        if not path.is_file():
            continue
        if 'assets' in path.parts or 'stylesheets' in path.parts:
            continue
        if path.suffix not in {'.md', '.ipynb'}:
            continue
        files.append(path.relative_to(DOCS_DIR))

    nav = []
    for rel in sorted(files):
        if rel.as_posix() == 'index.md':
            nav.insert(0, {'Home': rel.as_posix()})
        else:
            _insert_nav(nav, list(rel.parts), rel.as_posix())
    return nav


def merge_nav(nav):
    nav_text = yaml.dump({'nav': nav}, sort_keys=False)
    with open('mkdocs.yml', 'r') as f:
        content = f.read()
    idx = content.find('nav:')
    if idx != -1:
        content = content[:idx]
    content = content.rstrip() + '\n' + nav_text
    with open('mkdocs.yml', 'w') as f:
        f.write(content)


def main():
    clean_generated()
    processed = []
    for root, _, files in os.walk(SRC_DIR):
        for filename in files:
            src_path = Path(root) / filename
            rel_path = src_path.relative_to(SRC_DIR)
            if filename.endswith('.ipynb'):
                process_notebook(src_path, rel_path)
            elif filename.endswith('.md'):
                process_markdown(src_path, rel_path)
            elif filename.endswith('.csv'):
                process_csv(src_path, rel_path)
            elif filename.endswith('.pdf'):
                process_pdf(src_path, rel_path)
            else:
                continue
            processed.append(rel_path)
    generate_index(processed)
    print('Processed', len(processed), 'files')
    nav = generate_nav()
    merge_nav(nav)


if __name__ == '__main__':
    main()
