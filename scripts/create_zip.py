"""Package source code into deliverables/event-booking-system.zip"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / 'deliverables'
ZIP_PATH = OUT_DIR / 'event-booking-system.zip'

SKIP_DIRS = {
    '__pycache__', '.git', '.venv', 'venv', 'env', 'staticfiles',
    'node_modules', '.idea', '.vscode', 'deliverables', 'report_output',
}
SKIP_FILES = {'.pyc', '.sqlite3'}


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return True
    if path.suffix in SKIP_FILES:
        return True
    if path.name.endswith('.zip'):
        return True
    return False


def create_zip():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in ROOT.rglob('*'):
            if file_path.is_file() and not should_skip(file_path.relative_to(ROOT)):
                arcname = file_path.relative_to(ROOT)
                zf.write(file_path, arcname)
    print(f'Created {ZIP_PATH}')


if __name__ == '__main__':
    create_zip()
