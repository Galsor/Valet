from pathlib import Path

# Path
ROOT_FOLDER = Path(__file__).parent.parent.parent
DB_FOLDER = ROOT_FOLDER / "src" / "db"

DOCUMENT_STORE_PICKLE_PATH = DB_FOLDER / "document_store.pkl"
ARCHIVE_FILE_NAME = "data/result.json"

# Test sample size
TEST_SET_SIZE = 30
DOC_STORE_SIZE = 500

# Embedding
EMBEDDING_MODEL = "sentence-transformers/distiluse-base-multilingual-cased-v1"
EMBEDDING_DIM = 512
RETRIVED_DOCUMENTS = 5

# NLP
SPACY_MODEL = "fr_core_news_sm"
