from pathlib import Path

ROOT_FOLDER = Path(__file__).parent.parent.parent
DB_FOLDER = ROOT_FOLDER / "src" / "db"

DOCUMENT_STORE_PICKLE_PATH = DB_FOLDER / "document_store.pkl"
ARCHIVE_FILE_NAME = "data/result.json"

TEST_SET_SIZE = 30
