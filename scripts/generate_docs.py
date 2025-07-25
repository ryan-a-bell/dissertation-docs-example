import os
import shutil
from pathlib import Path
import pandas as pd

SRC_DIR = Path('src')
GENERATED_DIR = Path('docs/generated')
ASSETS_PDF_DIR = Path('docs/assets/pdfs')


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


if __name__ == '__main__':
    main()
